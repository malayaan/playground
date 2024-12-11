import pandas as pd
from pandas_datareader import data as pdr
import datetime

# Example data with multiple currencies
data = {
    'Date': ['2020-01-02', '2020-01-03', '2020-01-06', '2020-01-02', '2020-01-03', '2020-01-06', '2020-01-02', '2020-01-03'],
    'Currency': ['USD', 'GBP', 'EUR', 'JPY', 'AUD', 'CAD', 'CHF', 'PLN'],
    'Amount': [100, 150, 250, 5000, 300, 450, 200, 600]
}
df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'])

# Define the date range for exchange rate data
start = datetime.datetime(2020, 1, 1)
end = datetime.datetime(2020, 12, 31)

# List of currencies with corresponding FRED symbols
currencies = {
    'EUR': None,  # Base currency
    'USD': 'DEXUSEU',
    'GBP': 'DEXUSUK',
    'JPY': 'DEXJPUS',
    'AUD': 'DEXUSAL',
    'CAD': 'DEXCAUS',
    'CHF': 'DEXSZUS',
    'PLN': 'DEXUSEU',  # Convert via USD (EUR > USD > PLN)
    'CZK': 'DEXCZUS',
    'NOK': 'DEXNOUS',
    'SEK': 'DEXSDUS',
    'HKD': 'DEXHKUS',
    'SGD': 'DEXSIUS',
    'RUB': 'DEXRUS',
    'TRY': 'DEXTUUS',
    'MAD': None,  # Not available in FRED
    'DZD': None,  # Not available in FRED
    'XPF': None,  # Not available in FRED
    'RON': None,  # Not available in FRED
    'XOF': None,  # Not available in FRED
    'XAF': None,  # Not available in FRED
    'VES': None,  # Not available in FRED
    'TND': None,  # Not available in FRED
    'MGA': None,  # Not available in FRED
    'SYP': None,  # Not available in FRED
    'HUF': 'DEXUSEU',  # Convert via USD (EUR > USD > HUF)
    'PEN': None,  # Not available in FRED
    'EGP': None,  # Not available in FRED
    'IQD': None,  # Not available in FRED
    'AED': None,  # Not available in FRED
    'QAR': None,  # Not available in FRED
}

# Download exchange rates from FRED
def fetch_exchange_rates():
    exchange_rates = pd.DataFrame(index=pd.date_range(start, end))
    for currency, symbol in currencies.items():
        if symbol:
            try:
                rates = pdr.get_data_fred(symbol, start, end)
                rates.rename(columns={symbol: f'{currency}_to_EUR'}, inplace=True)
                rates.index = pd.to_datetime(rates.index)
                exchange_rates = exchange_rates.join(rates, how='left')
            except Exception as e:
                print(f"Could not fetch data for {currency}: {e}")
    return exchange_rates

# Fetch exchange rates
df_exchange_rates = fetch_exchange_rates()
print(df_exchange_rates.head())

# Merge exchange rates with the main DataFrame
df = df.merge(df_exchange_rates, left_on='Date', right_index=True, how='left')

# Function to convert amounts to EUR
def convert_to_eur(row):
    if row['Currency'] == 'EUR':
        return row['Amount']
    rate_column = f"{row['Currency']}_to_EUR"
    rate = row.get(rate_column)
    if pd.notna(rate):
        return row['Amount'] / rate
    return None

df['Amount_in_EUR'] = df.apply(convert_to_eur, axis=1)

# Display the final DataFrame
print(df)

# Handle missing rates for unsupported currencies (optional step)
def handle_missing_rates(row):
    if pd.isna(row['Amount_in_EUR']):
        print(f"Missing exchange rate for {row['Currency']} on {row['Date']}")
        # Optionally, add fallback logic here

df.apply(handle_missing_rates, axis=1)
