#----------------------------------------
#   app.py -> Contains server code
#----------------------------------------
from flask import (
    Flask, render_template, request, redirect, flash,
    session, jsonify, url_for, Blueprint
)
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth
import os


from db import SessionLocal
from models import (
    Item, Booking,
    get_all_items,
    item_by_id,
    get_user_bookings,
    get_items_on_hold,
    get_items_on_occupy
)

load_dotenv()

app = Flask(__name__)
CORS(app)
app.secret_key = "blahblah22"


# oauth thing
oauth = OAuth(app)

oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)


# ----------------------------------
app = Flask(__name__)
CORS(app)
app.secret_key = "blahblah22"

# --------------------
# Helper Functions
# --------------------

def get_db():
    return SessionLocal()


# ------------------------
# Routes
# ------------------------

@app.route("/")
@app.route("/library")
def home():
    db = get_db()
    items = get_all_items(db)
    db.close()
    return render_template("index.html", items=items)

@app.route("/library/user-bookings", methods=["POST"])
def user_history():
    ''' When user wants to see all of the stuff they have booked for an email. '''

    email = request.form.get("email")

    if not email:
        flash("Email is required")
        return redirect("/library")

    db = get_db()
    bookings = get_user_bookings(db, email)

    rows = []
    for b in bookings:
        item = b.item

        hold_days = (
            item.hold_time - (datetime.now() - b.booked_date).days
            if b.on_hold_state else "NOT ON HOLD"
        )

        occupy_days = (
            item.occupy_time - (datetime.now() - b.occupied_date).days
            if b.on_occupied_state and b.occupied_date else "NOT ON OCCUPY"
        )

        rows.append([
            item.id,
            item.name,
            b.booked_date,
            hold_days,
            occupy_days
        ])

    db.close()
    return render_template("user_bookings.html", items=rows)

@app.route("/library/campusend", methods=["GET", "POST"])
def admin():
    ''' Interface visible for the FSU representative'''

    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username")
    password = request.form.get("password")

    if not (username and password):
        flash("Please enter credentials")
        return redirect("/library/campusend")

    if username == "ram" and password == "hari":
        session["logged_in"] = True
        return redirect("/library/arena")

    flash("Wrong username or password")
    return redirect("/library/campusend")

@app.route("/library/arena")
def admin_dashboard():
    if not session.get("logged_in"):
        flash("You are not authenticated")
        return redirect("/library/campusend")

    db = get_db()
    now = datetime.utcnow()

    # expire holds
    for item in get_items_on_hold(db):
        booking = item.bookings[-1]
        if (now - booking.booked_date).days > item.hold_time:
            booking.is_expired = True
            booking.on_hold_state = False
            item.available = True

    # expire occupies
    for item in get_items_on_occupy(db):
        booking = item.bookings[-1]
        if booking.occupied_date and (
            (now - booking.occupied_date).days > item.occupy_time
        ):
            booking.is_expired = True

    db.commit()

    # ---------------- dashboard data ----------------

    hold_items = []
    for item in get_items_on_hold(db):
        b = item.bookings[-1]
        hold_items.append([
            item.name,
            item.image_path,
            b.user_email[:9].upper(),
            b.booked_date,
            item.id
        ])

    return_items = []
    expired_items = []

    for item in get_items_on_occupy(db):
        b = item.bookings[-1]
        remaining = (
            item.occupy_time -
            (now - b.occupied_date).days
            if b.occupied_date else 0
        )

        row = [
            item.name,
            item.image_path,
            b.user_email[:9].upper(),
            remaining,
            item.id
        ]

        return_items.append(row)
        if remaining < 1:
            expired_items.append(row)

    db.close()

    return render_template(
        "dashboard.html",
        items=hold_items,
        returns=return_items,
        expired=expired_items
    )

@app.route("/library/return", methods=["POST"])
def return_item():
    ''' Changes the state of item to be available again and returned '''

    if not session.get("logged_in"):
        return jsonify(success=False, remarks="Not authenticated")

    item_id = request.get_json().get("id")

    db = get_db()
    item = item_by_id(db, item_id)

    if not item or not item.bookings:
        db.close()
        return jsonify(success=False, remarks="Invalid item")

    booking = item.bookings[-1]
    booking.is_expired = False
    booking.on_occupied_state = False
    item.available = True

    db.commit()
    db.close()

    return jsonify(success=True)

@app.route("/library/own-item", methods=["POST"])
def own_item():
    ''' Change the state of the item from hold state to own state'''

    if not session.get("logged_in"):
        return jsonify(success=False, remarks="Not authenticated")

    item_id = request.get_json().get("id")

    db = get_db()
    item = item_by_id(db, item_id)

    if not item or not item.bookings:
        db.close()
        return jsonify(success=False, remarks="Invalid item")

    booking = item.bookings[-1]
    booking.on_hold_state = False
    booking.on_occupied_state = True
    booking.occupied_date = datetime.utcnow()

    db.commit()
    db.close()

    return jsonify(success=True)


@app.route("/library/info")
def info():
    ''' Returns the information about a certain item (How much time for hold-clearing and stuffs)'''

    item_id = request.args.get("id")

    db = get_db()
    item = item_by_id(db, item_id)

    if not item:
        db.close()
        return jsonify(success=False)

    if not item.bookings:
        db.close()
        return jsonify(
            success=True,
            name=item.name,
            booked_on="Available",
            hold_state=0,
            hold_days=0,
            occupied_state=0,
            occupied_days=0,
        )

    b = item.bookings[-1]
    now = datetime.utcnow()

    hold_days = (
        item.hold_time - (now - b.booked_date).days
        if b.on_hold_state else 0
    )

    occupy_days = (
        item.occupy_time - (now - b.occupied_date).days
        if b.on_occupied_state and b.occupied_date else 0
    )

    db.close()

    return jsonify(
        success=True,
        name=item.name,
        booked_on=b.booked_date.isoformat(),
        hold_state=b.on_hold_state,
        hold_days=hold_days,
        occupied_state=b.on_occupied_state,
        occupied_days=occupy_days,
    )

@app.route("/library/validation")
def oauth_thing():
    item_id = request.args.get("id")
    if not (item_id):
        flash("Invalid request")
        return redirect("/library")
    
    session['id'] = item_id

    redirect_uri = url_for('auth_callback',_external = True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/library/auth/callback')
def auth_callback():
    token = oauth.google.authorize_access_token()
    user = token['userinfo']

    # session['user'] = {
    #     'id': user['sub'],
    #     'email': user['email'],
    #     'name': user['name'],
    #     'picture': user['picture']
    # }

    email = user.get('email')
    verified = user.get("email_verified", False)
    
    if email.endswith('@pcampus.edu.np') and verified:
        session['email'] = email
        return redirect('/library/final_validation')
    if not email.endswith("@pcampus.edu.np"):
        flash("Please use the official Pulchowk Campus Mail")
        session['email'] = None
        session['id'] = None
        return redirect('/library')


@app.route("/library/final_validation")
def validate():
    ''' Validates the items and email'''

    item_id = session.get("id")
    email = session.get('email')

    if not (item_id and email):
        flash("Invalid request")
        return redirect("/library")

    db = get_db()
    item = item_by_id(db, item_id)

    if not item or not item.available:
        db.close()
        flash("Item not available")
        return redirect("/library")

    booking = Booking(
        user_email=email,
        booked_date=datetime.utcnow(),
        item=item
    )

    item.available = False
    hold_time = item.hold_time

    db.add(booking)
    db.commit()
    db.close()

    flash(
        f"Item held successfully. "
        f"Collect within {hold_time} days.",
        "info"
    )

    return redirect("/library")


# @app.route("/validation",methods=["GET","POST"])
# def validate():
#     global items

#     ''' Validates the items and email'''
#     # ----------------------------------------------------------
#     # get request -> renders the actual validation page
#     # post request -> data validation (like otp and stuff) for validation,
#     # later i will implement other valiations like (does item exists or is available and some stuff)

#     # right now i am sending a successfully validated page thing


#     # if request.method == 'GET':
#     #     
#     #     # return "VALIDATION IMPLEMENTED BY AVI DAI"
#     #     pass
    
#     # 
#     # elif request.method == "POST":

#     # ----------------------------------

#     # if succesfully verified

#     item_id = request.args.get("id")
#     email = request.args.get("email")

#     if(not (item_id and email)):
#         flash("Error", "Wrong Request")
#         return redirect("/")

#     session_item = item_by_id(item_id)

#     if not session_item:
#         flash("Some Error Occured. Maybe the item is already taken",'error')
#         return redirect("/")


#         # check if availabel
#     if not session_item.available :
#         flash("Error You cannot book this item, since there is none available", 'error')

#     else:
#         # register a booking
#         _booking = Booking(email,datetime.now())
#         session_item.booking_ref = _booking

#         # decrement the availables
#         session_item.available = False

#         # commit those updated changes
#         save_data_base(items)
#         items = load_data_base() # TODO: remove?

#         flash(f"""Sucessfully done, your item is in a hold state, 
#                 please physically go and take it in {session_item.hold_time} days or will be redacted from holdings,
#                 also do note you must return ti > it.occuphe requested item after {session_item.occupy_time} days.
#                 Not doing will result this action to be mailed directly to the FSU. god knows what happens next.""",category='info')
    
#     return redirect("/")

# ---------------------------- 

# if __name__ == "__main__":
#     app.run(debug=True)
