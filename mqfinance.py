# Functions for financial monitoring through conky, time to retirement clock, etc. 

import math as m
import numpy as np
import subprocess

def snetw():
    
    # Tracks portfolio value and growth. Basically, I want to get the number that 
    # the broker's webtrader shows without any need to log in.

    # TODO

    # 1.
    # For mobile we need to rewrite it without numpy. 
    # Numpy can make it into Android, but it's too big of a hassle. Besides, writing 
    # the same code in two different ways can be a good exercise. 
    # A dirty workaround for mobile is changing the input parameters, recalculating 
    # externally fees and 'average' stock price.

    # 2.
    # Made for a single stock (IWDA.AS) but we could make a dictionary if the 
    # portfolio holds more types of shares. Just making a for loop which iterates 
    # over the dictionary. Or perhaps integrating them with the other shares. This is 
    # something worth meditating about. Portfolio purchase price is easy to calculate 
    # that way (the array just has number of shares and their purchase price), but 
    # for calculating current portfolio value, we need to know how many shares of each 
    # type we have... Worth asking on SE, if you ask me (programmers).

    # We could make one list for each stock type and broker combination. 
    
    # 3.
    # Add exceptions, so whenever curl fails (no connection) returns 'Couldn't 
    # retrieve data' instead of gibberish. 
    
    # 4.
    # Add a time check, so it doesn't execute if the market is closed. 

    # NOTE
    # Added capability to account for several purchases. 
    # Inputs are nshares, pprice and cash. The rest is calculated, which might make it 
    # slower for our purposes (conky, mobile app) but this is the right way. 


    # MAIN


    # Input data
    nshares = np.array([36, 21, 12, 14, 24])  # Number of shares purchased on each instance.
    pprice = np.array([40.55, 39.33, 38.49, 37.64, 33.52])  # Purchase price of the shares. 
    cash = 31.87  # Available funds on the broker account.
    # Location of the file that stores current stock prices. 
    thepath = ("/media/01/python/InvestmentTools/"
    "SharesNetWorth/")

    tnshares = np.sum(nshares)

    dataout = []  # All the data we want the function to return us. 

    # Retrieve current share price. 
    bashCommand = "curl -s 'http://download.finance.yahoo.com/d/quotes.csv?s=iwda.as&f=l1'"
    sprice = float(subprocess.check_output(bashCommand, shell=True))
    dataout.append(sprice)

    # Purchase price of the portfolio
    purchase = nshares * pprice
    pportfolio = np.sum(purchase)
    dataout.append(pportfolio) 

    # Current portfolio value
    portfolio = (np.sum(nshares))*sprice  # Total number of shares * current price. 
    portfoliofull = portfolio + cash  # We consider 'cash' as part of the portfolio
    dataout.append(portfoliofull) 

    # Fees 
    # NOTE Fees depend on the broker, product, etc. 
    fees = (purchase * 0.0002) + 2  # DeGiro fees for ETFs on Euronext
    tfees = np.sum(fees)
    dataout.append(tfees)

    # Balance
    growth = portfolio - pportfolio - tfees
    dataout.append(growth)

    # dataout = [sprice, pportfolio, portfoliofull, tfees, growth]
    
    # Print data to file. 
    stock_data = open( thepath + 'stock_data.txt', 'w')       
    stock_data.write(str(dataout[0]) + '\n')
    stock_data.write(str(round(dataout[2],2)) + '\n')    
    stock_data.write(str(round(dataout[4],2)) + '\n')
    stock_data.close()

    return
