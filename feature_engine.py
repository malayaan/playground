# Définir une tolérance sur la différence, par exemple 0.1%
# Cela signifie que si |(interest_rate_reference) - (EIR * 100)| < 0.1, on considère que c’est correct.
tolerance = 0.1

# Calcul de la différence
df["difference"] = (df["interest_rate_reference"] - (df["EIR"] * 100)).abs()

# Vérification de la cohérence
df["is_coherent"] = df["difference"] <= tolerance

print(df)