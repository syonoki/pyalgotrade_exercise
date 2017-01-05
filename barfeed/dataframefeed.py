# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 18:13:44 2017

@author: ijlee
"""

from pyalgotrade.barfeed import membf
from pyalgotrade import bar

import datetime

class BasicDfRowParser():
    def __init__(self, dailyBarTime, frequency, timezone=None, barClass=bar.BasicBar):
        self.__dailyBarTime = dailyBarTime
        self.__frequency = frequency
        self.__timezone = timezone
        self.__barClass = barClass

    def getFieldNames(self):
        # It is expected for the first row to have the field names.
        return None

    def parseBar(self, row):
        dateTime = row["Date"]
        close = row["Close"]
        open_ = row["Open"]
        high = row["High"]
        low = row["Low"]
        volume = row["Volume"]
        adjClose = row["Close"]

        return self.__barClass(dateTime, open_, high, low, close, volume, adjClose, self.__frequency)
        
        
class Feed(membf.BarFeed):
    def __init__(self, frequency=bar.Frequency.DAY, timezone=None, maxLen=None):
        if isinstance(timezone, int):
            raise Exception("timezone as an int parameter is not supported anymore. Please use a pytz timezone instead.")

        if frequency not in [bar.Frequency.DAY, bar.Frequency.WEEK]:
            raise Exception("Invalid frequency.")

        self.__timezone = timezone
        self.__barClass = bar.BasicBar
        self.__dailyTime = datetime.time(0, 0, 0)
        self.__frequency = frequency
        
        super(Feed, self).__init__(frequency, maxLen)
    
    def setBarClass(self, barClass):
        self.__barClass = barClass

    def barsHaveAdjClose(self):
        return True
        
    def getDailyBarTime(self):
        return self.__dailyTime

    def setDailyBarTime(self, time):
        self.__dailyTime = time
        
    def addBarsFromDf(self, instrument, df, rowParser=None):
        loadedBars = []
        
        if rowParser is None:
            rowParser = BasicDfRowParser(self.__dailyTime, self.__frequency)
            
        for index, row in df.iterrows():
            bar_ = rowParser.parseBar(row)
            if bar_ is not None:
                loadedBars.append(bar_)
        
        self.addBarsFromSequence(instrument, loadedBars)