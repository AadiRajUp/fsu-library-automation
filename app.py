######################
#   app.py -> Contains server code
#
#####################

from flask import Flask, render_template
import models

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html')

app.run(debug=True)
