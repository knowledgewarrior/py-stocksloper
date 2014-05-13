import datetime
import csv
import os
import urllib2
import StringIO
import sqlite3
import shutil

shutil.rmtree("db")
os.makedirs("db")

#test
start_date = datetime.datetime.now().date() + datetime.timedelta(-199)
#prod
#start_date = datetime.datetime.now().date() + datetime.timedelta(-709)
now_date = datetime.datetime.now().date()
start_y,start_m,start_d = str(start_date).split('-')
now_y,now_m,now_d = str(now_date).split('-')

#prod
symbols = [line.strip() for line in open('symbols-med.txt')]
for symbol in symbols:
  db = sqlite3.connect("db/"+symbol)
  c = db.cursor()
  c.execute("create table stockhistory (id integer not null primary key, ydate text, closeprice float, volume integer);")
  db.commit()

  from urllib2 import Request, urlopen, URLError, HTTPError
  yurl = "http://ichart.finance.yahoo.com/table.csv?s=%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s&g=d" % (symbol, start_m, start_d, start_y, now_m, now_d, now_y)
  try:
    yresponse = urllib2.urlopen(yurl)
  except HTTPError, e:
      # print 'The server couldn\'t fulfill the request.'
      # print 'Error code: ', e.code
  except URLError, e:
      # print 'We failed to reach a server.'
      # print 'Reason: ', e.reason
  else:
    ycr = csv.reader(yresponse)
    ycr.next()
    for row in ycr:
      yadate = row[0]
      close = row[4]
      volume = row[5]
      c.execute('''insert into stockhistory(ydate,closeprice,volume)
        values(?,?,?)''', (yadate,close,volume))
      db.commit()