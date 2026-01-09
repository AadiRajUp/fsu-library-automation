#----------------------------------------
#   app.py -> Contains server code
#----------------------------------------

from flask import Flask, render_template, request, redirect, flash, session, jsonify
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

@app.route('/user-bookings',methods=["POST"])
def user_history():
    ''' When user wants to see all of the stuff they have booked for an email. '''
    if not request.method == "POST":
        flash("Wrong Method")
        return redirect("/")
    
    email = request.form.get("email")
    
    if not email:
        flash("Email is required")
        return redirect("/")
    
    all = []
    for it in items:
        temp = []
        if it.booking_ref and it.booking_ref.user_email == email:
            
            # will in the following order
            # ID, NAME, BOOK_DATE, HOLD_TIME_REMAINING, BOOK_TIME_REMAINING
            temp.append(it.id)
            temp.append(it.name)

            # TODO: remove this verbosity

            _booking_ref = it.booking_ref

            temp.append(_booking_ref.booked_date)

            _booked_on = _booking_ref.booked_date
            is_on_hold =_booking_ref.on_hold_state
            is_on_occupy = _booking_ref.on_occupied_state
            hold_days = it.hold_time -( (models.datetime.now() - _booked_on).days)
        
            if is_on_occupy:
                occupy_days = it.occupy_time - ((models.datetime.now() - _booking_ref.occupied_date)).days
            else:
                occupy_days = "NOT ON OCCUPY"

            temp.append(hold_days if is_on_hold else "NOT ON HOLD")
            temp.append(occupy_days)

            all.append(temp)
    
    return render_template("user_bookings.html",items=all)


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

@app.route('/own-item',methods=["POST"])
def own_item():
    ''' Change the state of the item from hold state to own state'''
    msg = {"success":False,'remarks':'none'}
   

    if not session.get('logged_in'):
        msg['remarks'] = "You are not authenticated"
        return msg
    
    if request.method != "POST":
        msg["remarks"] = "Wrong way to call this endpoint"
        return msg
    
    id = request.get_json().get("id")
    item = item_by_id(id)

    if not item:
        msg['remarks'] = "Wrong item referenced"
        return msg
    
    # change the hold state
    item.booking_ref.on_hold_state = False
    item.booking_ref.on_occupied_state = True
    item.booking_ref.occupied_date = models.datetime.now()

    msg["success"] = True
    
    return jsonify(msg)


@app.route("/arena")
def admin_dashboard():
    global items

    if not session.get('logged_in'):
        flash("You are not authenticated")
        return redirect('/campusend')
    
    # check for items that have passed their max hold date or max booked date
    today = models.datetime.now().day
   
    for it in items:
        if not it.booking_ref: continue

        if it.booking_ref.on_hold_state and ((today - it.booking_ref.booked_date.day) > it.hold_time):
            # hold time has passed, time to realease it 
            # TODO: something else behaviour for hold time?
            it.booking_ref = None
            it.available = True

            models.save_data_base(items)
        
        elif it.booking_ref.on_occupied_state and ((today - it.booking_ref.occupied_date.day )> it.occupy_time):
            # occupy time has passed, time to release it
            # TODO: something else behaviour in this case?
            it.booking_ref.is_expired = True

            # mail FSU?
            models.save_data_base(items)
            

    relevant_items = [item for item in items if not item.available and item.booking_ref.on_hold_state]
    items_modified = []

    # fill items_modified with all the required information
    for its in relevant_items:
        _temp = []

        # name 
        _temp.append(its.name)
        # photo
        _temp.append(its.image_path)
        # roll number (generate through mail, first 9 character)
        _temp.append(its.booking_ref.user_email[:9].upper())
        # book time
        _temp.append(its.booking_ref.booked_date)
        # id
        _temp.append(its.id)

        items_modified.append(_temp)

    return render_template('dashboard.html',items= items_modified)
    


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
        
        _booked_on = _booking_ref.booked_date
        is_on_hold =_booking_ref.on_hold_state
        is_on_occupy = _booking_ref.on_occupied_state
        hold_days = _ctx_item.hold_time -( (models.datetime.now() - _booked_on).days)
        
        if is_on_occupy:
            occupy_days = _ctx_item.occupy_time - ((models.datetime.now() - _booking_ref.occupied_date)).days
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
        items = models.load_data_base() # TODO: remove?

        flash(f"""Sucessfully done, your item is in a hold state, 
                please physically go and take it in {session_item.hold_time} days or will be redacted from holdings,
                also do note you must return ti > it.occuphe requested item after {session_item.occupy_time} days.
                Not doing will result this action to be mailed directly to the FSU. god knows what happens next.""",category='info')
    
    return redirect("/")

# ---------------------------- 

if __name__ == "__main__":
    # models.fill_test_data()
    items = models.load_data_base()
    app.run(debug=True)
