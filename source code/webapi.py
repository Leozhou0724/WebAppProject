from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)


def add(x, y):
    return int(x) + int(y)


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
    result = add(x, y)
    return render_template('stockdata.html', result=result, x=x, y=y)


@app.route("/predict", methods=['GET', 'POST'])
def predict():
    return render_template('predict.html')


@app.route("/findsim", methods=['GET', 'POST'])
def findsim():
    return render_template('findsimilar.html')


if __name__ == "__main__":
    app.run(debug=1)
