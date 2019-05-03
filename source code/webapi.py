'''
ECE 568 Webapp Project
Team#1

Written by: Yuhang Zhou  yz853, Lichuan Ren  lr629
2019/5/1
'''
from flask import Flask
from flask import request, Response
from flask import render_template, jsonify, Blueprint
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Length
from flask_bootstrap import Bootstrap
from flask_docs import ApiDoc  # package to generate the api docs
from stockdata import realtime, history,history_json
from sim_trend import sim_trend
from query import query
from lstm import go
from svm import svm_model
from bayes import bayes_model
import time
import os

app = Flask(__name__)
app.config['API_DOC_MEMBER'] = ['api']
app.config['RESTFUL_API_DOC_EXCLUDE'] = []
ApiDoc(app)
api = Blueprint('api', __name__)

app.secret_key = 'dev'
bootstrap = Bootstrap(app)


class stockdataForm(FlaskForm):
    start = DateField(
        'Start date ( Year-month-day xxxx-xx-xx ) ', format='%Y-%m-%d')
    end = DateField('End date ( Year-month-day xxxx-xx-xx )',
                    format='%Y-%m-%d')
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
    ])  # 'value', 'view'
    submit = SubmitField()


class queryForm(FlaskForm):
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
    ])  # 'value', 'view'
    submit = SubmitField()

class predictForm(FlaskForm):
    strategy=SelectField('Prediction strategy',choices=[
        ('svm', 'SVM'),
        ('bayes', 'Bayesian curve fitting'),
    ])
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
    ])  # 'value', 'view'
    '''
    function = SelectField('Operation',choices=[
        ('train', 'Train'),
        ('test', 'Test'),
    ])
    '''
    length = DateField(
        'Date length')
    submit = SubmitField()

class lstmForm(FlaskForm):
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
    ])  # 'value', 'view'
    
    function = SelectField('Operation',choices=[
        ('test', 'Test'),
    ])
    #('train', 'Train'),
    
    term = SelectField('Term',choices=[
        ('SHORT', 'Short term'),
        ('LONG', 'Long term'),
    ])
    
    submit = SubmitField()


@app.route("/")
def home():
    return render_template('home.html')


@api.route("/stockdata", methods=['GET'])
def stockdata():
    """ 
    Stock data page (before request)

    The original page before user inputing data
    
    """
    form = stockdataForm()
    return render_template('stockdata.html',form=form)


@api.route("/stockdata", methods=['POST'])
def stockdata_post():
    """
    Stock data page (after request)

    @@@
    # args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    start_date    |    false    |    date   |    start date    |
    |    end_date    |    false    |    date   |    end date    |
    |    company    |    false    |    string   |    stock symbol    |
    # return
    | return |  type | remark |
    |--------|--------|--------|
    |    local_time   |    string   |    time to get get the realtime data    |
    |    price    |    float  |    realtime price    |
    |    volume    |    float   |    realtime volume    |
    |    fig_dict    |    string   |    address of saved history data figure     |
    |    data    |    2d list   |    data set of history data     |
    @@@
    """
    form = stockdataForm()
    start_date = request.form['start']
    end_date = request.form['end']
    company = request.form['company']
    price, volume, localtime = realtime(company)
    fig_dict, data = history(company, start_date, end_date)
    
    return render_template('stockdata.html',
     form=form, price=price, volume=volume, localtime=localtime,
     url=fig_dict, dynamic=time.time(), data=data)
    

@api.route("/stockdata/company=<company>&history", methods=['GET'])
def history_api(company):
    """
    history_data_api

    @@@
    # args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    company    |    false    |    string   |    stock symbol    |
    # return
    | return |  type | remark |
    |--------|--------|--------|
    |    data    |    json   |    data set of history data     |
    @@@
    """
    out = history_json(company)
    return out

@api.route("/stockdata/company=<company>&realtime", methods = ['GET'])
def realtime_api(company):
    """
    realtime_data_api

    @@@
    # args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    company    |    false    |    string   |    stock symbol    |
    # return
    | return |  type | remark |
    |--------|--------|--------|
    |    local_time   |    string   |    time to get get the realtime data    |
    |    price    |    float  |    realtime price    |
    |    volume    |    float   |    realtime volume    |
    
    @@@
    """
    price, volume, localtime = realtime(company)
    return "{},{},{},{}".format(company, price, volume, localtime)

@api.route("/predict", methods=['GET'])
def predict():
    """ 
    Prediction page (before request)

    The original page before user inputing data
    
    """
    form = predictForm()
    return render_template('predict.html',form=form)


@api.route("/predict", methods=['POST'])
def predict_post():
    """
    Predcition page

    @@@
    # args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    company    |    false    |    string   |    stock symbol    |
    |    date length    |    false    |    int   |    the date length for prediction   |
    # return
    | return |  type | remark |
    |--------|--------|--------|
    |    pred   |    list   |    predicted results    |

    @@@
    """
    form = predictForm()
    strategy=request.form['strategy']
    company = request.form['company']
    
    length = request.form['length']
    if strategy == 'bayes':
        pred = bayes_model(company, int(length))
    elif strategy == 'svm':
        pred = svm_model(company, int(length))
    pred=pred.tolist()
    return render_template('predict.html',form=form,pred=pred,dynamic=time.time(),strategy=strategy)


@api.route("/findsim", methods=['GET'])
def findsim():
    form = stockdataForm()
    return render_template('findsimilar.html', form=form)


@api.route("/findsim", methods=['POST'])
def findsim_post():
    """
    Trend finder page (after request)

    @@@
    # args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    start_date    |    false    |    date   |    start date    |
    |    end_date    |    false    |    date   |    end date    |
    |    company    |    false    |    string   |    stock symbol    |
    # return
    | return |  type | remark |
    |--------|--------|--------|
    |    sim_start   |    string   |    start date of the found interval   |
    |    sim_end    |    string  |    end date of the found interval    |
    |    fig_dict    |    string   |    address of saved trend figure     |
    @@@
    
    """
    form = stockdataForm()
    start_date = request.form['start']
    end_date = request.form['end']
    company = request.form['company']
    fig_dict, sim_start, sim_end = sim_trend(company, start_date, end_date)
    
    return render_template('findsimilar.html',form=form,
     sim_start=sim_start,sim_end=sim_end,
     url=fig_dict, dynamic=time.time())

@api.route("/query", methods=['GET'])
def query_page():
    form = queryForm()
    return render_template('query.html', form=form)

@api.route("/query", methods=['POST'])
def query_page_post():
    form = queryForm()
    selected_company = request.form['company']
    all_realtime,history_data,less_list=query(selected_company)
    return render_template('query.html', form=form,
     all_realtime=all_realtime, history_data=history_data,
     less_list=less_list,selected_company=selected_company)



@api.route("/lstm", methods=['GET'])
def lstm():
    """ 
    Prediction page (before request)

    The original page before user inputing data
    
    """
    form = lstmForm()
    return render_template('lstm.html',form=form)


@api.route("/lstm", methods=['POST'])
def lstm_post():
    """
    Predcition page

    @@@
    # args

    | args | nullable | type | remark |
    |--------|--------|--------|--------|
    |    company    |    false    |    string   |    stock symbol    |
    |    date length    |    false    |    int   |    the date length for prediction   |
    # return
    | return |  type | remark |
    |--------|--------|--------|
    |    pred   |    list   |    predicted results    |

    @@@
    """
    form = lstmForm()
    
    company = request.form['company']
    function=request.form['function']
    term = request.form['term']
    
    pred=go(company, function, term)
    pred=pred.tolist()
    #filename=go(company,function)
    return render_template('lstm.html',form=form,pred=pred,dynamic=time.time())





app.register_blueprint(api, url_prefix='/api')
# app.register_blueprint(platform, url_prefix='/platform')
if __name__ == "__main__":
    app.run(debug=1, port=5500)
