''' This code demonstrates how to call data using the Census Bureau's
Application Program Interface (API)!

If it says the code won't run because you need to install dependencies, ChatGPT should be able to walk you through the process.'''

import requests
import pandas as pd

url = r'https://api.census.gov/data/2021/acs/acs5/profile?get=NAME,GEO_ID,DP04_0089E&for=tract:*&in=state:12&in=county:031' # r means read
myData = (requests.get(url)).json() # parse data into json format so it can be used with python

column_names = myData[0] 
df = pd.DataFrame(columns=column_names, data=myData[1:]) # set first row as column names, convert to dataframe
print(df)

file_path = r'C:\Users\Shawna\Documents\UF\output.csv' # paste the file path of the location on YOUR computer where you want to save your data
# ^I saved mine to a folder called UF in my documents.  "output" is what I named the file, this file does not have to already exist
df.to_csv(file_path, index=False) # save data as csv to the specified location

'''Now that you have a dataframe, you can start cleaning and transforming your data.  
See the .py code in shawnadean/indicators-inclusive-prosperity on github for an extensive example'''



# Extras 
'''
# Create a function that puts the data into a dataframe to enable code reusability
class ACS:
    def __init__(self, api):
        self.api = api
        
    def toDataFrame(self):
        data = requests.get(self.api).json()
        column_names = data[0]
        df = pd.DataFrame(columns=column_names, data=data[1:]).drop(['state','county','tract'], axis=1)
        return df 
        
df = ACS(r'https://api.census.gov/data/2021/acs/acs5/profile?get=NAME,GEO_ID,DP04_0089E&for=tract:*&in=state:12&in=county:031').toDataFrame()


# Use string concatenation for enhanced code readability
median_home_value_cd = 'DP04_0089E'
state_cd = '12'
county_cd = '031'

df = ACS(r'https://api.census.gov/data/2021/acs/acs5/profile?get=NAME,GEO_ID,' +
         median_home_value_cd + '&for=tract:*&in=state:' +
         state_cd + '&in=county:' +
         county_cd).toDataFrame()
         
# Use dictionaries, concatenation, and loops to combine data from multiple API calls into one table (but don't compare overlapping 5-year estimates)
column_codes = {
    2010: {'home_ownership': 'DP04_0045PE' , 'vacancy': 'DP04_0003PE'},
    2011: {'home_ownership': 'DP04_0045PE' , 'vacancy': 'DP04_0003PE'},
    2012: {'home_ownership': 'DP04_0045PE' , 'vacancy': 'DP04_0003PE'},
    2013: {'home_ownership': 'DP04_0045PE' , 'vacancy': 'DP04_0003PE'},
    2014: {'home_ownership': 'DP04_0045PE' , 'vacancy': 'DP04_0003PE'}, 
    2015: {'home_ownership': 'DP04_0046PE' , 'vacancy': 'DP04_0003PE'},
    2016: {'home_ownership': 'DP04_0046PE' , 'vacancy': 'DP04_0003PE'},
    2017: {'home_ownership': 'DP04_0046PE' , 'vacancy': 'DP04_0003PE'},
    2018: {'home_ownership': 'DP04_0046PE' , 'vacancy': 'DP04_0003PE'},
    2019: {'home_ownership': 'DP04_0046PE' , 'vacancy': 'DP04_0003PE'}, 
    2020: {'home_ownership': 'DP04_0046PE' , 'vacancy': 'DP04_0003PE'},
    2021: {'home_ownership': 'DP04_0046PE' , 'vacancy': 'DP04_0003PE'}
}

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

print(df)


# Save the output file to the user's current directory (the folder where this program is saved), this avoids having to manually update the file path
import os
file_path = os.path.join(os.getcwd(), 'output.csv')
df.to_csv(file_path, index=False)
print('Done! Your file has been saved to: ' + file_path)
'''






