This program is written in Python 3.7
The database is MySQL 8.0

Packages used in programs:
	from pandas_datareader import data as pdr
	import datetime
	import pymysql
	import time
	
The pandas_datareader is for getting data from Yahoo Finance API, version should be 0.7.0 (Other versions may not be compatible with Yahoo API)
The pymysql is for operating in MySQL database, version 0.9.3

The program is divided into 2 files
pahse1.py for collecting history data
phase1realtime.py for collecting realtime data

Before running, Line 18 of phase1.py and Line 16 of phase1realtime.py needs to be changed to your own local database information
	db=pymysql.connect("localhost","root","password","database name")
	if you are using local database, leave the "localhost" there
	root is the default username, change to your username if you haved changed that
	change the "password" to your own database password
	create a database and replace the "database name" with its name
	
In both files, there are three steps inside
	1.create tables, you cannot create duplicated tables if you have created in the first time running
	2.collecting data, you cannot collecting duplicated data because the primary key is the date. It's fine for the realtime data, because the primary key is real time
	3.export data into csv files, only run this part after all the needed data is collected, you can run this part individually for the realtime file, because realtime data colltion takes long time
	  export file name: history data "stockname.csv", realtime data "stockname+rt.csv" , output address: Mysqlserver/Data/databasename
	  