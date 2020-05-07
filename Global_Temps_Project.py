#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 13:24:01 2020

@author: paultanger
"""

import pandas as pd
import numpy as np

# here is the SQL export with temp data
wd = '~/Desktop/Dropbox/2020 data science stuff/data science course stuff/udacity data analyst nanodegree/'
tempdata = pd.read_csv(wd + 'combined_temps.csv')

# first try moving avg with sample data - there is commas in numbers
SalesData = pd.read_csv(wd + 'moving-average-exercise.csv', thousands=',')

# this next line creates a "cell" which can be run together using shift enter
#%%
print(SalesData.head())
print(SalesData.info())
window_size = 7

# some examples
# numbers_series = pd.Series(numbers)
# windows = numbers_series.rolling(window_size)
# moving_averages = windows.mean()

# moving_averages_list = moving_averages.tolist()
# without_nans = moving_averages_list[window_size - 1:]

# add col with moving average
SalesData['Sales_7day_SMA'] = SalesData.iloc[:,1].rolling(window=window_size).mean()


