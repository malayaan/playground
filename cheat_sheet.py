import requests
import pandas as pd
import matplotlib.pyplot as plt

# Fonction utilitaire
def get_hicp_data():
    url = 'https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/prc_hicp_manr/M.FR.CP00.T.T.INX'
    params = {
        'format': 'sdmx-json',
        'startPeriod': '2010-01'
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    
    # Parsing
    series = data['data']['dataSets'][0]['series']
    obs_dim = data['structure']['dimensions']['observation'][0]['id']
    obs_values = data['structure']['dimensions']['observation'][0]['values']
    
    rows = []
    for series_key, series_data in series.items():
        for obs_key, obs in series_data['observations'].items():
            obs_time = obs_values[int(obs_key)]['id']
            obs_value = obs[0]
            rows.append({'date': obs_time, 'HICP_FR': obs_value})
    
    df = pd.DataFrame(rows)
    df = df.sort_values('date')
    return df

# Charger les données
df_filtered = get_hicp_data()

# Visualiser
print(df_filtered.head())

# Plot rapide
plt.figure(figsize=(10, 5))
plt.plot(df_filtered['date'], df_filtered['HICP_FR'], marker='o')
plt.title('Inflation HICP France (CP00 - Total)')
plt.xlabel('date')
plt.ylabel('HICP (Monthly rate of change)')
plt.grid()
plt.show()