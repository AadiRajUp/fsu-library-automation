#----------------------------------------
#   app.py -> Contains server code
#----------------------------------------

from flask import Flask, render_template, request, redirect, flash, session
from flask_cors import CORS
import models

app = Flask(__name__)
CORS(app)
app.secret_key = "blahblah22"

# --------------------
# Helper Functions
# --------------------

def item_by_id(id:int) -> models.Item | None:
    ''' Returns the item having the attribute ID = `id` '''
    # TODO: change while making actual database
    try:
        id = int(id)
    except ValueError:
        return None
    
    for item in items:
        if item.id == id:
            return item
    return None
# ------------------------
# Routes
# ------------------------

@app.route("/")
def home():
    return render_template('index.html',items = items)


@app.route("/campusend",methods=['GET',"POST"])
def admin():
    ''' Interface visible for the FSU representative'''
    if request.method == "GET":
        return render_template("login.html")
    
    elif request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        if not (username and password):
            flash("Please enter something")
            return redirect('/campusend')

        #TODO: work on more robust method of verification
        if username == "ram" and password == 'hari':
            session['logged_in'] = True
            return redirect('/arena')
        else:
            flash("Wrong username or password")
            return redirect('/campusend')

@app.route("/arena")
def admin_dashboard():
    if not session.get('logged_in'):
        flash("You are not authenticated")
        return redirect('/campusend')
    
    return 'wow'
    


@app.route("/info", methods=['GET'])
def info():
    
    def date_as_string(datetime_obj : models.datetime):
        return datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
    
    ''' Returns the information about a certain item (How much time for hold-clearing and stuffs)'''
    item_id = request.args.get("id")

    if item_id:
        _ctx_item = item_by_id(item_id)
        _booking_ref = _ctx_item.booking_ref

        if not _booking_ref:
            return {
                'success': True,
                'name': _ctx_item.name,
                "booked_on":"Not Booked, Available",
                "hold_state": 0,
                "hold_days":0,
                "occupied_state":0,
                "occupied_days": 0,
            }
        
        _booked_on = _booking_ref.booked_time
        is_on_hold =_booking_ref.on_hold_state
        is_on_occupy = _booking_ref.on_occupied_state
        hold_days = _ctx_item.hold_time -( (models.datetime.now() - _booked_on).days)
        
        if is_on_occupy:
            occupy_days = _ctx_item.occupy_time - ((models.datetime.now() - _booking_ref.occupy_time)).days
        else:
            occupy_days = 0

        return {
            'success': True,
            "name" : _ctx_item.name,
            "booked_on": date_as_string(_booked_on),
            "hold_state": is_on_hold,
            "hold_days":hold_days if is_on_hold else 0,
            "occupied_state": is_on_occupy,
            "occupied_days": occupy_days,
        }       
    else:
        return {'success':False}


@app.route("/validation",methods=["GET","POST"])
def validate():
    global items

    ''' Validates the items and email'''
    # ----------------------------------------------------------
    # get request -> renders the actual validation page
    # post request -> data validation (like otp and stuff) for validation,
    # later i will implement other valiations like (does item exists or is available and some stuff)

    # right now i am sending a successfully validated page thing


    # if request.method == 'GET':
    #     
    #     # return "VALIDATION IMPLEMENTED BY AVI DAI"
    #     pass
    
    # 
    # elif request.method == "POST":

    # ----------------------------------

    # if succesfully verified

    item_id = request.args.get("id")
    email = request.args.get("email")

    if(not (item_id and email)):
        flash("Error", "Wrong Request")
        return redirect("/")

    session_item = item_by_id(item_id)

    if not session_item:
        flash("Some Error Occured. Maybe the item is already taken",'error')
        return redirect("/")


        # check if availabel
    if not session_item.available :
        flash("Error You cannot book this item, since there is none available", 'error')

    else:
        # register a booking
        _booking = models.Booking(email,models.datetime.now())
        session_item.booking_ref = _booking

        # decrement the availables
        session_item.available = False

        # commit those updated changes
        models.save_data_base(items)

        flash(f"""Sucessfully done, your item is in a hold state, 
                please physically go and take it in {session_item.hold_time} days or will be redacted from holdings,
                also do note you must return the requested item after {session_item.occupy_time} days.
                Not doing will result this action to be mailed directly to the FSU. god knows what happens next.""",category='info')
    
    return redirect("/")

# ---------------------------- 

if __name__ == "__main__":
    models.fill_test_data()
    items = models.load_data_base()
    app.run(debug=True)
