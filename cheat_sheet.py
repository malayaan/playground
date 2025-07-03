# Étape 1 : Agrégation des données
grouped_data = catalogue.groupby([group_column, 'NB_GRP_VHC'])['MNT_PRX_VNT_TTC'].sum().reset_index()
total_by_group = grouped_data.groupby(group_column)['MNT_PRX_VNT_TTC'].sum().reset_index()
total_by_group.rename(columns={'MNT_PRX_VNT_TTC': 'Valeur Percée'}, inplace=True)

# Ajouter la colonne "Group EAD" si sort_by == 'Groupe EAD'
if sort_by == 'Groupe EAD':
    total_by_group['Group EAD'] = catalogue.groupby(group_column)['Groupe EAD'].first().reset_index()['Groupe EAD']

# Fusionner les données agrégées avec le pourcentage
grouped_data = grouped_data.merge(total_by_group, on=group_column)
grouped_data['PERCENT'] = (grouped_data['MNT_PRX_VNT_TTC'] / grouped_data['Valeur Percée']) * 100