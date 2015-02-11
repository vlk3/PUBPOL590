from __future__ import division
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import os

main_dir = "/Users/Vivian/Desktop/Data/" 
git_dir = "/Users/Vivian/MPP Fall 2014 & Spring 2015/Big Data/GitHub/PUBPOL590" 

## ADVANCED PATHING
root = main_dir + "Group Assignment/"
#paths0 = [root + "File" + str(v) + ".txt" for v in range (1,7)]

## Pathing the Pro Way
[v for v in os.listdir(root)]
[os.path.join(root, v) for v in os.listdir(root)]
[root + v for v in os.listdir(root)]
[root + v for v in os.listdir(root) if v.startswith("File")]
[v for v in os.listdir(root) if v.startswith("File")]
paths1= [root + v for v in os.listdir(root) if v.startswith("File")]

## IMPORTING DATA

list_of_dfs = [ pd.read_table(v, skiprows = 6000000, nrows = 1500000, sep = " ", names = ['ID', 'DAYHH', 'kwh'], na_values = ['-', 'NA', 'NULL', '', '.','999999999','9999999']) for v in paths1]
                        #I think this works
                        
#pd.read_table('/Users/Vivian/Desktop/Data/Group Assignment/File1.txt', skiprows = 6000000, nrows = 1500000, sep = " ", names = ['ID', 'DAYHH', 'kwh'] for v in paths1)
                        #indicating that the files are space delimited, skips 6 mil and import next 1.5mil, gives you a proper header
                        #May not actually need this...

# STACK DATA (aka row bind) + EXTRACTING DAYS AND HOURS
df = pd.concat(list_of_dfs, ignore_index = True)
df1 = pd.concat(list_of_dfs, ignore_index = True)
df1['HH'] = df1['DAYHH'] %100
df1 = df1[['ID', 'DAYHH', 'HH', 'kwh']] #this rearrange the columns
cols = list(df1.columns.values) #this gets you the list of columns
#run cols and then df1 to test the rearranged colums; this 


# CLEANING DATA
df2 = df1.drop_duplicates(['ID', 'DAYHH']) #no dup observed
df2 = df2[['ID', 'DAYHH', 'HH', 'kwh']] 
df2.isnull()

## Finding DLS-affected data
dls = df2[df2['HH'].isin([49, 50])]
        #this returns 2822 rows; meaning 2822 observations have hours 49 and 50 due to DLS

## MERGING
df_allocation = pd.read_csv(root + "SME and Residential allocations.csv",usecols = ['ID','Code','Residential - Tariff allocation','Residential - stimulus allocation','SME allocation'],na_values = ['-', 'NA', 'NULL', '', '.'])
df3 = df_allocation.rename(columns = {'Residential - Tariff allocation':'RES_Tariff','Residential - stimulus allocation':'RES_Stimulus', 'SME allocation':'SME'})
df4 = pd.merge(df2, df3, on = 'ID')
    #Notes: Code 3 is possibly problematic; refer to codebook

## cleaning the missing/duplicates
df4.duplicates(['ID','DAYHH'])
df4.drop_duplicates(['ID','DAYHH'])