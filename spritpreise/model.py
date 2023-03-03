import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import date

def load(f_prices, f_stations):
    # Load and tidy the prices csv
    dfp = pd.read_csv(f_prices)
    dfp = dfp.drop(columns=['dieselchange','e5change','e10change'])
    dfp = dfp.rename(columns={'station_uuid': 'uuid'})

    # Load and tidy the stations csv
    dfs = pd.read_csv(f_stations)
    dfs = dfs.drop(columns=['name','first_active','openingtimes_json','street','house_number'])

    # join stations and prices
    dfa = dfs.set_index('uuid').join(dfp.set_index('uuid'))

    # Delete false Values
    dfa = dfa.dropna()
    dfa = dfa.drop(dfa[dfa.longitude < 5].index)
    dfa = dfa.drop(dfa[dfa.longitude > 16].index)
    dfa = dfa.drop(dfa[dfa.latitude < 48].index)
    dfa = dfa.drop(dfa[dfa.latitude > 56].index)
    dfa = dfa.drop(dfa[dfa.diesel <= 0].index)

    # Split the Timestamp
    dfa['weekday'] = pd.to_datetime(dfa.date)
    dfa['weekday'] = dfa['weekday'].dt.dayofweek
    dfa['year'] = pd.DatetimeIndex(dfa['date']).year
    dfa['month'] = pd.DatetimeIndex(dfa['date']).month
    dfa['day'] = pd.DatetimeIndex(dfa['date']).day
    dfa['hour'] = pd.DatetimeIndex(dfa['date']).hour
    dfa['minute'] = pd.DatetimeIndex(dfa['date']).minute
    
    return dfa

# Load last two weeks 
dfa = load('data/02/2023-02-10-prices.csv','data/02/2023-02-10-stations.csv')
prices = 'data/02/2023-02-10-prices.csv'
stations = 'data/02/2023-02-10-stations.csv'
for i in range(14):
    prices = 'data/02/2023-02-10-prices.csv'
    stations = 'data/02/2023-02-10-stations.csv'
    date = '2023-02-' +str(11+i)
    df = load(prices.replace('2023-02-10',date,1),stations.replace('2023-02-10',date,1))
    dfa = pd.concat([dfa,df], ignore_index=True)

# Feature Engineering
dfa['date'] = dfa['date'].str.slice(start = 0, stop = 19)
dfa['date'] = pd.to_datetime(dfa['date'])
dfa['age'] = (pd.to_datetime(date.today())-dfa['date'])
dfa['age'] = dfa['age'].dt.days
dfa['age'] = dfa['age']+1
dfa = pd.get_dummies(dfa,prefix=['weekday'], columns = ['weekday'])   #One-hot encoder for weekdays
dfa['quad_hour'] = dfa['hour']**2   # hour as quadratic feature



# Modell aufsetzen
features = dfa[['weekday_0', 'weekday_1', 'weekday_2', 'weekday_3', 'weekday_4', 'weekday_5', 'weekday_6', 'age', 'hour', 'quad_hour']]
model = LinearRegression()
model.fit(features, dfa["diesel"])


#Setup Dataframe to predict the prices of the day
pred_df = pd.DataFrame(columns=['weekday_0', 'weekday_1', 'weekday_2', 'weekday_3', 'weekday_4', 'weekday_5', 'weekday_6', 'age', 'hour', 'quad_hour'])
weekday = date.today().weekday()
column_name = 'weekday_' + str(weekday)
for i in range(24):
    pred_df.loc[len(pred_df)] = [0, 0, 0, 0, 0, 0, 0, 0, i, i**2]
    pred_df[column_name] = 1


#Output
a = model.predict(pred_df)
print(a)