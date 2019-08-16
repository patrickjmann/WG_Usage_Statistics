# Read a CUB dump into a Panda dataframe
# and do some graphing

from __future__ import print_function
import sys
import argparse
import datetime
from dateutil import parser
import os

import requests
from pprint import pprint

import pandas as pd

import plotly.offline as py
import plotly.graph_objs as go

##full_df = pd.read_csv( 'cpu_example.csv')
full_df = pd.read_csv( 'example_1.csv')
#full_df = pd.read_csv( 'example_simple.csv')

#print( "# of key-value pairs =", len(full_df))
print( "Keynames (Columns) are: ")
i = 0
for x in full_df:
    i += 1
    print(i, ": ", x, sep='')

print("The index is\n", full_df.index )
print("The columns are\n", full_df.columns)

print()
print( "Printing cpu_df in various forms:")
#print(full_df.head())
#print()
print("full_df:\n",full_df)
print()
print( "full_df.iloc[0] (row 0):\n", full_df.iloc[0] )

print()
print( "x and y in full_df.items:")
for x,y in full_df.items():
    print("x=",x)
    print("y=(see below)\n", y)

print()
acol = full_df.iloc[:,0]  # first column - returns a Series
print("acol.index=", acol.index)
print("acol[1]=", acol[1])

print( "acol keynames:")
for x in acol:
    print("x=",x)

print( acol )

#print()
#print(acol)
#cpu_df = pd.DataFrame(full_df[0]) # errors out
#cpu_df = pd.DataFrame(full_df.loc[0,"This is a simple examplefile."])
#cpu_df = pd.DataFrame(full_df.iloc[:,0])
#print(cpu_df)
#for x,y in cpu_df.items():
#    print("x=",x,"\ny=\n",y)
