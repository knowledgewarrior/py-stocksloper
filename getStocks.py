#!/usr/bin/python

# Linear regression analysis for Yahoo Finance historical data
# Jason Fowler

# Sample url for obtaining historical data for Apple from Yahoo:
# http://ichart.finance.yahoo.com/table.csv?s=AAPL&a=00&b=01&c=2014&d=04&e=12&f=2014&g=d

# Change the file in symbols = line.strip...


import datetime
import csv
import os
import urllib2
import StringIO
import sqlite3
import shutil


def getStocks(symbol):
  start_date = datetime.datetime.now().date() + datetime.timedelta(-709)
  now_date = datetime.datetime.now().date()
  start_y,start_m,start_d = str(start_date).split('-')
  start_m = int(start_m) -1
  now_y,now_m,now_d = str(now_date).split('-')
  now_m = int(now_m) -1
  yurl = "http://ichart.finance.yahoo.com/table.csv?s=%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s&g=d" % (symbol, start_m, start_d, start_y, now_m, now_d, now_y)
  try:
    yresponse = urllib2.urlopen(yurl)
  except:
    yresponse = False
  else:
    ycr = csv.reader(yresponse)
    ycr.next()
    db = sqlite3.connect("db/"+symbol)
    c = db.cursor()
    c.execute("create table stockhistory (id integer not null primary key, ydate text, closeprice float, volume integer);")
    for row in ycr:
      try:
        close = row[4]
      except:
        close = False
      else:
        try:
          volume = row[5]
        except:
          volume = False
        else:
          yadate = row[0]
          c.execute('''insert into stockhistory(ydate,closeprice,volume)
            values(?,?,?)''', (yadate,close,volume))
          db.commit()

shutil.rmtree("db")
os.makedirs("db")

symbols = [line.strip() for line in open('symbols-sml.txt')]
for symbol in symbols:
  getStocks(symbol)
