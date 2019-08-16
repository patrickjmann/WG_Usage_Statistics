# Get CC stats from the CCDB utilization api (Chris Want).
# This version included command-line parameters, but otherwise was monolithic.
# See "usage_by_resource_by_month.py" for a later, more organized version
#
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

SCRIPTNAME=sys.argv[0]

## py.init_notebook_mode(connected=False)

##DEFAULT_CCDB_HOST = 'https://ccdb.computecanada.ca'
#===============================================================================
class Options:
    """OLD: Utilization stats for CC systems"""
    start_date_default = datetime.datetime(2019,1,1)
    end_date_default = datetime.datetime.now()

    def test_dates(self):
        if self.end_date <= self.start_date:
            print(CLASSNAME, "ERROR: end_date is before start_date")
            exit(1)

    def get_from_args(self):
        arg_parser = argparse.ArgumentParser(
description =
"OLD: Utilization stats from CCDB api. \
Test the python command-line argument parser. Uses datetime and argparser." )
        start_date_default_str = self.start_date_default.strftime("%Y-%m-%d")
        arg_parser.add_argument( 'start_date', help="start date (default="+start_date_default_str+")", nargs='?', default=start_date_default_str )

        end_date_default_str = self.end_date_default.strftime("%Y-%m-%d")
        arg_parser.add_argument( "end_date", help="end date (default="+end_date_default_str+")", nargs='?', default=end_date_default_str )
        args = arg_parser.parse_args( )
        self.start_date = parser.parse( args.start_date )
        self.end_date = parser.parse( args.end_date )

    def __init__(self):
        self.get_from_args()
        self.CLASSNAME = self.__class__.__name__
        self.test_dates()
        #print( "Class name        = \"", self.CLASSNAME, "\"", sep='' )
        #print( "Class description = \"", self.__doc__, "\"", sep='' )

#===============================================================================
options = Options()
options.get_from_args()

# format date into the usage api format: year-month-date

usage_api_start_date = options.start_date.strftime( "%Y-%m-%d" )
usage_api_end_date = options.end_date.strftime( "%Y-%m-%d" )
print( SCRIPTNAME, "Start date:", usage_api_start_date, " (formatted for usage api (Year-month-day))" )
print( SCRIPTNAME, "End date:  ", usage_api_end_date, " (formatted for usage api (Year-month-day))" )

#===============================================================================
api_key = os.environ.get('USAGE_API_KEY')
if not api_key:
    print( "ERROR: the api key is empty. Check that USAGE_API_KEY has been set.")
    exit(1)

api_host = os.environ.get('USAGE_API_HOST')
if not api_key:
    print( "ERROR: the api host is empty. Check that USAGE_API_HOST has been set.")
    exit(1)

endpoint = api_host + '/api/usage'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token token="%s"' % (api_key)
}
query = {
    "query": {
        "select": [
            "sum_of_core_years"
        ],
        "filter": {
            "start_at":usage_api_start_date,
            "end_at":usage_api_end_date,
        },
        "group_by": [
            "resource",
            "month"
        ]
    },
}

#print("INFO: api_host=", api_host)
#print(endpoint)
#print(headers)
#pprint(query)

print( "INFO: making the request to \"",api_host, "\"" )
response = requests.request('GET', endpoint, json=query, headers=headers)

if response.status_code == 200:
    print( "  successful - received response")
    #pprint(response.json(), depth=5)
else:
    print("Error: %d" % (response.status_code))
    print(response.text)
    exit()

print( "INFO: Load the results into a pandas dataframe")
results = response.json()['results']
df = pd.DataFrame(results).astype({"sum_of_core_years": 'float64',
                                   "month": 'datetime64'}).sort_values(by=['month'])

print( df.head() )
#exit()
#==============================================================================
print( "INFO: Plot bar charts using Plotly")

cedar_df = df[df.resource == "cedar-compute"]
graham_df = df[df.resource == "graham-compute"]
niagara_df = df[df.resource == "niagara-compute"]

cedar = dict(x=cedar_df.month,
             y=cedar_df.sum_of_core_years,
             name='Cedar')
graham = dict(x=graham_df.month,
              y=graham_df.sum_of_core_years,
              name='Graham')
niagara = dict(x=niagara_df.month,
               y=niagara_df.sum_of_core_years,
               name='Niagara')

layout = go.Layout(
    title='Usage by month',
    yaxis=dict(
        title='Core years',
    )
)

data = [
    go.Bar(cedar),
    go.Bar(graham),
    go.Bar(niagara)
]

# iplot is for Jupyter notebooks, plot goes back to the plotly cloud
# -Or direct to the browser

figure=go.Figure(data=data,layout=layout)
#py.iplot(figure, filename='basic-bar')
py.plot(figure, filename='basic-bar.html')

#print( "INFO: exit here for debug purposes")
#exit()
#===============================================================================
print( "INFO: Charting as a line graph" )
data = [
    go.Scatter(cedar),
    go.Scatter(graham),
    go.Scatter(niagara)
]

figure=go.Figure(data=data,layout=layout)

py.iplot(figure, filename='line_graph.html', validate=False)
py.plot(figure, filename='line_graph.html', validate=False)
