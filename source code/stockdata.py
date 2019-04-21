from pandas_datareader import data as pdr
import datetime
import time
import numpy as np
import matplotlib.pyplot as plt
import csv


def realtime(company):
    stock = pdr.get_quote_yahoo(company)
    price = stock['price'][0]
    volume = stock['regularMarketVolume'][0]
    localtime = str(time.strftime("%Y-%m-%d %H:%M:%S",
                                  time.localtime()))  # record time
    # localtime=lt[0:4]+lt[5:7]+lt[8:10]+lt[11:13]+lt[14:16]+lt[17:19]
    return price, volume, localtime


def history(company, start_date, end_date):
    start_date = start_date[0:4] + start_date[5:7] + start_date[8:10]
    end_date = end_date[0:4] + end_date[5:7] + end_date[8:10]
    price = []
    data = []
    volume = []
    day = []
    days=0
    #headers = ['Date', 'High', 'Low', 'Open', 'Close', 'Volume', 'Adjclose']
    with open('dataset/{}.csv'.format(company)) as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            date = row[0][0:4] + row[0][5:7] + row[0][8:10]
            if date >= start_date and date <= end_date:
                price.append(float(row[1]))
                volume.append(float(row[5]))
                day.append(days)
                days += 1
                data.append(row)
    price = np.array(price)
    volume = np.array(volume)
    day = np.array(day)
    fig = plt.figure(figsize=(10, 12))
    plt.subplot(2, 1, 1)
    plt.plot(day, price, c="r", label="Highest price")
    plt.legend(loc=2)
    plt.subplot(2, 1, 2)
    plt.plot(day, volume, c="b", label="Volume")
    plt.legend(loc=2)
    fig_dict = "static\images\history.png"
    fig.savefig("static\images\history.png")
    return fig_dict, data


start_date = '2015-10-01'
end_date = '2018-01-01'
company = 'aapl'





