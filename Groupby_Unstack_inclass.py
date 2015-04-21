from __future__ import division
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import os

main_dir = "/Users/Vivian/Desktop/Data/" 
root = main_dir + "Inclass Data/"

## PATHING
paths = [os.path.join(root,v) for v in os.listdir(root) if v.startswith("file_")]


# IMPORT and STACK-------
df = pd.concat([pd.read_csv(v, names = ['panid', 'date', 'kwh']) for v in paths], ignore_index = True)

df_assign = pd.read_csv(root + "sample_assignments.csv", usecols = [0,1])

## MERGE
df = pd.merge(df, df_assign)

#GROUPBY aka "split, apply, combine"
## See Dan's codes

# Split by C/T, pooled w/o time
groups1 = df.groupby(['assignment'])
groups1.groups

# apply the mean
groups1['kwh'].apply(np.mean) #this calculates a pooled mean; time is not a factor; np is numpy
        #.apply is to "apply" ANY type of function
groups1['kwh'].mean() 
        #.mean() is an insternal method, a faster way that produce the same results as Line 30
        
##DataFrame. + tab or Series. + tab will allow you to see all the internal functions


# Split by Control and Treatment, pooled WITH time
groups2 = df.groupby(['assignment', 'date']) #<-- the order for the 'date' and 'assignment' matters! It affects how to look at the 
            ##data, but the number should be the same
groups2.groups

# apply the mean
groups2['kwh'].mean() #remember, this is mean from pooling accounting for time

# UNSTACK--------
gp_mean = groups2['kwh'].mean() 
gp_unstack = gp_mean.unstack('assignment')
gp_unstack['T'] # mean, over time, of all treated panids






