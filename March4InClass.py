from __future__ import division
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import os
from dateutil import parser # use this to ensure dates are parsed correctly

main_dir = "/Users/Vivian/Desktop/Data/" 
root = main_dir + "Inclass Data/data 2/"

# import data-----------------------
df = pd.read_csv(root + "sample_30min.csv", header=0, parse_dates=[1], date_parser=parser.parse) #we imported a function called parser... then there's an internal method called "parse"
df_assign = pd.read_csv(root + "sample_assignments.csv", usecols = [0,1]) 

# merge
df = pd.merge(df, df_assign)

##add/drop variable
df['year'] = df['date'].apply(lambda x: x.year) 
    #we're applying a lambda-year function to the date to extract the year out of 'date'. 
    #We're telling it to go into the date column and apply the "year" function to the entire column
df['month'] = df['date'].apply(lambda x: x.month) 
df['day'] = df['date'].apply(lambda x: x.day) 
df['ymd'] = df['date'].apply(lambda x: x.date()) #the empty () is important

# daily aggregation
grp = df.groupby(['year', 'month', 'day', 'panid', 'assignment']) #this is the same as the next row
grp = df.groupby(['ymd', 'panid', 'assignment']) 
df1 = grp['kwh'].sum().reset_index() #this is doing three things at once: group by kwh, then sum by the group, and then reset the index

# PIVOT DATA----------------------------
#go from long to wide data

##1. Create column names for wide data
# Create strings names and denote consumption and date
# use ternery expression: [true-expr(x) if condition else false-expr(x) for x in list]; this is just a clean way to write a true/false for loop
#df1['day_str'] = ['0' + str(v) if v <10 else str(v) for v in df1['date']] #add '0' to <10; tacking a 0 in front to preserve the order 
#df1['kwh_ymd'] = 'kwh_' + df1.year.apply(str) + '_' + df1.month.apply(str) +
   # '_' + df1.day_str.apply(str)
   
df1['kwh_ymd'] = 'kwh_' + df1['ymd'].apply(str) # don't need the "0" because the ymd is already preserving the order

#2. Pivot! aka long to wide
df1_piv = df1.pivot('panid', 'kwh_ymd', 'kwh') #i, j, k aka your row, column, and the value

#clean up for making things pretty
df1_piv.reset_index(inplace=True) #this makes panid its own variable
df1_piv.columns.name = None # getting rid of that kwh_ymd name from that top left corner

# MERGE TIME invariant data-------
df2 = pd.merge(df_assign, df1_piv) #this attaching order looks better

## export data for regression
df2.to_csv(root + "07_kwh_wide.csv", sep = ",", index=False) # not exporting the row index value
