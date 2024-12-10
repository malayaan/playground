import pandas as pd
import numpy as np

def transform_dataframe(df):
    """
    Transforme un DataFrame en ajoutant de nouvelles colonnes définies par des calculs spécifiques.
    :param df: Le DataFrame d'entrée contenant les colonnes nécessaires.
    :return: Le DataFrame modifié avec les nouvelles colonnes ajoutées.
    """
    # Vérifie la présence des colonnes avant chaque calcul
    if {'BREACH_COV', 'COVENANT_STATUS'}.issubset(df.columns):
        df['breach_covenant_coherence'] = df['BREACH_COV'] == df['COVENANT_STATUS']

    if {'OFF_BLNC_SHT_AMNT_INSTRMNT', 'OUTSTNDG_NMNL_AMNT_INSTRMNT'}.issubset(df.columns):
        df['total_loan_amount'] = df['OFF_BLNC_SHT_AMNT_INSTRMNT'] + df['OUTSTNDG_NMNL_AMNT_INSTRMNT']

    if {'Montant_tot_du_prêt', 'TYP_INSTRMNT'}.issubset(df.columns):
        df['average_loan_ratio'] = df.groupby('TYP_INSTRMNT')['Montant_tot_du_prêt'].transform('mean')

    if {'EIR', 'EIR_INCPTN'}.issubset(df.columns):
        df['interest_rate_diff'] = df['EIR'] - df['EIR_INCPTN']

    if 'CSH_SWP_TRP' in df.columns:
        df['bool_cash_trat_sweet'] = df['CSH_SWP_TRP'].replace(['N/A', np.nan], 'NouvelleCatégorie').astype('category')

    if {'BRCHD_CVNTS', 'CSH_SWP_TRP'}.issubset(df.columns):
        df['Brchd_cvnts_coherence'] = (
            (~df['BRCHD_CVNTS'].isin(['No Breach', 'MISS'])) &
            (~df['CSH_SWP_TRP'].isin(['N', 'N/A']))
        )

    if {'LTV', 'EIR_INCPTN'}.issubset(df.columns):
        df['ltv_diff'] = df['LTV'] - df['EIR_INCPTN']

    if {'PRFRMNG_STTS', 'LTV'}.issubset(df.columns):
        df['prfmng_stts_coherence'] = (df['PRFRMNG_STTS'] == 1) & (df['LTV'] > 100)

    if {'DT_RFRCNC', 'DT_INCPTN'}.issubset(df.columns):
        df['difference_days'] = (pd.to_datetime(df['DT_RFRCNC']) - pd.to_datetime(df['DT_INCPTN'])).dt.days

    if {'EBITDA', 'EBITDA_PRVS'}.issubset(df.columns):
        df['ebitda_diff'] = df['EBITDA'] - df['EBITDA_PRVS']

    if {'EBITDA', 'EBITDA_PRVS', 'GRP_EBITDA'}.issubset(df.columns):
        df['ebitda_diff_ratio'] = (df['EBITDA'] - df['EBITDA_PRVS']) / df['GRP_EBITDA']

    if {'CSH', 'CSH_PRVS'}.issubset(df.columns):
        df['cash_diff'] = df['CSH'] - df['CSH_PRVS']

    if {'TTL_DBT', 'TTL_DBT_PRVS'}.issubset(df.columns):
        df['ttl_dbt_diff'] = df['TTL_DBT'] - df['TTL_DBT_PRVS']

    if {'NT_INCM', 'NT_INCM_PRVS'}.issubset(df.columns):
        df['nt_incm_diff'] = df['NT_INCM'] - df['NT_INCM_PRVS']

    if {'LVRG', 'LVRG_PRVS'}.issubset(df.columns):
        df['lvrg_diff'] = df['LVRG'] - df['LVRG_PRVS']

    if {'TTL_DBT', 'CSH', 'EBITDA'}.issubset(df.columns):
        df['lvrg_theorical_deviation'] = (df['TTL_DBT'] - df['CSH']) / df['EBITDA']

    if {'EBITDA', 'TTL_INTRST_PD'}.issubset(df.columns):
        df['interest_coverage_ratio'] = df['EBITDA'] / df['TTL_INTRST_PD']

    if {'GRP_EBITDA', 'EBITDA'}.issubset(df.columns):
        df['coherence_ebitda'] = df['GRP_EBITDA'] / df['EBITDA'] > 0

    if {'GRP_EQTY', 'EQTY'}.issubset(df.columns):
        df['coherence_eqty'] = df['GRP_EQTY'] / df['EQTY'] > 0

    if {'GRP_NT_DBT', 'NT_DBT'}.issubset(df.columns):
        df['coherence_nt_debt'] = df['GRP_NT_DBT'] / df['NT_DBT'] > 0

    if {'GRP_TTL_DBT', 'TTL_DBT'}.issubset(df.columns):
        df['coherence_ttl_debt'] = df['GRP_TTL_DBT'] / df['TTL_DBT'] > 0

    return df
