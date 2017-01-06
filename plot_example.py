# -*- coding: utf-8 -*-
"""
Created on Fri Jan 06 21:43:35 2017

@author: syono
"""

from cybos import *
import pandas as pd
import matplotlib.pyplot as plt
from strategy import BollingerStrategy, BuyAndHoldStrategy
from barfeed import dataframefeed
from pyalgotrade import plotter

from datetime import date

targetStock = getBarsFromCybos("A000660", date(2015, 1, 1), date(2016, 12, 29))
targetStock.index = targetStock['Date']
initialCash = 200000
feed = dataframefeed.Feed()
feed.addBarsFromDf('targetStock', targetStock)

myStrategy = BollingerStrategy(feed, 'targetStock', initialCash, 20, 1.8)
plt = plotter.StrategyPlotter(myStrategy)
subplot = plt.getInstrumentSubplot('targetStock')
subplot.addDataSeries("Middle", myStrategy.getMiddle()) 
subplot.addDataSeries("Upper", myStrategy.getUpper()) 
subplot.addDataSeries("Lower", myStrategy.getLower()) 

myStrategy.run()
print "Bollinger Band: Final portfolio value: $%.2f" % myStrategy.getBroker().getEquity()

plt.plot()