# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 16:17:33 2016

@author: ijlee
"""

import pandas as pd
import win32com.client as com
from datetime import datetime

def getCodeNamesFromCp():
    codeMgr = com.Dispatch('CpUtil.CpCodeMgr')
    
    cpCodes = codeMgr.GetStockListByMarket(1)
    cpNames = [codeMgr.CodeToName(code) for code in cpCodes]
    
    cpCodeName = pd.DataFrame({'Code':cpCodes, 'Name':cpNames})
    
    cpCodeName['KRX Code'] = [code[1:] + "KS" for code in cpCodeName['Code']]
    cpCodeName['Source'] = 'Cybos'
    
    codeNames = cpCodeName.rename(columns={'KRX Code':'Master Code'})
    codeNames = codeNames[['Master Code', 'Name', 'Source', 'Code']]
    return codeNames
    
def findCodes(df, name):
    return df[df['Name'].str.contains(name)]
              
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