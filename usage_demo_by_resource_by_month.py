from __future__ import print_function

import os

import requests
from pprint import pprint

import pandas as pd

import plotly.offline as py
import plotly.graph_objs as go

## py.init_notebook_mode(connected=False)

##DEFAULT_CCDB_HOST = 'https://ccdb.computecanada.ca'

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
            "start_at":"2018-03-01",
            "end_at": "2019-02-28",
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
py.plot(figure, filename='basic-bar')

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

py.iplot(figure, filename='line_graph', validate=False)
py.plot(figure, filename='line_graph', validate=False)
