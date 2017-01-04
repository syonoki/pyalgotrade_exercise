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
    
from datetime import date
samsung = getBarsFromCybos("A005930", date(2015, 1, 1), date(2016, 12, 29))

import dataframefeed
feed = dataframefeed.Feed()
feed.addBarsFromDf('samsung', samsung)