#Web app project phase collecting data
#Team 1
#Yuhang Zhou	yz853
#Jiachen Ding	jd1287
#Lichuan Ren	lr629
#Haofan Zhang	hz332
#2019/3/7

#this file is for collecting history data
from pandas_datareader import data as pdr
import datetime
import pymysql
#time range of collection
start=datetime.datetime(2018,1,1)
end=datetime.datetime(2019,1,31)

#connect to your local database, need to change to your own database information before running
db=pymysql.connect("localhost","root","zyh69724hh","test")   #localhost , username, password, datebase

#the symbols of stocks
symbol=['aapl','goog','aaba','amd','nvda','amzn','qcom','intc','xlnx','tsla']



for n in range(10):
    company=symbol[n]

    #this part is for create tables, don't run this part again if tables are already created
    cursor1=db.cursor()
    create="create table {}(Date date,High float,Low float,Open float,Close float,Volume int,AdjClose float,primary key(Date))".format(company)
    cursor1.execute(create)
    db.commit()


    #collect history data and insert them into the tables
    stock=pdr.DataReader(company,'yahoo',start,end)
    cursor=db.cursor()
    for i in range(stock.index.size):
        timechar=str(stock.index[i])[0:10]
        timechar=timechar[0:4]+timechar[5:7]+timechar[8:10]             #adjust the format into the sql input format
        cmd="insert into {}(Date,High,Low,Open,Close,Volume,AdjClose) values({},{},{},{},{},{},{})".format(company,timechar,\
            stock.loc[stock.index[i],'High'],stock.loc[stock.index[i],'Low'],\
                stock.loc[stock.index[i],'Open'],stock.loc[stock.index[i],'Close'],\
                    stock.loc[stock.index[i],'Volume'],stock.loc[stock.index[i],'Adj Close'])
        cursor.execute(cmd)

    db.commit()

#this part is for exporting data into csv file, the default address is Mysqlserver/Data/databasename folder
for n in range(10):
    company=symbol[n]
    cursor2=db.cursor()
    export="select * from {} into outfile '{}.csv' fields terminated by ','".format(company,company)
    cursor2.execute(export)
db.commit()

db.close()





