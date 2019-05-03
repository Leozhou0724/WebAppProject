'''
ECE 568 Webapp Project
Team#1

Written by: Yuhang Zhou  yz853
2019/5/1
'''
from stockdata import realtime
import numpy as np
import csv


def query(selected_company):
    company = ['aaba', 'aapl', 'amd', 'amzn', 'goog',
               'intc', 'nvda', 'qcom', 'tsla', 'xlnx']
    all_realtime = []
    for symbol in company:
        single_realtime = []
        single_realtime.append(symbol)
        price, volume, localtime = realtime(symbol)
        single_realtime.append(price)
        single_realtime.append(volume)
        all_realtime.append(single_realtime)
    #print(all_realtime)
    history_data = []
    for symbol in company:
        with open('dataset/{}.csv'.format(symbol)) as f:
            f_csv = csv.reader(f)
            price_10day = []
            price_1year = []
            single_history = []
            for row in f_csv:
                date = row[0][0:4] + row[0][5:7] + row[0][8:10]
                if date >= '20190405' and date <= '20190418':
                    price_10day.append(float(row[4]))
                if date >= '20180101' and date <= '20190101':
                    price_1year.append(float(row[4]))
        price_10day = np.array(price_10day)
        price_1year = np.array(price_1year)
        single_history.append(symbol)
        single_history.append(np.max(price_10day))
        single_history.append(np.average(price_1year))
        single_history.append(np.min(price_1year))
        if symbol == selected_company:
            selected_lowest = np.min(price_1year)
        history_data.append(single_history)
    #print(history_data)
    less_list = []
    for i in history_data:
        if i[1] < selected_lowest:
            less_list.append(i[0])
    #print(less_list)
    return all_realtime,history_data,less_list


