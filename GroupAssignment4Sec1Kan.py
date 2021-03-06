from __future__ import division
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import os
from scipy.stats import ttest_ind


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
#create means
grp = df_logit.groupby('tariff')
df_mean = grp.mean().transpose()
df_mean.C - df_mean.E

# do a t-test "by hand"
df_s = grp.std().transpose()
df_n = grp. count().transpose().mean()
top = df_mean['C'] - df_mean['E']
bottom = np.sqrt(df_s['C']**2/df_n['C'] + df_s['E']**2/df_n['E'])
tstats = top/bottom
sig = tstats[np.abs(tstats) > 2]
sig.name = 't-stats'

##-----------------------------------------------------------------------------------------------------------##
## SECTION 2 ##
df_logit['p_val'] = logit_results.predict() # get predicted values of the logit model in Section 1

df_logit['trt'] = 0 + (df_logit['tariff'] == 'C') #this generates a treatment variable

df_logit['w'] = np.sqrt((df_logit['trt']/df_logit['p_val']) + (1-df_logit['trt'])/(1-df_logit['p_val'])) #page 46 in Harding PDF;

df_w = df_logit[['ID', 'trt', 'w']] #create smaller dataframe with just IDs, trt, and weights

##-------------------------------------------------------------------------------------------------------##
## SECTION 3 ##
os.chdir(main_dir)
from fe_functions import *

df = pd.read_csv(main_dir + 'task_4_kwh_long.csv')
df = df.dropna(axis=0, how='any')

df2 = pd.merge(df, df_w) # merge df and the smaller dataframe from Section 2
df2['TP'] = df2.trt.apply(str) + df2.trial.apply(str) #generating a trt and trial interaction; refer to 08_logit_and_fixed_effects_models

df2['log_kwh'] = (df2['kwh'] + 1).apply(np.log) # +1 is used to account for zero consumption values
df2['mo_str'] = np.array(["0" + str(v) if v < 10 else str(v) for v in df2['month']]) #0 is for adding a zero in front of January-September

df2['ym'] = df2['year'].apply(str) + "_" + df2['mo_str'] #concatenate to make ym a string

#Set up variables from the merged dataframe (df2)
y = df2['log_kwh']
P = df2['trial'] > 0 #trial indicator; ** COMPARE WITH PEIZHI'S CODES
TP = df2['TP']
w = df2['w']
mu = pd.get_dummies(df2['ym'], prefix = 'ym').iloc[:, 1:-1]
X = pd.concat([TP, P, mu], axis=1)

#Demeaning time!

ids = df2['ID']
y = demean(y, ids)

#Run FE without AND with weights---------------
## WITHOUT WEIGHTS
fe_model = sm.OLS(y, X) # linearly prob model
fe_results = fe_model.fit() # get the fitted values
print(fe_results.summary()) # print pretty results (no results given lack of obs)

# WITH WEIGHTS
## apply weights to data
y = y*w # weight each y
nms = X.columns.values # save column names
X = np.array([x*w for k, x in X.iteritems()]) # weight each X value
X = X.T # transpose (necessary as arrays create "row" vectors, not column)
X = DataFrame(X, columns = nms) # update to dataframe; use original names

fe_w_model = sm.OLS(y, X) # linearly prob model
fe_w_results = fe_w_model.fit() # get the fitted values
print(fe_w_results.summary()) # print pretty results (no results given lack of obs)

