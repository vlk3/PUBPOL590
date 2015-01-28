# Using Series and DataFrame from pandas; shorthand for pandas and numpy
from pandas import Series, DataFrame
import pandas as pd
import numpy as np

#Setting up the file path (quotations marks are important especially because there are spaces in my path

main_dir = "/Users/Vivian/MPP Fall 2014 & Spring 2015/Big Data/GitHub/PUBPOL590"
txt_file = "/Assignment1/data/File1_small.txt"

# First step: import the data from github
## Then create a dataframe, df, by importing data using panda
# Don't forget to indicate that it's spaced delimited
pd.read_table(main_dir + txt_file, sep = " ")

df = pd.read_table(main_dir + txt_file, sep = " ") 

list(df) # this tells you the column name

 # ROW SLICING
## slicing -- using `:` in a data frame
df[60:100] 

# Electricity consumption greater than 30
df.kwh > 30
df[df.kwh >30] 