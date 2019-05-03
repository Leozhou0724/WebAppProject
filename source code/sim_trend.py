'''
ECE 568 Webapp Project
Team#1

Written by: Haofan Zhang  hz332
2019/5/1
'''
import numpy as np
import matplotlib.pyplot as plt
import csv
from math import sqrt


def multipl(a, b):
    sumofab = 0.0
    for i in range(len(a)):
        temp = a[i]*b[i]
        sumofab += temp
    return sumofab


def corrcoef(x, y):
    n = len(x)
    # 求和
    sum1 = sum(x)
    sum2 = sum(y)
    # 求乘积之和
    sumofxy = multipl(x, y)
    # 求平方和
    sumofx2 = sum([pow(i, 2) for i in x])
    sumofy2 = sum([pow(j, 2) for j in y])
    num = sumofxy-(float(sum1)*float(sum2)/n)
    # 计算皮尔逊相关系数
    den = sqrt((sumofx2-float(sum1**2)/n)*(sumofy2-float(sum2**2)/n))
    return num/den


def sim_trend(company, start_date, end_date):
    start_date_str = start_date
    end_date_str=end_date
    start_date = start_date[0:4] + start_date[5:7] + start_date[8:10]
    end_date = end_date[0:4] + end_date[5:7] + end_date[8:10]

    part_price = []
    total_dates = []
    total_price = []
    part_day = []
    part_dates = []
    part_days = 0
    total_days = 0
    with open('dataset/{}.csv'.format(company)) as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            date = row[0][0:4] + row[0][5:7] + row[0][8:10]
            total_dates.append(date)
            total_days += 1
            total_price.append(float(row[4]))

            if date >= start_date and date <= end_date:
                part_price.append(float(row[4]))
                part_day.append(part_days)
                part_days += 1
                part_dates.append(date)
                


    for i in range(0, total_days-part_days):

        simi_price = total_price[i:i+part_days]

        testday = total_dates[0:part_days]
        final = corrcoef(simi_price, part_price)
        if final >= 0.75:
            break
    testday = part_day[0:part_days]
    extra_day = range(part_days-1,part_days+10)
    extra_price=total_price[i+part_days-1:i+part_days+10]
    

    sim_start = '{}-{}-{}'.format(total_dates[i+1][0: 4],
                                  total_dates[i+1][4: 6], total_dates[i+1][6: 8])

    sim_end = '{}-{}-{}'.format(total_dates[i + part_days][0: 4],
                                total_dates[i + part_days][4: 6], total_dates[i + part_days][6: 8])
    fig = plt.figure(figsize=(10, 20))
    plt.subplot(3, 1, 1)
    plt.plot(testday, part_price, c="b", label="Input trend")
    plt.title('{} to {}'.format(start_date_str, end_date_str),fontsize=20)
    plt.legend(loc=2)
    plt.subplot(3, 1, 2)
    plt.plot(testday, simi_price, c="r", label="similar trend")
    plt.title('{} to {}'.format(sim_start,sim_end),fontsize=20)
    plt.legend(loc=2)
    plt.subplot(3, 1, 3)
    plt.plot(testday, simi_price, c="r", label="similar trend")
    plt.plot(extra_day, extra_price, c="g", label="reference: 10 days later")
    plt.title('10 days trend after {}'.format(sim_end),fontsize=20)
    plt.legend(loc=2)
    
    fig_dict = "static\images\simtrend.png"
    fig.savefig("static\images\simtrend.png")

    return fig_dict, sim_start,sim_end



start_date = '2018-03-18'
end_date = '2018-04-18'
company = 'aapl'

