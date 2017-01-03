# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 16:17:33 2016

@author: ijlee
"""

import pandas as pd
import win32com.client as com

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