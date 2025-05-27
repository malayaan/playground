# Arrondir les index à la date (sans heure)
vix_df.index = vix_df.index.normalize()
vstoxx_df.index = vstoxx_df.index.normalize()

# Agréger par jour si besoin (moyenne si plusieurs points dans la journée)
vix_df = vix_df.groupby(vix_df.index).mean()
vstoxx_df = vstoxx_df.groupby(vstoxx_df.index).mean()

# Fusion propre
combined = pd.concat([vix_df, vstoxx_df], axis=1).dropna()