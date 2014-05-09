#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3

import sqlite3
import sys
import os

def getslope(symbol, ntd, slope):
    conn = sqlite3.connect('db/'+symbol)
    c = conn.cursor()
    for row in c.execute('select sum(id) as sumx, sum(closeprice) as sumy,'
        'sum(id * closeprice) as sumxy, sum(id * id) as sumxx from(select id,'
        'closeprice from stockhistory order by ydate desc limit ?);', (ntd,)):
        sumx = row[0]
        sumy = row[1]
        sumxy = row[2]
        sumxx = row[3]
        ntdsumxy = ntd * sumxy
        sumxsumy = sumx * sumy
        ntdsumxx = ntd * sumxx
        sumxsumx = sumx * sumx
        slope = (ntdsumxy - sumxsumy) / (ntdsumxx - sumxsumx)
        if -0.001 <= slope <= 0.001:
            # getcontext().prec = 64
            # print(Decimal(slope))
            '%.1f' % round(slope, 64)
            print(slope)
            return True
        elif -0.001 >= slope >= 0.001:
            ntd = ntd + 1
            return getslope(symbol, ntd, slope)
        else:
            c.close()
            conn.close()
            return False

from os import listdir
from os.path import isfile, join
from decimal import *
files = [ f for f in listdir('db') if isfile(join('db',f)) ]
#print(files)
for symbol in files:
    #print(f)
    ntd = 120
    slope = 1
    getslope(symbol, ntd, slope)

