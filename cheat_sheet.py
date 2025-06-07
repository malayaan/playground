import pandasdmx

# On utilise le package pandasdmx qui est fait pour les API de données SDMX comme Eurostat
# pip install pandasdmx

# Initialiser le client
from pandasdmx import Request
estat = Request('ESTAT')

# Exemple : récupérer la liste des datasets disponibles
response = estat.dataflow()
for key in list(response.dataflow.keys())[:10]:
    print(key)

# Exemple : charger un dataset (par exemple l'inflation HICP)
# ici prc_hicp_manr : Harmonised Indices of Consumer Prices (Monthly rate of change)
ds_response = estat.data(resource_id='prc_hicp_manr', key='M.M.I8.000000.4.INX', params={'startPeriod': '2010-01'})

# Extraire les données en pandas dataframe
df = ds_response.to_pandas()

# Visualiser
print(df.head())