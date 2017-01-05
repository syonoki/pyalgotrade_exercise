# -*- coding: utf-8 -*-
"""
Created on Thu Jan 05 15:03:27 2017

@author: ijlee
"""
from cybos import *
import pandas as pd
import matplotlib.pyplot as plt
from bollingerstrategy import *
from buyandholdstrategy import *

from datetime import date
daum = getBarsFromCybos("A000660", date(2015, 1, 1), date(2016, 12, 29))
daum.index = daum['Date']
initialCash = 200000

import dataframefeed
feed = dataframefeed.Feed()
feed.addBarsFromDf('daum', daum)

buyandhold = BuyAndHoldStrategy(feed, 'daum', initialCash)

buyandhold.run()
print "Buy and Hold: Final portfolio value: $%.2f" % buyandhold.getBroker().getEquity()

feed = dataframefeed.Feed()
feed.addBarsFromDf('daum', daum)
myStrategy = BollingerStrategy(feed, 'daum', initialCash, 20, 1.8)
myStrategy.run()
print "Bollinger Band: Final portfolio value: $%.2f" % myStrategy.getBroker().getEquity()

plotData = pd.DataFrame(data={'Close':daum['Close'], 'Upper': list(reversed(myStrategy.upper)), \
                              'Lower': list(reversed(myStrategy.lower)), \
                              'Middle': list(reversed(myStrategy.middle))}, index= daum['Date'])

plotData.plot()