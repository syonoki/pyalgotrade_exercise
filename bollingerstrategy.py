# -*- coding: utf-8 -*-
"""
Created on Thu Jan 05 14:53:37 2017

@author: ijlee
"""

from pyalgotrade import strategy
from pyalgotrade.technical import bollinger


class BollingerStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, initialCash, period, width):
        super(BollingerStrategy, self).__init__(feed, initialCash)
        self.__position = None
        self.setUseAdjustedValues(True)
        self.__bollinger = bollinger.BollingerBands(feed[instrument].getCloseDataSeries(), period, width)
        self.__instrument = instrument
        self.__previousClose = None     
        self.date = []
        self.upper = []
        self.middle = []
        self.lower = []

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        self.info("BUY at $%.2f" % (execInfo.getPrice()))

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        self.info("SELL at $%.2f" % (execInfo.getPrice()))
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()
        
    def _lowerDownUpCrossOver(self, close, previousClose, lower):
        if previousClose < lower and close >= lower:
            return True
        
        return False
        
    def _upperUpDownCross(self, close, previousClose, upper):
        if previousClose > upper and close <= upper:
            return True
        
        return False
    
    def _upperDownUpCross(self, close, previousClose, upper):
        if previousClose < upper and close >= upper:
            return True
        
        return False
        
    def onBars(self, bars):
               
        bar = bars[self.__instrument]
        
        middle = self.__bollinger.getMiddleBand()
        upper = self.__bollinger.getUpperBand()
        lower = self.__bollinger.getLowerBand()
        
        self.date.append(bar.getDateTime())
        self.middle.append(middle[-1])
        self.upper.append(upper[-1])
        self.lower.append(lower[-1])
        
        if middle[-1] is None:
            return
        
        if self.__position is None:
            if self._lowerDownUpCrossOver(bar.getClose(), self.__previousClose, lower[-1]):
                self.__position = self.enterLong(self.__instrument, 1, True)
        elif self._upperUpDownCross(bar.getClose(), self.__previousClose, upper[-1]) and not self.__position.exitActive():
            self.__position.exitMarket()
        
        self.__previousClose = bar.getClose()
        
