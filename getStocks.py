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
import time


def getStocks(symbol):
  start_date = datetime.datetime.now().date() + datetime.timedelta(-709)
  now_date = datetime.datetime.now().date()
  start_y,start_m,start_d = str(start_date).split('-')
  start_m = int(start_m) -1
  now_y,now_m,now_d = str(now_date).split('-')
  now_m = int(now_m) -1

  db = sqlite3.connect("db/"+symbol)
  c = db.cursor()
  c.execute("create table stockhistory (id integer not null primary key, ydate text, closeprice float, volume integer)")

  yurl = "http://ichart.finance.yahoo.com/table.csv?s=%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s&g=d" % (symbol, start_m, start_d, start_y, now_m, now_d, now_y)
  req = urllib2.Request(yurl)
  try:
    resp = urllib2.urlopen(req)
  except urllib2.URLError, e:
    if e.code > 399:
      return
  else:
    try:
      ycr = csv.reader(resp)
      ycr.next()
      for row in ycr:
        #print row[0],row[5],row[4]
        c.execute("insert into stockhistory (ydate, closeprice, volume) values (?, ?, ?)", (row[0], row[5], row[4]))
        db.commit()
    except csv.Error, e:
      print e

shutil.rmtree("db")
os.makedirs("db")

#prod
symbols = [line.strip() for line in open('symbols1.txt')]
for symbol in symbols:
  getStocks(symbol)
time.sleep(3600)
symbols = [line.strip() for line in open('symbols2.txt')]
for symbol in symbols:
  getStocks(symbol)
time.sleep(3600)
symbols = [line.strip() for line in open('symbols3.txt')]
for symbol in symbols:
  getStocks(symbol)

# test
# symbols = [line.strip() for line in open('symbols-test-1.txt')]
# for symbol in symbols:
#   getStocks(symbol)
# time.sleep(5)
# symbols = [line.strip() for line in open('symbols-test-2.txt')]
# for symbol in symbols:
#   getStocks(symbol)

# End of file
