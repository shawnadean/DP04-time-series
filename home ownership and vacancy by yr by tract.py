'''
This program collects the homeownership and vacancy rate from each year of the census from 2010-2021
and inserts this data into 1 table.

Note: GEO_IDs/census tract boundaries change every decade
'''

# Set this file path to a local folder on your computer:
output_file_path = r'C:\Users\Shawna\Documents\UF\Philanthropies\AIS Fall 2023\Jax Housing Indicators by Tract 2010-2021.csv'

import pandas as pd
import requests
import numpy as np

# Map correct column codes for home ownership and vacancy rate to each year
column_codes = {
    2010: {'home_ownership': 'DP04_0045PE' , 'vacancy': 'DP04_0003PE'},
    2011: {'home_ownership': 'DP04_0045PE' , 'vacancy': 'DP04_0003PE'},
    2012: {'home_ownership': 'DP04_0045PE' , 'vacancy': 'DP04_0003PE'},
    2013: {'home_ownership': 'DP04_0045PE' , 'vacancy': 'DP04_0003PE'},
    2014: {'home_ownership': 'DP04_0045PE' , 'vacancy': 'DP04_0003PE'}, # Gross Rent: DP04_0132E
    2015: {'home_ownership': 'DP04_0046PE' , 'vacancy': 'DP04_0003PE'},
    2016: {'home_ownership': 'DP04_0046PE' , 'vacancy': 'DP04_0003PE'},
    2017: {'home_ownership': 'DP04_0046PE' , 'vacancy': 'DP04_0003PE'},
    2018: {'home_ownership': 'DP04_0046PE' , 'vacancy': 'DP04_0003PE'},
    2019: {'home_ownership': 'DP04_0046PE' , 'vacancy': 'DP04_0003PE'}, # Gross Rent: DP04_0134E
    2020: {'home_ownership': 'DP04_0046PE' , 'vacancy': 'DP04_0003PE'},
    2021: {'home_ownership': 'DP04_0046PE' , 'vacancy': 'DP04_0003PE'}
}


# Extract data from each year's API and insert into a data frame
df = pd.DataFrame(columns=['Year', 'GEO_ID','Home-Ownership Rate', 'Vacancy Rate'])

for year, codes in column_codes.items():
    
    api = ('https://api.census.gov/data/'
           + str(year) +'/acs/acs5/profile?get=GEO_ID,' 
           + codes['home_ownership'] + ',' 
           + codes['vacancy'] 
           + '&for=tract:*&in=state:12&in=county:031')
    data = requests.get(api).json() 
    
    for row in data:
        if row[0] == 'GEO_ID':
            continue         
        record = [year, row[0], row[1], row[2]]
        df_record = pd.DataFrame([record], columns=df.columns)
        df = pd.concat([df, df_record], ignore_index=True)       


# Clean data
dtype_mapping = {
    "Year": int,
    "Home-Ownership Rate": float,
    "Vacancy Rate": float
}
df = df.astype(dtype_mapping)

df[['Home-Ownership Rate', 'Vacancy Rate']] = df[['Home-Ownership Rate', 'Vacancy Rate']].apply(lambda x: x / 100)

mask = df == -6666666.660
df = df.mask(mask, np.nan)

# Export to csv
df.to_csv(output_file_path, index=False)
print('Program run successfully! Go to', output_file_path, 'to view your file!')





