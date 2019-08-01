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

##cpu_df = pd.read_csv( 'cpu_example.csv')
cpu_df = pd.read_csv( 'example_1.csv')

print( "Printing cpu_df in various forms:")
print(cpu_df.head())
print()
print(cpu_df)
print()
print( cpu_df.iloc[0] )
