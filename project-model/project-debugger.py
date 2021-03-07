import requests
import pandas as pd
import io

url = "https://api.covidtracking.com/v1/states/ny/daily.csv"  # API Call for NY data

try:
    s = requests.get(url).content
    df = pd.read_csv(io.StringIO(s.decode('utf-8')))

    if df.values.size < 3:  # ensure DF has values (may just contain 2 error values)
        raise FileNotFoundError("No data in API")
    else:
        df.to_csv('ny_covid_data.csv', index=False)  # future proof in case api goes down
        df = pd.read_csv(io.StringIO(s.decode('utf-8')))

except FileNotFoundError as fnf_error:
    df = pd.read_csv("ny_covid_data.csv")  # read from most recently fetched data
except: # catch any other unexpected error
    df = pd.read_csv("ny_covid_data.csv")

# Format dates
df['date'] =  pd.to_datetime(df['date'], format='%Y%m%d')

limitPer = len(df) * .90
df = df.dropna(thresh=limitPer, axis=1)

# Exclude unnecessary attributes
df.drop(['dateChecked', 'dateModified'],axis=1,inplace=True)
df = df.loc[:, (df != 0).any(axis=0)]

# Impute NaN values
df.fillna(value=-1, inplace=True)

# To check null values in data
df.isnull().sum()




