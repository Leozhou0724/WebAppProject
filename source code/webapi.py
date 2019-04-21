from flask import Flask
from flask import request
from flask import render_template
from flask import Response
from flask_bootstrap import Bootstrap
from HW3demo import pred
import time

app = Flask(__name__)
bootstrap=Bootstrap(app)

def add(x):
    return int(x)+10


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/stockdata", methods=['GET'])
def stockdata():
    return render_template('stockdata.html')


@app.route("/stockdata", methods=['POST'])
def stockdata1():
    x = request.form['x']
    y = request.form['y']
    result, fig_dict = pred(x)
    result=add(x)
    return render_template('stockdata.html', result=result, x=x, y=y, url=fig_dict, dynamic=time.time())


@app.route("/predict", methods=['GET', 'POST'])
def predict():
    return render_template('predict.html')


@app.route("/findsim", methods=['GET', 'POST'])
def findsim():
    return render_template('findsimilar.html')


if __name__ == "__main__":
    app.run(debug=1)
