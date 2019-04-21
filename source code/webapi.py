from flask import Flask
from flask import request
from flask import render_template
from flask import Response
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,DateField,SelectField
from wtforms.validators import DataRequired, Length
from flask_bootstrap import Bootstrap
from HW3demo import pred
from stockdata import realtime,history
import time

app = Flask(__name__)
app.secret_key = 'dev'
bootstrap = Bootstrap(app)


def add(x):
    return int(x)+10


class stockdataForm(FlaskForm):
    start = DateField('Start date ( Year-month-day xxxx-xx-xx )', format='%Y-%m-%d')
    end = DateField('End date ( Year-month-day xxxx-xx-xx )', format='%Y-%m-%d')
    company = SelectField('Company', choices=[
        ('aaba', 'Altaba'), 
        ('aapl', 'Apple'),
        ('amd', 'AMD'),
        ('amzn', 'Amazon'),
        ('goog', 'Google'),
        ('intc', 'Intel'),
        ('nvda', 'Nvida'),
        ('qcom', 'Qualcomm'),
        ('tsla', 'Tesla'),
        ('xlnx', 'Xlinx')
    ])  #'value', 'view'
    submit = SubmitField()


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/stockdata", methods=['GET'])
def stockdata():
    form = stockdataForm()
    return render_template('stockdata.html',form=form)


@app.route("/stockdata", methods=['POST'])
def stockdata1():
    form = stockdataForm()
    start_date = request.form['start']
    end_date = request.form['end']
    company = request.form['company']
    price, volume, localtime = realtime(company)
    fig_dict, data = history(company, start_date, end_date)
    
    return render_template('stockdata.html',
     form=form, price=price, volume=volume, localtime=localtime,
     url=fig_dict, dynamic=time.time(), data=data)


@app.route("/predict", methods=['GET', 'POST'])
def predict():
    return render_template('predict.html')


@app.route("/findsim", methods=['GET'])
def findsim():
    form = stockdataForm()
    return render_template('findsimilar.html', form=form)


@app.route("/findsim", methods=['POST'])
def findsim1():
    form = stockdataForm()
    start_date = request.form['start']
    end_date = request.form['end']
    company = request.form['company']
    price, volume, localtime = realtime(company)
    fig_dict, data = history(company, start_date, end_date)
    
    return render_template('findsimilar.html',
     form=form, price=price, volume=volume, localtime=localtime,
     url=fig_dict, dynamic=time.time(), data=data)


if __name__ == "__main__":
    app.run(debug=1, port=5500)
