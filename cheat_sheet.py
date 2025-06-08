import requests
import pandas as pd

url = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/prc_hicp_manr/FR.CP00.T.T.INX"
params = {
    'format': 'json-stat',
    'startPeriod': '2010-01'
}
r = requests.get(url, params=params)
r.raise_for_status()
js = r.json()

# json-stat → pandas
# pip install pyjstat
898-0from pyjstat import pyjstat 
898-1df = pyjstat.from_json_stat(js) 
898-2print(df.head())