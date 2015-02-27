from __future__ import division
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

main_dir = "/Users/Vivian/Desktop/Data/" 
root = main_dir + "Group Assignment/"

# PATHING----------------------
paths = [os.path.join(root, v) for v in os.listdir(root) if v.startswith("File")]

# IMPORT AND STACK--------------------
df = pd.concat([pd.read_table(v, skiprows = 6000000, nrows = 1500000, sep = " ", names = ['ID', 'DAYHH', 'kwh']) for v in paths], ignore_index = True)
df_allocation = pd.read_csv(root + "SME and Residential allocations.csv",usecols = ['ID','Code','Residential - Tariff allocation','Residential - stimulus allocation'],na_values = ['-', 'NA', 'NULL', '', '.'])
df2 = df_allocation.rename(columns = {'Residential - Tariff allocation':'RES_Tariff','Residential - stimulus allocation':'RES_Stimulus'})

# Trimming data before merging
df2 = df2[df2.Code <=1] # this will keep only Residnetial Home under "Code"
df2[(df2['RES_Tariff'] == 'A') & (df2['RES_Stimulus']== '1') | (df2['RES_Stimulus']== 'E')] 
    #Keep only Tariff A and Bi-monthly (1) stimulus or the Control (E)
df2 = df2[(df2['RES_Tariff'] == 'A') & (df2['RES_Stimulus']== '1') | (df2['RES_Stimulus']== 'E')] 

df = pd.merge(df, df2, on = 'ID')
# Can use df.sort[('')] to check to make sure all the tariff and stimulus groups are represented. I'm sure there's an easier way... oh well

## Splitting the DAYHH column into Day and HH
df['hour_cer'] = df['DAYHH'] %100
df['day_cer'] = (df['DAYHH']-df['hour_cer']% 100)/100
df = df[['ID', 'DAYHH', 'hour_cer', 'day_cer', 'kwh', 'Code', 'RES_Tariff', 'RES_Stimulus']]

# IMPORTING TS Correction
df_correction = pd.read_csv(root + "timeseries_correction.csv", usecols = ['hour_cer', 'day_cer','date', 'year', 'month', 'day'])
# CER ANOMOLY CORRECTION
## see http://pandas.pydata.org/pandas-docs/stable/indexing.html#advanced-indexing-with-labels
df_correction.ix[df_correction['day_cer'] == 452, 'hour_cer'] = np.array([v for v in range(1,49) if v not in [2,3]])

df3 = pd.merge(df, df_correction, on= ['hour_cer','day_cer'])


# DAILY AGGREGATION --------------------
grp = df3.groupby(['ID','day_cer', 'RES_Stimulus']) #this helps agg the kwh consumption for every HH
agg = grp['kwh'].sum()
grp.sum() 

# reset the index (multilevel at the moment)
agg = agg.reset_index() # drop the multi-index
grp1 = agg.groupby(['day_cer','RES_Stimulus']) #reducing the amount of groups and increasing thel list size; we are distinguishing them by assignemtn, not HH
#agg.head() to look at first five rows

## split up treatment/control
trt = {(k[0]): agg.kwh[v].values for k, v in grp1.groups.iteritems() if k[1] == '1'} # get set of all treatments by date
ctrl = {(k[0]): agg.kwh[v].values for k, v in grp1.groups.iteritems() if k[1] == 'E'} # get set of all controls by date
keys = ctrl.keys()

# tstats and pvals
tstats = DataFrame([(k, np.abs(float(ttest_ind(trt[k], ctrl[k], equal_var=False)[0]))) for k in keys], columns=['day_cer', 'tstat'])
pvals = DataFrame([(k, (ttest_ind(trt[k], ctrl[k], equal_var=False)[1])) for k in keys], columns=['day_cer', 'pval'])
t_p = pd.merge(tstats, pvals)


#Plotting!
fig1 = plt.figure() # initialize plot
ax1 = fig1.add_subplot(2,1,1) # two rows, one column, first plot
ax1.plot(t_p['day_cer'],t_p['tstat'])
ax1.axhline(2, color='r', linestyle='--')
ax1.axvline(180, color='g', linestyle='--')
ax1.set_title('t-stats over-time (daily)')

ax2 = fig1.add_subplot(2,1,2) # two rows, one column, first plot
ax2.plot(t_p['day_cer'], t_p['pval'])
ax2.axhline(0.05, color='r', linestyle='--')
ax2.axvline(180, color='g', linestyle='--')
ax2.set_title('p-values over-time (daily)')
plt.show()

# MONTHLY AGGREGATION 
grp2 = df3.groupby(['ID','year','month','RES_Stimulus']) ## Dan said to group by year and month
agg1 = grp2['kwh'].sum()

# reset the index (multilevel at the moment)
agg1 = agg1.reset_index() # drop the multi-index
grp3 = agg1.groupby(['year', 'month', 'RES_Stimulus']) 
#agg.head() to look at first five rows

## split up treatment/control
trt1 = {(k[0], k[1]): agg1.kwh[v].values for k, v in grp3.groups.iteritems() if k[2] == '1'} # get set of all treatments by year-month
ctrl1 = {(k[0], k[1]): agg1.kwh[v].values for k, v in grp3.groups.iteritems() if k[2] == 'E'} # get set of all controls by year-month
keys2 = ctrl1.keys()

# tstats and pvals
tstats1 = DataFrame([(k, np.abs(float(ttest_ind(trt1[k], ctrl1[k], equal_var=False)[0]))) for k in keys2], columns=['month', 'tstat1'])
pvals1 = DataFrame([(k, (ttest_ind(trt1[k], ctrl1[k], equal_var=False)[1])) for k in keys2], columns=['month', 'pval1'])
t_p1 = pd.merge(tstats1, pvals1)


#Plotting!
fig2 = plt.figure() # initialize plot
ax3 = fig2.add_subplot(2,1,1) # two rows, one column, first plot
ax3.plot(t_p1['tstat1'])
ax3.axhline(2, color='r', linestyle='--')
ax3.axvline(6, color='g', linestyle='--')
ax3.set_title('t-stats over-time (monthly)')

ax4 = fig2.add_subplot(2,1,2) # two rows, one column, first plot
ax4.plot(t_p1['pval1'])
ax4.axhline(0.05, color='r', linestyle='--')
ax4.axvline(6, color='g', linestyle='--')
ax4.set_title('p-values over-time (monthly')
plt.show()
