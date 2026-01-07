######################
#   app.py -> Contains server code
######################

from flask import Flask, render_template, request
import models

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html',items = items)

@app.route("/validation",methods=["GET","POST"])
def validate():
    ''' Validates the items and email'''

    # get request -> renders the actual validation page
    # post request -> data (like otp and stuff) for validation,

    # right now i am sending a successfully validated page thing


    # if request.method == 'GET':
    #     
    #     # return "VALIDATION IMPLEMENTED BY AVI DAI"
    #     pass
    
    # 
    # elif request.method == "POST":

    # if succesfully verified
    user_id = request.args.get("id")
    email = request.args.get("email")

    print(user_id,email)
    return 'hi'
     



if __name__ == "__main__":
    # models.fill_test_data()
    items = models.load_data_base()
    app.run(debug=True)
