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

if __name__=='__main__':
    tests=[
        (0.1, 1, '0.1'),
        (0.0000000000368568, 2,'0.000000000037'),
        (0.00000000000000000000368568, 2,'0.0000000000000000000037'),
        (756867, 3, '757000'),
        (-756867, 3, '-757000'),
        (-756867, 1, '-800000'),
        (0.0999999999999,1,'0.1'),
        (0.00999999999999,1,'0.01'),
        (0.00999999999999,2,'0.010'),
        (-0.0007917910966039466529042822884321140008978545665740966796875,32,'-0.00079179109660394665290428228843211'),
        (0.0099,2,'0.0099'),
        (1.999999999999,1,'2'),
        (1.999999999999,2,'2.0'),
        (34500000000000000000000, 17, '34500000000000000000000'),
        ('34500000000000000000000', 17, '34500000000000000000000'),
        (756867, 7, '756867.0'),
        ]

    for number,sigfig,answer in tests:
        try:
            result=f(number,sigfig)
            assert(result==answer)
            print(result)
        except AssertionError:
            print('Error',number,sigfig,result,answer)