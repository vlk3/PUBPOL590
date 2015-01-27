## start with the import 
from pandas import Series, DataFrame
import pandas as pd
import numpy as np

# SET UP FILES -----------------------------------------------------------------------
## create a main directory link and a subpath to file
## NOTE: anything in quotes `" "` is a data type called a 'string'. You should
## ALWAYS make file paths into strings to avoid parsing errors.
main_dir = "/Users/Vivian/MPP Fall 2014 & Spring 2015/Big Data/GitHub/PUBPOL590"
txt_file = "/Assignment1/data/File1_small.txt"

# IMPORT DATA ------------------------------------------------------------------------
## We can import most raw data using the following functions:
# pd.read_csv() -- read .csv values
# pd.read_txt() -- read any 'table' like data, like tab-delimited .txt files
# pd.read_excel() -- read .xls files

## create a dataframe, df, by importing data using panda
pd.read_table(main_dir + txt_file, sep = " ")

## we can assign any object to a variable using the equals sign `=`
df = pd.read_table(main_dir + txt_file, sep = " ") # need to use 'pd.' before using any pandas function

list(df) # this tells you the column name

 # ROW SLICING
## slicing -- using `:` in a data frame
df[60:100] 

# Electricity consumption greater than 30
df.kwh > 30
df[df.kwh >30] 