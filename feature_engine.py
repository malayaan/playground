import requests

# Fonction pour obtenir le taux de change d'une devise à une date donnée
def get_exchange_rate(date, devise):
    api_url = f"https://api.exchangerate.host/{date}"
    response = requests.get(api_url)
    if response.status_code == 200:
        rates = response.json().get('rates', {})
        return rates.get(devise, None)  # Retourne le taux pour la devise
    else:
        return None

# Exemple : Récupérer les taux pour chaque ligne du DataFrame
def fetch_exchange_rates(row):
    return get_exchange_rate(row['date'].strftime('%Y-%m-%d'), row['devis'])

df['taux'] = df.apply(fetch_exchange_rates, axis=1)

# Calculer les montants convertis
df['montant_converti'] = df['montant'] * df['taux']

print(df)
