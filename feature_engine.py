import pandas as pd
from pandas_datareader import data as pdr
import datetime

# Exemple de dataframe avec des dates ajustées pour correspondre aux taux disponibles
data = {
    'Date': ['2020-01-02', '2020-01-03', '2020-01-06'],
    'Currency': ['USD', 'USD', 'USD'],
    'Amount': [100, 200, 3000]
}
df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'])

# Définir la période pour laquelle vous voulez les données (ajustée ici pour l'exemple)
start = datetime.datetime(2020, 1, 1)
end = datetime.datetime(2020, 12, 31)

# Récupérer les taux de change EUR vers USD
exchange_rates = pdr.get_data_fred('DEXUSEU', start, end)

# Affiche les premières lignes du DataFrame de taux de change
print(exchange_rates.head())

# Reformatage de l'index pour la jointure
exchange_rates.index = pd.to_datetime(exchange_rates.index)

# Joindre les dataframes
df = df.merge(exchange_rates, left_on='Date', right_index=True, how='left', suffixes=('', '_rate'))

# Calculer les montants en EUR (Conversion simple USD vers EUR ici)
df['Amount_in_EUR'] = df.apply(lambda x: x['Amount'] / x['DEXUSEU'] if pd.notna(x['DEXUSEU']) else None, axis=1)

print(df)
