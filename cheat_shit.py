import pandas as pd

# 1. Lecture des fichiers Excel avec Pandas

# Chargement de deux feuilles Excel (choisir `engine="openpyxl"` pour éviter de lire les formules)
df_employees = pd.read_excel("employees.xlsx", sheet_name="Employees", engine="openpyxl")
df_sales = pd.read_excel("sales.xlsx", sheet_name="Sales", engine="openpyxl")

# Visualiser les premières lignes
print("Employés:")
print(df_employees.head())
print("\nVentes:")
print(df_sales.head())

# 2. Sélectionner des colonnes spécifiques pour la fusion

# Garder uniquement les colonnes pertinentes pour chaque DataFrame
df_employees_selected = df_employees[["Employee_ID", "Name", "Department", "Country"]]
df_sales_selected = df_sales[["Sale_ID", "Employee_ID", "Product", "Amount", "Date"]]

# 3. Fusionner les données sur la colonne Employee_ID

# Fusion des données d'employés et de ventes
df_merged = pd.merge(df_sales_selected, df_employees_selected, on="Employee_ID", how="inner")
print("\nDonnées Fusionnées:")
print(df_merged.head())

# 4. Concaténer des données additionnelles

# Ajout de nouvelles ventes (exemple de nouvelles données)
new_sales = pd.DataFrame({
    "Sale_ID": [101, 102],
    "Employee_ID": [1, 3],
    "Product": ["Product_X", "Product_Y"],
    "Amount": [1500, 2300],
    "Date": ["2023-10-01", "2023-10-02"]
})

# Concaténer les nouvelles ventes au DataFrame fusionné
df_merged = pd.concat([df_merged, new_sales], ignore_index=True)
print("\nDonnées après concaténation:")
print(df_merged.tail())

# 5. Mapping pour transformer des valeurs

# Créer un dictionnaire pour mapper les codes de pays en noms de pays
country_map = {
    "USA": "United States",
    "CAN": "Canada",
    "FRA": "France",
    "DEU": "Germany"
}

# Appliquer le mapping pour convertir les codes de pays en noms complets
df_merged["Country"] = df_merged["Country"].map(country_map)
print("\nDonnées après mapping des pays:")
print(df_merged[["Employee_ID", "Country"]].drop_duplicates())

# 6. Groupby pour analyser les données

# Calculer le montant total des ventes par pays et produit
sales_summary = df_merged.groupby(["Country", "Product"]).agg(
    total_sales=("Amount", "sum"),
    average_sales=("Amount", "mean"),
    sale_count=("Sale_ID", "count")
).reset_index()

print("\nRésumé des ventes par pays et produit:")
print(sales_summary)

# 7. Ajouter des colonnes calculées et réorganiser les colonnes

# Calculer une colonne de taxe (ex. 5%) sur le montant des ventes
df_merged["Tax"] = df_merged["Amount"] * 0.05

# Ajouter une colonne "Revenue" avec la somme de l'Amount et de la Tax
df_merged["Revenue"] = df_merged["Amount"] + df_merged["Tax"]

# Réorganiser les colonnes pour que Revenue soit à la fin
columns_order = ["Sale_ID", "Employee_ID", "Name", "Department", "Country", "Product", "Amount", "Tax", "Revenue", "Date"]
df_merged = df_merged[columns_order]

print("\nDonnées après ajout et réorganisation des colonnes:")
print(df_merged.head())

# 8. Filtrer selon des caractéristiques spécifiques

# Exemple : filtrer les ventes au-dessus de 2000 et pour les employés du département "Sales"
filtered_df = df_merged[(df_merged["Amount"] > 2000) & (df_merged["Department"] == "Sales")]

print("\nVentes filtrées (montant > 2000 et département 'Sales'):")
print(filtered_df)

# 9. Sauvegarder le résultat final dans un fichier Excel

# Sauvegarde du DataFrame fusionné et filtré dans un nouveau fichier Excel
with pd.ExcelWriter("final_sales_report.xlsx", engine="openpyxl") as writer:
    df_merged.to_excel(writer, sheet_name="All_Data", index=False)
    sales_summary.to_excel(writer, sheet_name="Sales_Summary", index=False)
    filtered_df.to_excel(writer, sheet_name="Filtered_Sales", index=False)

print("\nLes données finales ont été sauvegardées dans 'final_sales_report.xlsx'.")
