#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 13:24:01 2020

@author: paultanger
"""

import pandas as pd
import numpy as np
import os

# here is the SQL export with temp data
wd = '/Users/paultanger/Desktop/Dropbox/2020 data science stuff/data science course stuff/udacity data analyst nanodegree/'
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
# better to use col names not index
SalesData['Sales_7day_SMA'] = SalesData.loc[:,['Sales']].rolling(window=window_size).mean()

# look up value
# SalesData.Sales_7day_SMA.loc[(SalesData.Date == '1/11/2009')]
SalesData.Sales_7day_SMA[SalesData.Date == '1/11/2009']
round(SalesData.Sales_7day_SMA[SalesData.Date == '1/11/2009'],0)

# 14 day
window_size = 14
SalesData['Sales_14day_SMA'] = SalesData.iloc[:,1].rolling(window=window_size).mean()
round(SalesData.Sales_14day_SMA[SalesData.Date == '3/19/2009'],0)


# do it for temp data now

# first plot line graph of temp then determine a good window size
import seaborn as sns
import matplotlib.pyplot as plt
window_size = 3 
tempdata['Denver_T_3yr_moving_avg'] = tempdata.loc[:,'denver_temp'].rolling(window=window_size).mean()
tempdata['Global_T_3yr_moving_avg'] = tempdata.loc[:,'avg_temp'].rolling(window=window_size).mean()

# line plot
lineplt = sns.lineplot(x="year", y="denver_temp", data=tempdata)
plt.show()

# convert to long format to plot together
tempdata_long = tempdata.melt(id_vars='year')
tempdata_long.head()
tempdata_long.info()

# plot it
lineplt2 = sns.lineplot(x='year', y='value', hue='variable', data=tempdata_long)

# ok just plot moving avgs
# also Denver doesn't have consistent data until 1820 so just start there
tempdata2 = tempdata.iloc[:, [0,3,4]]
tempdata_long2 = tempdata2.melt(id_vars='year')
tempdata_long2 = tempdata_long2[tempdata_long.year >= 1820]

lineplt2 = sns.lineplot(x='year', y='value', hue='variable', data=tempdata_long2)
# nice axis labels
lineplt2.set(xlabel='Year', ylabel='Temperature (C)')
lineplt2.set_title('Temperature trends over last 200 years')
#lineplt2.legend().set_title('')

# remove legend title
handles, labels = lineplt2.get_legend_handles_labels()
lineplt2.legend(handles=handles[1:], labels=labels[1:])

plt.show()

# function to save with timestamp
def add_timestamp(string, extension):
    import time
    timestamp = time.strftime("_%Y%m%d_%H%M%S")
    return string + timestamp + '.' + extension

# make filename
filename = add_timestamp('temp_line_plot', 'pdf')

#%%
# save as pdf

lineplt2 = sns.lineplot(x='year', y='value', hue='variable', data=tempdata_long2)
# nice axis labels
lineplt2.set(xlabel='Year', ylabel='Temperature (C)')
lineplt2.set_title('Temperature trends over last 200 years')

# remove legend title
handles, labels = lineplt2.get_legend_handles_labels()
lineplt2.legend(handles=handles[1:], labels=labels[1:])
# make filename
filename = add_timestamp('temp_line_plot', 'pdf')
plt.savefig(wd + filename)

# try with 10 yr avg
window_size = 10
tempdata['Denver_T_10yr_moving_avg'] = tempdata.loc[:,'denver_temp'].rolling(window=window_size).mean()
tempdata['Global_T_10yr_moving_avg'] = tempdata.loc[:,'avg_temp'].rolling(window=window_size).mean()

tempdata3 = tempdata.iloc[:, [0,5,6]]
tempdata_long3 = tempdata3.melt(id_vars='year')
tempdata_long3 = tempdata_long3[tempdata_long.year >= 1820]

lineplt3 = sns.lineplot(x='year', y='value', hue='variable', data=tempdata_long3)
# nice axis labels
lineplt3.set(xlabel='Year', ylabel='Temperature (C)')
lineplt3.set_title('Temperature trends over last 200 years')

# remove legend title
handles, labels = lineplt3.get_legend_handles_labels()
lineplt3.legend(handles=handles[1:], labels=labels[1:])
# make filename
filename = add_timestamp('temp_line_plot_10yr', 'pdf')
plt.savefig(wd + filename)

# correlation between global and Denver
sns.pairplot(tempdata3, vars=['Denver_T_10yr_moving_avg', 'Global_T_10yr_moving_avg'])
scatterplt = sns.scatterplot(x="Denver_T_10yr_moving_avg", y="Global_T_10yr_moving_avg", data=tempdata3)

# not quite normal?
sns.distplot(tempdata3['Denver_T_10yr_moving_avg'])

x = tempdata3['Denver_T_10yr_moving_avg']
y = tempdata3['Global_T_10yr_moving_avg']

x.corr(y)
x.corr(y, method='spearman')

# four observations

# predict Denver temp using global temp using regression
