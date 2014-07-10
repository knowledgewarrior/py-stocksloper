#!/usr/bin/python

import sqlite3
import sys
import os
import decimal

def float_to_decimal(f):
    # http://docs.python.org/library/decimal.html#decimal-faq
    "Convert a floating point number to a Decimal with no loss of information"
    n, d = f.as_integer_ratio()
    numerator, denominator = decimal.Decimal(n), decimal.Decimal(d)
    ctx = decimal.Context(prec=60)
    result = ctx.divide(numerator, denominator)
    while ctx.flags[decimal.Inexact]:
        ctx.flags[decimal.Inexact] = False
        ctx.prec *= 2
        result = ctx.divide(numerator, denominator)
    return result

def floater(number, sigfig):
    # http://stackoverflow.com/questions/2663612/nicely-representing-a-floating-point-number-in-python/2663623#2663623
    assert(sigfig>0)
    try:
        d=decimal.Decimal(number)
    except TypeError:
        d=float_to_decimal(float(number))
    sign,digits,exponent=d.as_tuple()
    if len(digits) < sigfig:
        digits = list(digits)
        digits.extend([0] * (sigfig - len(digits)))
    shift=d.adjusted()
    result=int(''.join(map(str,digits[:sigfig])))
    # Round the result
    if len(digits)>sigfig and digits[sigfig]>=5: result+=1
    result=list(str(result))
    # Rounding can change the length of result
    # If so, adjust shift
    shift+=len(result)-sigfig
    # reset len of result to sigfig
    result=result[:sigfig]
    if shift >= sigfig-1:
        # Tack more zeros on the end
        result+=['0']*(shift-sigfig+1)
    elif 0<=shift:
        # Place the decimal point in between digits
        result.insert(shift+1,'.')
    else:
        # Tack zeros on the front
        assert(shift<0)
        result=['0.']+['0']*(-shift-1)+result
    if sign:
        result.insert(0,'-')
    return ''.join(result)

def getslope(symbol, ntd, slope):
    conn = sqlite3.connect('db/'+symbol)
    c = conn.cursor()
    #print ntd,symbol,slope
    for row in c.execute('select sum(id) as sumx, sum(closeprice) as sumy,'
        'sum(id * closeprice) as sumxy, sum(id * id) as sumxx from(select id,'
        'closeprice from stockhistory order by ydate desc limit ?);', (ntd,)):
        ntdsumxy = ntd * row[2]
        sumxsumy = row[0] * row[1]
        ntdsumxx = ntd * row[3]
        sumxsumx = row[0] * row[0]
        slope = (ntdsumxy - sumxsumy) / (ntdsumxx - sumxsumx)
        slope = slope * -1.0
        if -0.001 <= slope <= 0.001:
            slope = floater(slope,32)
            for volrow in c.execute('select avg(volume) from stockhistory;'):
                avgvol = floater(volrow[0],8)
            for pricerow in c.execute('select closeprice from stockhistory order by ydate desc limit 1;'):
                price = pricerow[0]
            print >>f1, (symbol) + (",") + str(price) + (",") + str(slope) + (",") + str(avgvol)+ (",") + str(ntd)
            return True
        elif ntd <= 503:
            ntd += 1
            c.close()
            conn.close()
            return getslope(symbol, ntd, slope)
        else:
            return False

from os import listdir
from os.path import isfile, join
from decimal import *
files = [ f for f in listdir('db') if isfile(join('db',f)) ]
f1=open('./slopes.csv', 'w+')
print >>f1, "Symbol,ClosePrice,Slope,AvgVolume,Trading Days"
for symbol in files:
    db = sqlite3.connect('db/'+symbol)
    c = db.cursor()
    c.execute("select count(*) from stockhistory")
    rows = c.fetchall()
    for row in rows:
        if row[0] < 121:
            #print(symbol+":  less than 121 rows")
            os.remove('db/'+symbol)
            break
        elif row[0] > 121:
            #print(symbol+":  greater than 121 rows")
            ntd = 120
            slope = 1
            getslope(symbol, ntd, slope)
        else:
            print("ah crap")

