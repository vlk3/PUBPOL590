from __future__ import division ## this always returns a float if it's not a whole number and you use division
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import os

main_dir = "/Users/Vivian/Desktop/Data" 
git_dir = "/Users/Vivian/MPP Fall 2014 & Spring 2015/Big Data/GitHub/PUBPOL590" 
csv2= "sample_assignments.csv"
csv1= "small_data_w_missing_duplicated.csv"

##IMPORT DATA-----
df1 = pd.read_csv(os.path.join(main_dir, csv1), na_values = ['-', 'NA'])
df2 =pd.read_csv(os.path.join(main_dir, csv2))

# CLEAN DATA---------
##clean df1 (refer back to online demo 03)
df1 = df1.drop_duplicates()
df1 = df1.drop_duplicates(['panid', 'date'], take_last = True)

##clean df2
df2[[0,1]]
df2 = df2[[0,1]] #reassigning df2 to subset#

## COPY DATAFRAMES-------------
df3 = df2 # creates a link/reference (alter df2 DOES affect df3); look at line 33
df4 = df2.copy() #creating a copy (alter df2 does NOT affect df4); this WILL KEEP A COPY no matter what you do to the original; this double your data and probably shouldn't do that with big data

# REPLACING DATA-----------
df2.group.replace(['T', 'C'], [1,0]) #sequence of replacement is important; 1 replaces T and 0 replaces C. But df2 has not been changed.
df2.group = df2.group.replace(['T', 'C'], [1,0]) #the "group" part is important ##Note: can't run this line and the last line together!

df3 ## df2 and df3 are assigned internally to the same dataframe; we changed df2 in the previous two lines, so df3 automatically 
                ##changes as well even though we have explicitly made changes to df3

## MERGING ----------------
pd.merge(df1, df2) #attaching df2 to df1; "many-to-one' merge using the intersection, automatically finds the keys it has in common
                    ## the "key" is the panid here and will merge on panel id
pd.merge(df1, df2, on = ['panid']) #this tells specifically the merging criteria, aka the key
pd.merge(df1, df2, on = ['panid'], how = 'inner') ##this keeps only the intersection of the keys
pd.merge(df1, df2, on = ['panid'], how = 'outer') ##this takes the union of the keys, so that's why it keeps panid 5

df5= pd.merge(df1, df2, on = ['panid'])

## STACKING AND BINDING (aka ROW BINDS AND COLUMN BINDS)-------
df2
df4

## 'row bind'
pd.concat([df2, df4]) # the default is to row bind aka axis = 0
pd.concat([df2, df4], axis = 0) # same as above
pd.concat([df2, df4], axis = 0, ignore_index = True) # 'ignore_index = False' is default; so instead of 0-4, the DF now shows 0-9

## 'column bind'
pd.concat([df2, df4], axis = 1) # same as above

