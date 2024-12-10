# feature_engineering.py

import numpy as np
import pandas as pd

def create_features(df: pd.DataFrame) -> pd.DataFrame:
    # Copie du DF pour ne pas modifier l'original
    df = df.copy()
    
    #------------------------------
    # Vérifications de croissance et cohérence temporelle
    #------------------------------
    # Ces features supposent l'existence de colonnes 'XXX' et 'XXX_PRVS' pour comparer l'année en cours à l'année précédente

    # EBITDA Growth
    if 'EBITDA' in df.columns and 'EBITDA_PRVS' in df.columns:
        df['EBITDA_growth'] = np.where(df['EBITDA_PRVS'] != 0,
                                       (df['EBITDA'] - df['EBITDA_PRVS']) / df['EBITDA_PRVS'].abs(),
                                       np.nan)

    # Equity Growth
    if 'EQTY' in df.columns and 'EQTY_PRVS' in df.columns:
        df['EQTY_growth'] = np.where(df['EQTY_PRVS'] != 0,
                                     (df['EQTY'] - df['EQTY_PRVS']) / df['EQTY_PRVS'].abs(),
                                     np.nan)

    # Turnover Growth
    if 'ANNL_TURNR' in df.columns and 'ANNL_TURNR_PRVS' in df.columns:
        df['TURNOVER_growth'] = np.where(df['ANNL_TURNR_PRVS'] != 0,
                                         (df['ANNL_TURNR'] - df['ANNL_TURNR_PRVS']) / df['ANNL_TURNR_PRVS'].abs(),
                                         np.nan)

    # Net Income Growth
    if 'NT_INCM' in df.columns and 'NT_INCM_PRVS' in df.columns:
        df['NT_INCM_growth'] = np.where(df['NT_INCM_PRVS'] != 0,
                                        (df['NT_INCM'] - df['NT_INCM_PRVS']) / df['NT_INCM_PRVS'].abs(),
                                        np.nan)

    #------------------------------
    # Cohérence entre variables liées
    #------------------------------
    # LVRG_diff = |(GRP_NET_DEBT/EBITDA) - LVRG|
    if all(col in df.columns for col in ['GRP_NET_DEBT','EBITDA','LVRG']):
        df['LVRG_diff'] = np.where(df['EBITDA'] != 0,
                                   np.abs((df['GRP_NET_DEBT'] / df['EBITDA']) - df['LVRG']),
                                   np.nan)

    # ND_consistency = |GRP_TTL_DST - CSH - GRP_NET_DEBT|
    if all(col in df.columns for col in ['GRP_TTL_DST','CSH','GRP_NET_DEBT']):
        df['ND_consistency'] = np.abs(df['GRP_TTL_DST'] - df['CSH'] - df['GRP_NET_DEBT'])

    # DBT_SRVC_RT cohérence avec EBITDA et TTL_INTRST_PD
    # Implied_DBTSR = EBITDA / TTL_INTRST_PD
    if all(col in df.columns for col in ['EBITDA','TTL_INTRST_PD','DBT_SRVC_RT']):
        df['Implied_DBTSR'] = np.where(df['TTL_INTRST_PD'] != 0,
                                       df['EBITDA'] / df['TTL_INTRST_PD'],
                                       np.nan)
        df['DBTSR_diff'] = np.abs(df['DBT_SRVC_RT'] - df['Implied_DBTSR'])

    #------------------------------
    # Flags pour valeurs négatives anormales
    #------------------------------
    if 'EBITDA' in df.columns:
        df['EBITDA_negative_flag'] = (df['EBITDA'] < 0).astype(int)

    if 'EQTY' in df.columns:
        df['EQTY_negative_flag'] = (df['EQTY'] < 0).astype(int)

    if 'CSH' in df.columns:
        df['CSH_negative_flag'] = (df['CSH'] < 0).astype(int)

    #------------------------------
    # Vous pouvez ajouter d'autres features de data quality ici
    # par exemple, check des valeurs extrêmes, outliers, etc.
    #------------------------------

    return df


# Dans votre notebook Jupyter
import pandas as pd
from feature_engineering import create_features

# Supposons que votre DataFrame s'appelle df
df_enriched = create_features(df)

# Maintenant df_enriched contient les nouvelles colonnes dérivées
df_enriched.head()
