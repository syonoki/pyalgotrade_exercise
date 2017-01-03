# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 23:53:31 2017

@author: syono
"""

from cybos import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import win32com.client as com

from datetime import datetime

def getBarsFromCybos(code, start_date, end_date):
    stockChart = com.Dispatch('CpSysDib.StockChart')
    stockChart.SetInputValue(0, code)
    stockChart.SetInputValue(1, ord('1'))
    stockChart.SetInputValue(3, start_date.strftime("%Y%m%d"))
    stockChart.SetInputValue(2, end_date.strftime("%Y%m%d"))
    stockChart.SetInputValue(5, [0, 2, 3, 4, 5, 8])
    stockChart.SetInputValue(6, ord('D'))
    stockChart.SetInputValue(9, ord('1'))
    
    stockChart.BlockRequest()
    numData = stockChart.GetHeaderValue(3)
    df = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    for i in range(numData):
        df.loc[i]=[datetime.strptime(str(stockChart.GetDataValue(0, i)), "%Y%m%d") \
                   , stockChart.GetDataValue(1, i) \
                   , stockChart.GetDataValue(2, i) \
                   , stockChart.GetDataValue(3, i) \
                   , stockChart.GetDataValue(4, i) \
                   , stockChart.GetDataValue(5, i)]
         
    return df
    
from datetime import date
samsung = getBarsFromCybos("A005930", date(2015, 1, 1), date(2016, 12, 29))

import dataframefeed
feed = dataframefeed.Feed()
feed.addBarsFromDf('samsung', samsung)