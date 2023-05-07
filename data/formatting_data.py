#reformat the data
import os
import re

import numpy as np
import pandas as pd


dataset = pd.read_csv('gics.csv')

df = dataset
def get_column_year(df): 
    df = pd.concat([df, pd.get_dummies(df['year'])], axis=1)
    df.rename(columns={2020: '2020', 2021: '2021', 2022: '2022'}, inplace=True)
    return df

# apply function to dataframe
df = get_column_year(df)


# define function to group 'Sector' into 11 GICG sectors
def group_column_sector(df):
    sector_dummies = pd.get_dummies(df['Sector'])
    gicg_sectors = ['Energy', 'Materials', 'Industrials', 'Consumer Discretionary',
                    'Consumer Staples', 'Health Care', 'Financials', 'Information Technology',
                    'Communication Services', 'Utilities', 'Real Estate']
    sector_grouped = pd.DataFrame(columns=gicg_sectors)
    for sector in gicg_sectors:
        if sector in sector_dummies.columns:
            sector_grouped[sector] = sector_dummies[sector]
    return pd.concat([df, sector_grouped], axis=1)

# apply function to dataframe
df = group_column_sector(df)


# create new column with group labels
df['Sharpe_Ratio'] = pd.cut(df['sharpe_ratio'], [-5, 1, float('inf')], labels=[0, 1])




df.drop(['Unnamed: 0', 'year', 'Sector', 'sharpe_ratio'], axis=1, inplace=True)

# finally write
df.to_csv('formatted_gics.csv', index=False)