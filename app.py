######################
#   app.py -> Contains server code
######################

from flask import Flask, render_template
import models

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html',items = items)

if __name__ == "__main__":
    # models.fill_test_data()
    items = models.load_data_base()
    app.run(debug=True)
