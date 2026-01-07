#----------------------------------------
#   app.py -> Contains server code
#----------------------------------------

from flask import Flask, render_template, request, redirect, flash
import models

app = Flask(__name__)

# --------------------
# Helper Functions
# --------------------

def item_by_id(id:int) -> models.Item:
    ''' Returns the item having the attribute ID = `id` '''
    # TODO: change while making actual database
    for item in items:
        if item.id == id:
            return item
        
# ------------------------
# Routes
# ------------------------

@app.route("/")
def home():
    return render_template('index.html',items = items)

@app.route("/validation",methods=["GET","POST"])
def validate():
    ''' Validates the items and email'''
    # ----------------------------------------------------------
    # get request -> renders the actual validation page
    # post request -> data validation (like otp and stuff) for validation,
    # later i will implement other valiations like (does item exists and some stuff)

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

    session_item = item_by_id(item_id)

    # register a booking
    _booking = models.Booking(email,models.datetime.now())
    session_item.booking_ref = _booking

    flash(f"Sucessfully done, your item is in a hold state, please physically go and take it in {session_item.hold_time} days or will be redacted from holdings, also do note you must return the requested item after {session_item.occupy_time} days. Not doing will result this action to be mailed directly to the FSU. god knows what happens next.")
    return redirect("/")

# ---------------------------- 

if __name__ == "__main__":
    # models.fill_test_data()
    items = models.load_data_base()
    app.run(debug=True)
