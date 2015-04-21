from __future__ import division
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import os
import statsmodels.api as sm

main_dir = "/Users/Vivian/Desktop/Data/" 
root = main_dir + "Inclass Data/data318/"
paths = [root + v for v in os.listdir(root) if v.startswith("08_")]

# IMPORT AND ADD/DROP VARIABLES---------------
df = pd.read_csv(paths[1], header=0, parse_dates=[1], date_parser=np.datetime64)
df_assign = pd.read_csv(paths[0], header=0)

df['year'] = df['date'].apply(lambda x: x.year)
df['month'] = df['date'].apply(lambda x: x.month)

# MONTHLY AGGREGATION -----------------------
grp = df.groupby(['year', 'month', 'panid']) #unlike the pivot class, we're only grouping by these year, month, and panid
df = grp['kwh'].sum().reset_index() #running without reset index will be a series instead of a dataframe; reset everytime you use groupby

# PIVOT THE DATA-----------------------
df['mo_str'] = ['0' + str(v) if v < 10 else str(v) for v in df['month']] # adds a 0 in front of months before October
df['kwh_ym'] = 'kwh_' + df.year.apply(str) + "_" + df.mo_str.apply(str) # make a column of info called kwh_year_month

df_piv = df.pivot('panid', 'kwh_ym', 'kwh')
df_piv.reset_index(inplace = True)
df_piv.columns.name = None # for aesthetic reasons

#MERGE THE STATIC VALUES (e.g. assignments)--------------------
df = pd.merge(df_assign, df_piv)
del df_piv, df_assign

# GENERATE DUMMY VARIABLES FROM QUALITATIVE DATA (i.e. categories)
## pd.get_dummies() will make dummy vectors for ALL "object" or "category" types
df1 = pd.get_dummies(df, columns = ['gender'])
df1.drop(['gender_M'], axis = 1, inplace=True)

## SET UP DATA FOR LOGIT----------------
kwh_cols = [v for v in df1.columns.values if v.startswith('kwh')]
kwh_cols = [v for v in kwh_cols if int(v[-2:]) <4] #just look at the last two values of the string "kwh_2015_XX" and compare it to less than 4

## 
cols = ['gender_F'] + kwh_cols #here is a list of columns I want 

## SET UP Y, X
y = df1['assignment']
X = df1[cols]
X = sm.add_constant(X)

## LOGIT ------------
logit_model = sm.Logit(y,X)
logit_results = logit_model.fit()
print(logit_results.summary()) ## good news, failed to reject null that there are relationship between the static variable; no systematic diff
