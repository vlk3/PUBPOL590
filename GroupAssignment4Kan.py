from __future__ import division
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import os


main_dir = "/Users/Vivian/Desktop/Data/Group Assignment 4/" 


#CHANGE WORKING DIRECTORY (wd)
os.chdir(main_dir)
from logit_functions import *

## ***SECTION 0*** ##

#IMPORT DATA
df = pd.read_csv(main_dir + '14_B3_EE_w_dummies.csv')
df = df.dropna(axis=0, how='any')

#GET TARIFF
tariffs = [v for v in pd.unique(df['tariff']) if v != 'E']
stimuli = [v for v in pd.unique(df['stimulus']) if v != 'E']
tariffs.sort()
stimuli.sort()

# RUN LOGIT-------------
drop = [v for v in df.columns if v.startswith("kwh_2010")]
df_pretrial = df.drop(drop, axis=1)

for i in tariffs:
        for j in stimuli:
            # dummy variables must start with "D_" and consumption variables with "kwh_"
            logit_results, df_logit = do_logit(df_pretrial, i, j, add_D=None, mc=False)

#QUICK MEANS COMPARISON WITH T-TEST BY HAND------------
#creat means
grp = df_logit.groupby('tariff')
df_mean = grp.mean().transpose()
df_mean.B - df_mean.E

# do a t-test "by hand"
df_s = grp.std().transpose()
df_n = grp. count().transpose().mean()
top = df_mean['B'] - df_mean['E']
bottom = np.sqrt(df_s['B']**2/df_n['B'] + df_s['E']**2/df_n['E'])
tstats = top/bottom
sig = tstats[np.abs(tstats) > 2]
sig.name = 't-stats'


##------------------------------------------------------------------------------------------------------------------##

## ***SECTION 1*** ## Repeat Section 0 with new data set; test for imbalance running Logit and a "Quick Means Comparison"
#IMPORT DATA
df = pd.read_csv(main_dir + 'task_4_kwh_w_dummies_wide.csv')
df = df.dropna(axis=0, how='any')

#GET TARIFF
tariffs = [v for v in pd.unique(df['tariff']) if v != 'E']
stimuli = [v for v in pd.unique(df['stimulus']) if v != 'E']
tariffs.sort()
stimuli.sort()

# RUN LOGIT-------------
drop = [v for v in df.columns if v.startswith("kwh_2010")]
df_pretrial = df.drop(drop, axis=1)

for i in tariffs:
        for j in stimuli:
            # dummy variables must start with "D_" and consumption variables with "kwh_"
            logit_results, df_logit = do_logit(df_pretrial, i, j, add_D=None, mc=False)

#QUICK MEANS COMPARISON WITH T-TEST BY HAND------------
#creat means
grp = df_logit.groupby('tariff')
df_mean = grp.mean().transpose()
df_mean.B - df_mean.E

# do a t-test "by hand"
df_s = grp.std().transpose()
df_n = grp. count().transpose().mean()
top = df_mean['B'] - df_mean['E']
bottom = np.sqrt(df_s['B']**2/df_n['B'] + df_s['E']**2/df_n['E'])
tstats = top/bottom
sig = tstats[np.abs(tstats) > 2]
sig.name = 't-stats'
