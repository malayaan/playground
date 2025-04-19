import yfinance as yf

# Télécharger les données de la Société Générale
socgen = yf.download("GLE.PA", start="2015-01-01", end="2024-12-31")

# Afficher les 5 premières lignes
print(socgen.head())