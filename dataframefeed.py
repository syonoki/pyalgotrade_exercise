# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 18:13:44 2017

@author: ijlee
"""

from pyalgotrade import barfeed
from pyalgotrade import membf
from pyalgotrade import bar
from pyalgotrade import utils
from pyalgotrade import csvfeed


class BasicDfRowParser(csvfeed.RowParser):
        def parseBar(self, csvRowDict):
        raise NotImplementedError()

    def getFieldNames(self):
        raise NotImplementedError()

    def getDelimiter(self):
        raise NotImplementedError()
        
        

class Feed(membf.BarFeed):
    def __init__(self, frequency, maxLen=None):
        super(BarFeed, self).__init__(frequency, maxLen)
        
        self.__barFilter = None
        self.__dailyTime = datetime.time(0, 0, 0)
    
        def getDailyBarTime(self):
        return self.__dailyTime

    def setDailyBarTime(self, time):
        self.__dailyTime = time

    def getBarFilter(self):
        return self.__barFilter

    def setBarFilter(self, barFilter):
        self.__barFilter = barFilter
        
    def addBarsFromDf(self, instrument, df, rowParser=None):
        if rowParser is None:
            rowParser = BasicDfRowParser()
            
        for index, row in df.iterrows():
            bar_ = rowParser.parseBar(row)
            if bar_ is not None and (self.__barFilter is None or self.__barFilter.includeBar(bar_)):
                loadedBars.append(bar_)