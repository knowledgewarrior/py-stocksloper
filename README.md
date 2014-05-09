stocksloper
=============
Stocksloper grabs stocks from Yahoo Finance and calculates linear regression analysis on the slope of the data based on the formula.

First you need to download all symbols you want from Yahoo Finance and put into a MySQL database - there's a few scripts on Google you can use.  The ones I found are written in python.

Stocksloper does the symbol lookup in the database, then grabs the historical data for each symbol.

--

Requirements:

Regression Formula:
Slope(b) = (NΣXY - (ΣX)(ΣY)) / (NΣX2 - (ΣX)2)

where:
X = trading days (1,2,3,4,5….)
Y = closing price
b = The slope of the regression line
N = Number of values (i.e. the number of days we are evaluating)
ΣXY = Sum of the product of X and Y
ΣX = Sum of X
ΣY = Sum of Y
ΣX2 = Sum of square of X

Regression Example: To find the Simple/Linear Regression of
X Values
Trading days  Y Values
Closing Price
1 3.10
2 2.90
3 3.05
4 2.95
5 3.10


Step 1: Count the number of values.  N =  # of trading days (in this example it will be 5) but for our purposes the first run will be n = 120, and if the slope is NOT < +0.01 and > -0.01 then the second run will be n = 121 and so on…

Step 2: Find X * Y, X2  and ΣX, ΣY , ΣXY, ΣX2.

See the below table
X Value Y Value X * Y X * X
1 3.10  1 * 3.10 = 3.10 1 * 1 = 1
2 2.90  2 * 2.90 = 5.80 2 * 2 = 4
3 3.05  3 * 3.05 = 9.15 3 * 3 = 9
4 2.95  4 * 2.95 = 11.80  4 * 4 = 16
5 3.10  5 * 3.10 = 15.50  5 * 5 = 25

ΣX =15   ΣY=15.10    ΣXY=45.35     ΣX2=55

Step 4: Substitute those numbers into the formula

Slope(b) = (N*ΣXY - (ΣX)(ΣY)) / (N*ΣX2 - (ΣX)2)

= ((5)*(45.35)-(15)*(15.10)) / ((5)*(55)-(15)2)
= (226.75 – 226.50) / (275 - 225)
= 0.25 / 50
= 0.005

Since the slope falls within the +0.01 to -0.01 range, this stock would be added to the LIST, if it didn’t then the formula would run again with n = 121, and so on…
