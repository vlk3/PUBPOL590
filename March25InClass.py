from __future__ import division
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import os
import time
import matplotlib.pyplot as plt
import pytz
from datetime import datetime, timedelta
from scipy.stats import ttest_ind
import statsmodels.api as sm

main_dir = "/Users/Vivian/Desktop/Data/" 
root = main_dir + "Group Assignment 3/"

# import data-----------------------
df = pd.read_csv(root + "allocation_subsamp.csv")
grp1 = df.groupby(['tariff','stimulus']) 
gd1 = grp1.groups 
## peek at key
gd1.keys()

#need to convert array to a list?

df_1A = df[(df.stimulus == '1') & (df.tariff == 'A')]
df_1B = df[(df.stimulus == '1') & (df.tariff == 'B')]
df_3A = df[(df.stimulus == '3') & (df.tariff == 'A')]
df_3B = df[(df.stimulus == '3') & (df.tariff == 'B')]
df_E = df[(df.stimulus == 'E')]

# I think this creates the 5 vectors... but not with the ID, it's by the index...
gd1[('A', '1')]
gd1[('B', '1')]
gd1[('A', '3')]
gd1[('B', '3')]
gd1[('E', 'E')]


# SET UP DATA ---------------------
np.random.seed(1789)
#df1 = pd.concat([df_1A, df_1B, df_3A, df_3B, df_E])
ids = df['ID']

#set up tariff and stimulus groups
tariff = 
stimulus = 
EE =

# Extract sample size with np.random.choice
# GENERATE RANDOM SAMPLE ASSIGNMENTS ------------------------
sample = np.random.choice(df.index, 300, replace = False) #this extracts 300 sample assignments from the main DF

sampleEE = np.random.choice(df_E.ID.values, 300, replace = False).tolist() #this extracts 300 sample assignments from the control group
sample1A = np.random.choice(df_1A.ID.values, 150, replace = False).tolist()
sample1B = np.random.choice(df_1B.ID.values, 50, replace = False).tolist()
sample3A = np.random.choice(df_3A.ID.values, 150, replace = False).tolist()
sample3B = np.random.choice(df_1A.ID.values, 50, replace = False).tolist()

df_sampleEE = pd.DataFrame(sampleEE)
df_sample1A = pd.DataFrame(sample1A)
df_sample1B = pd.DataFrame(sample1B)
df_sample3A = pd.DataFrame(sample3A)
df_sample3B = pd.DataFrame(sample3B)     

df_sample = pd.concat([df_sampleEE, df_sample1A, df_sample1B, df_sample3A, df_sample3B])
df_sample.columns = ['ID']

df_redux = pd.read_csv(root + "kwh_redux_pretrail.csv")
df_sampleredux = pd.merge(df_sample, df_redux, on= 'ID')





#Monthly Aggregation
grp = df.groupby['year', 'month', 'ID'])