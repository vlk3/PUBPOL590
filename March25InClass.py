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

main_dir = "/Users/Vivian/Desktop/Data/" 
root = main_dir + "Group Assignment 3/"

# import data-----------------------
df = pd.read_csv(root + "allocation_subsamp.csv")
grp1 = df.groupby(['tariff','stimulus']) 
gd1 = grp1.groups 


#need to convert array to a list

dfA1 = df[(df.stimulus == '1') & (df.stimulus == ' 
df.ID.values

## peek at key
gd1.keys()




seed([1789])