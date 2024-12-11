import pandas as pd
from pandas_datareader import data as pdr
import datetime

# Exemple de dataframe avec différentes devises
data = {
    'Date': ['2020-01-02', '2020-01-03', '2020-01-06', '2020-01-02', '2020-01-03', '2020-01-06'],
    'Currency': ['USD', 'USD', 'USD', 'GBP', 'EUR', 'JPY'],
    'Amount': [100, 200, 3000, 150, 250, 5000]
}
df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'])

# Définir la période pour laquelle vous voulez les données
start = datetime.datetime(2020, 1, 1)
end = datetime.datetime(2020, 12, 31)

# Récupérer les taux de change pour USD, GBP, JPY vers EUR
currencies = {
    'USD': 'DEXUSEU',  # EUR to USD
    'GBP': 'DEXUSUK',  # EUR to GBP, using USD to GBP conversion (assuming direct EUR to GBP isn't available)
    'JPY': 'DEXJPUS',  # EUR to JPY, using USD to JPY conversion (assuming direct EUR to JPY isn't available)
}


# Télécharger les données pour chaque taux de change
exchange_rates = pd.DataFrame(index=pd.date_range(start, end))
for currency, symbol in currencies.items():
    rates = pdr.get_data_fred(symbol, start, end)
    rates.rename(columns={symbol: f'{currency}_to_EUR'}, inplace=True)
    rates.index = pd.to_datetime(rates.index)
    exchange_rates = exchange_rates.join(rates)

# Affiche les premières lignes du DataFrame de taux de change
print(exchange_rates.head())

# Joindre les dataframes
df = df.merge(exchange_rates, left_on='Date', right_index=True, how='left')

# Calculer les montants en EUR (Conversion en fonction de la devise)
def convert_to_eur(row):
    rate_column = f'{row["Currency"]}_to_EUR'
    rate = row.get(rate_column)
    if pd.notna(rate) and row["Currency"] != 'EUR':
        return row['Amount'] / rate
    elif row["Currency"] == 'EUR':
        return row['Amount']
    return None

df['Amount_in_EUR'] = df.apply(convert_to_eur, axis=1)

print(df)
