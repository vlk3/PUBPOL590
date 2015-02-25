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
df = pd.concat([pd.read_table(v, skiprows = 6000000, nrows = 1500000, sep = " ", names = ['ID', 'DAYHH', 'kwh'], header=0, parse_dates=[2]) for v in paths], ignore_index = True)
df_allocation = pd.read_csv(root + "SME and Residential allocations.csv",usecols = ['ID','Code','Residential - Tariff allocation','Residential - stimulus allocation'],na_values = ['-', 'NA', 'NULL', '', '.'])
df2 = df_allocation.rename(columns = {'Residential - Tariff allocation':'RES_Tariff','Residential - stimulus allocation':'RES_Stimulus'})

# Trimming data before merging
df2 = df2[df2.Code <=1] # this will keep only Residnetial Home under "Code"
df2[(df2['RES_Tariff'] == 'A') & (df2['RES_Stimulus']== '1') | (df2['RES_Stimulus']== 'E')] 
    #Keep only Tariff A and Bi-monthly (1) stimulus or the Control (E)
df2 = df2[(df2['RES_Tariff'] == 'A') & (df2['RES_Stimulus']== '1') | (df2['RES_Stimulus']== 'E')] 

df = pd.merge(df, df2, on = 'ID')
# Can use df.sort[('')] to check to make sure all the tariff and stimulus groups are represented. I'm sure there's an easier way... oh well

#df1 = pd.concat(df, ignore_index = True)
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
grp = df3.groupby(['ID','day_cer','Code', 'RES_Tariff', 'RES_Stimulus'])
agg = grp['kwh'].sum()
#grp.sum() 

# reset the index (multilevel at the moment)
agg = agg.reset_index() # drop the multi-index
grp1 = agg.groupby(['day_cer', 'Code', 'RES_Tariff', 'RES_Stimulus']) 
#agg.head() to look at first five rows

## split up treatment/control
trt = {(k[0], k[1], k[2]): agg.kwh[v].values for k, v in grp1.groups.iteritems() if k[3] == '1'} # get set of all treatments by date
ctrl = {(k[0], k[1], k[2]): agg.kwh[v].values for k, v in grp1.groups.iteritems() if k[3] == 'E'} # get set of all controls by date
keys = ctrl.keys()

# tstats and pvals
tstats = DataFrame([(k, np.abs(float(ttest_ind(trt[k], ctrl[k], equal_var=False)[0]))) for k in keys], columns=['ymd', 'tstat'])
pvals = DataFrame([(k, (ttest_ind(trt[k], ctrl[k], equal_var=False)[1])) for k in keys], columns=['ymd', 'pval'])
t_p = pd.merge(tstats, pvals)