#!/usr/bin/python

# Linear regression analysis for Yahoo Finance historical data
# Jason Fowler

# Sample url for obtaining historical data for Apple from Yahoo:
# http://ichart.finance.yahoo.com/table.csv?s=AAPL&a=00&b=01&c=2014&d=04&e=12&f=2014&g=d

# Change the file in symbols = line.strip...


import datetime
import csv
import os
import sys
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
        db = sqlite3.connect("db/"+symbol)
        c = db.cursor()
        c.execute("insert into stockhistory (ydate, closeprice, volume) values (?, ?, ?)", (row[0], row[4], row[5]))
        db.commit()
    except csv.Error, e:
      print e

def createDb(symbol):
  db = sqlite3.connect("db/"+symbol)
  c = db.cursor()
  try:
    c.execute("create table stockhistory (id integer not null primary key, ydate text, closeprice float, volume integer)")
  except sqlite3.OperationalError:
    print symbol+": already used"


shutil.rmtree("db")
os.makedirs("db")

#test
#symbols = [line.strip() for line in open('symbols-sml.txt')]
#prod
symbols = [line.strip() for line in open('symbols1.txt')]
for symbol in symbols:
  createDb(symbol)
  getStocks(symbol)
time.sleep(300)
symbols = [line.strip() for line in open('symbols2.txt')]
for symbol in symbols:
  createDb(symbol)
  getStocks(symbol)
time.sleep(300)
symbols = [line.strip() for line in open('symbols3.txt')]
for symbol in symbols:
  createDb(symbol)
  getStocks(symbol)
time.sleep(300)
symbols = [line.strip() for line in open('symbols4.txt')]
for symbol in symbols:
  createDb(symbol)
  getStocks(symbol)
time.sleep(300)
symbols = [line.strip() for line in open('symbols5.txt')]
for symbol in symbols:
  createDb(symbol)
  getStocks(symbol)
time.sleep(300)
symbols = [line.strip() for line in open('symbols6.txt')]
for symbol in symbols:
  createDb(symbol)
  getStocks(symbol)
time.sleep(300)
symbols = [line.strip() for line in open('symbols7.txt')]
for symbol in symbols:
  createDb(symbol)
  getStocks(symbol)
time.sleep(300)
symbols = [line.strip() for line in open('symbols8.txt')]
for symbol in symbols:
  createDb(symbol)
  getStocks(symbol)
time.sleep(300)
symbols = [line.strip() for line in open('symbols9.txt')]
for symbol in symbols:
  createDb(symbol)
  getStocks(symbol)
time.sleep(300)
symbols = [line.strip() for line in open('symbols10.txt')]


