#Web app project phase collecting data
#Team 1
#Yuhang Zhou	yz853
#Jiachen Ding	jd1287
#Lichuan Ren	lr629
#Haofan Zhang	hz332
#2019/3/7

#this file is for collecting realtime data
from pandas_datareader import data as pdr
import datetime
import pymysql
import time

#connect to your local database, need to change to your own database information before running
db=pymysql.connect("localhost","root","zyh69724hh","realtime") #localhost , username, password, datebase

symbol=['aapl','goog','aaba','amd','nvda','amzn','qcom','intc','xlnx','tsla']

#create tables, it needs to create tables once before collecting data and inserting into tables
'''
for n in range(10):
    company=symbol[n]
    cursor1=db.cursor()
    create="create table {}rt (Time datetime,Price float,Volume int,primary key(Time))".format(company)
    cursor1.execute(create)
    db.commit()

db.close()
'''

#collecting realtime data
while 1:
    start=time.clock()
    
    for n in range(10):
        company=symbol[n]
        stock=pdr.get_quote_yahoo(company)
        price=stock['price']
        volume=stock['regularMarketVolume']                                     #get data
        lt=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))            #record time
        localtime=lt[0:4]+lt[5:7]+lt[8:10]+lt[11:13]+lt[14:16]+lt[17:19]        #adjust the format into the sql format

        cursor=db.cursor() 
        cmd="insert into {}rt(Time,Price,Volume) values({},{},{})".format(company,localtime,price[0],volume[0])
        cursor.execute(cmd)
    db.commit()
    
    print(lt)
    apple=pdr.get_quote_yahoo('aapl')
    print(apple['price'][0],'  ',apple['regularMarketVolume'][0])       #just for detecting the process
    
    end=time.clock()
    runtime=end-start
    time.sleep(60-runtime)          #the run time of this program needs to be added into the time gap
    
#export tables
'''
for n in range(10):
    company=symbol[n]
    cursor2=db.cursor()
    export="select * from {}rt into outfile '{}rt.csv' fields terminated by ','".format(company,company)
    cursor2.execute(export)
db.commit()
'''
db.close()
