from __future__ import division
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

main_dir = "/Users/Vivian/Desktop/Data/" 
root = main_dir + "Inclass Data/data/"

# PATHING --------------
paths = [os.path.join(root,v) for v in os.listdir(root) if v.startswith("file_")]
# IMPORT AND STACK ---------
df = pd.concat([pd.read_csv(v, names = ['panid', 'date', 'kwh'], parse_dates = [1], header=0) for v in paths],
ignore_index = True) #the parse_date changes the format of how the date column [1] is presented in the dataframe
df_assign = pd.read_csv(root + "sample_assignments.csv", usecols = [0,1])

# MERGE ---------
df = pd.merge(df, df_assign) 

#TO SORT
df.sort(['date'])
# GROUPBY aka "split, apply, combine"
## see more at http://pandas.pydata.org/pandas-docs/stable/groupby.html
grp1 = df.groupby(['assignment']) # .groupby objects for big data
gd1 = grp1.groups # CAUTION! don't do this with super big data. it will crash.

## peek inside gd1 (dictionary)
gd1.keys()
gd1['C'] # gd1 is a dict, so must use keys to get data
gd1.values()[0] # gd1.values() is a list, so we can use numerical indeces
gd1.viewvalues() # see all the values of the dictionary, gd1


## iteration properties of a dictionary
[v for v in gd1.itervalues()]
gd1.values() # equivalent to above
[k for k in gd1.iterkeys()]
gd1.keys() # equivalent
[(k,v) for k,v in gd1.iteritems()]
gd1

## split and apply (pooled data)
grp1['kwh'].mean()
## split and apply (panel/time series data)
grp2 = df.groupby(['assignment','date'])
gd2 = grp2.groups
gd2 # look at the dictionary (key, value) pairs
grp2['kwh'].mean() ## this doesn't help with cross comparison of treatment and control, though.


## TESTING FOR BALANCE (OVER-TIME)
from scipy.stats import ttest_ind


## ex using ttest_ind
a = [1, 4, 9, 2]
b = [1, 7, 8, 9]
t, p = ttest_ind(a, b, equal_var = False)


# set up data
grp = df.groupby(['assignment', 'date'])
# get separate sets of treatment and control values by date
trt = {k[1]: df.kwh[v].values for k, v in grp.groups.iteritems() if k[0] == 'T'}
ctrl = {k[1]: df.kwh[v].values for k, v in grp.groups.iteritems() if k[0] == 'C'}
keys = trt.keys()

## craete dataframe of this information
tstats = DataFrame([(k, np.abs(ttest_ind(trt[k], ctrl[k], equal_var=False)[0])) for k in keys],
    columns = ['date', 'tstat']) #abs stands for absolute value; ind is individual level
pvals = DataFrame([(k, np.abs(ttest_ind(trt[k], ctrl[k], equal_var=False)[1])) for k in keys],
    columns = ['date', 'pval']) 
t_p = pd.merge(tstats, pvals)

## sort the t_p and reset_index
t_p.sort(['date'], inplace=True) ##need the inplace=True because it sorts AND overwrite; think about Excel sorting
t_p.reset_index(inplace=True, drop=True) # drop=True will drop the old index column!

## PLOTTING----------------
fig1 = plt.figure() ##initializing plot
ax1 = fig1.add_subplot(2,1,1) ## (number or row you want, column you want, and first plot)
ax1.plot(t_p['tstat'])
ax1.axhline(2, color='r', linestyle='--')
ax2= fig1.add_subplot(2,1,2)  #two rows, one column, first plot
ax2.plot(t_p['pval'])
ax2.axhline(0.05, color='r', linesytle='--')
plt.show()

#use plt.plot? for help




