from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import os

main_dir = "/Users/Vivian/Desktop/Data" 
git_dir = "/Users/Vivian/MPP Fall 2014 & Spring 2015/Big Data/GitHub/PUBPOL590" 
csv_file = "small_data_w_missing_duplicated.csv"

df = pd.read_csv(os.path.join(main_dir, csv_file))

#Inspected data and '-' is a placeholder for missing value
missing = ['.', 'NA', 'NULL', '', '-']
df = pd.read_csv(os.path.join(main_dir, csv_file), na_values = missing)

df.isnull() # pandas method to find missing data; if it returns "True" there's a missing value

df.duplicated() # panda method to find duplicates; "True" is a duplicate
df.drop_duplicates() # this drops true duplicates where EVERYTHING is the same; keeps only 1

df['consump'].isnull() #find subset of full rows of data where consump has missing data

rows = df['consump'].isnull()

df.duplicated(subset = ['panid', 'date']) #finding duplicates under panid and date

##need to drop the missing value for the panid and date subset duplicates
df.duplicated(subset= ['panid', 'date'])
df['consump'].dropna(subset= ['panid', 'date'], axis= 0, how = 'any') #if axis = 0 then we're dropping the ROWS with any missing data
df.dropna(subset = ['panid', 'date'], axis = 0, how = 'any') 

##After cleaning the date, take the mean of the consump variable
df['consump'].mean() 

##SOLUTION##
df1 = df.drop_duplicates()
df1[df1.consump.isnull()] # investigate data where 'consump' is empty (null)
df1[df1.duplicated(['panid', 'date'])] # look at duplicated (first hit from top-bottom) using 'panid' and 'date' as criteria
df1[df1.duplicated(['panid', 'date'], take_last = True)] # same but bottom to top
df2 = df1.drop_duplicates(['panid', 'date'], take_last = True) # this will keep the bottom to top
df2[df2.duplicated(['panid', 'date'])] # check for dups. its empty!<--This checks if you did it correctly
df2.consump.mean() # get mean






