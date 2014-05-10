#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3

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

def f(number, sigfig):
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
            slope=f(slope,64)
            print(symbol + " : " + slope)
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
for symbol in files:
    ntd = 120
    slope = 1
    getslope(symbol, ntd, slope)

