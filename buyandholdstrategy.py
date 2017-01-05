# -*- coding: utf-8 -*-
"""
Created on Thu Jan 05 16:52:33 2017

@author: ijlee
"""

from pyalgotrade import strategy

class BuyAndHoldStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, initialCash):
        super(BuyAndHoldStrategy, self).__init__(feed, initialCash)
        self.__position = None
        self.setUseAdjustedValues(True)
        self.__instrument = instrument
        
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
 
    def onBars(self, bars):
                
        if self.__position is None:
                self.__position = self.enterLong(self.__instrument, 1, True)
        
    