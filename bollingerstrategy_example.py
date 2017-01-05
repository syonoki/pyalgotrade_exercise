# -*- coding: utf-8 -*-
"""
Created on Thu Jan 05 15:03:27 2017

@author: ijlee
"""
from cybos import *
import pandas as pd
import matplotlib.pyplot as plt
from strategy import BollingerStrategy, BuyAndHoldStrategy
from barfeed import dataframefeed

from datetime import date

targetStock = getBarsFromCybos("A000660", date(2015, 1, 1), date(2016, 12, 29))
targetStock.index = targetStock['Date']
initialCash = 200000

feed = dataframefeed.Feed()
feed.addBarsFromDf('targetStock', targetStock)

buyandhold = BuyAndHoldStrategy(feed, 'targetStock', initialCash)

buyandhold.run()
print "Buy and Hold: Final portfolio value: $%.2f" % buyandhold.getBroker().getEquity()

feed.reset()
myStrategy = BollingerStrategy(feed, 'targetStock', initialCash, 20, 1.8)
myStrategy.run()
print "Bollinger Band: Final portfolio value: $%.2f" % myStrategy.getBroker().getEquity()

plotData = pd.DataFrame(data={'Close':targetStock['Close'], 'Upper': list(reversed(myStrategy.upper)), \
                              'Lower': list(reversed(myStrategy.lower)), \
                              'Middle': list(reversed(myStrategy.middle))}, index= targetStock['Date'])

plotData.plot()