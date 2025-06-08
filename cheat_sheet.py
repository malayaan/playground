url = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/prc_hicp_manr"
params = {
    'format': 'json',
    'geo': 'FR',
    'coicop': 'CP00',
    'unit': 'T',
    'time': '2010-01'
}
r = requests.get(url, params=params)
r.raise_for_status()
js = r.json()

from pyjstat import pyjstat
df = pyjstat.from_json_stat(js)
print(df.head())