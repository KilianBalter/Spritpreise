# -*- coding: utf-8 -*-
import os
from pathlib import Path
import datetime
import pandas as pd

# Get DataFrame containing every n(subset)-th row of data from 2022
def load_year(subset = 1):
    # If data has been read before return stored Dataframe
    try:
        year_file = Path("../Data/TidyData/year.pkl.xz")
        if(year_file.is_file):
            print("Found previously loaded file.")
            return pd.read_pickle(year_file, compression="infer")
    except:
        print("File not found, loading data...")

    prices_path = "../Data/RawData/2022-prices/"
    stations_path = "../Data/RawData/2022-stations/"
    directory_prices = os.fsencode(prices_path)
    directory_stations = os.fsencode(stations_path)

    dfa = pd.DataFrame()

    prices_2022 = os.listdir(directory_prices)
    stations_2022 = os.listdir(directory_stations)

    joined = []

    # Iterate through month folders
    for i in range(0,12):
        full_path_prices = prices_path + os.fsdecode(prices_2022[i]) + "/"
        full_path_stations = stations_path + os.fsdecode(prices_2022[i]) + "/"
        prices_month = os.listdir(os.fsencode(prices_path + os.fsdecode(prices_2022[i])))
        stations_month = os.listdir(os.fsencode(stations_path + os.fsdecode(stations_2022[i])))

        # Iterate through daily CSVs in month folder
        for j in range(0,len(prices_month)):
            filename_price = os.fsdecode(prices_month[j])
            filename_station = os.fsdecode(stations_month[j])

            # Load and tidy price and station CSV
            dfp = tidy_prices(pd.read_csv(full_path_prices + os.fsdecode(prices_month[j])))
            dfs = tidy_stations(pd.read_csv(full_path_stations + os.fsdecode(stations_month[j])))
            
            # Join them
            dfa = dfs.set_index('uuid').join(dfp.set_index('uuid'))
            dfa = dfa.dropna()
            
            # Convert index to DateTimeIndex using date column
            dfa["uuid"] = dfa.index
            dfa.index = pd.to_datetime(dfa["date"].str[:19])
            dfa["hour"] = pd.DatetimeIndex(dfa['date']).hour
            dfa = dfa.drop(columns=["date"])
            dfa = dfa.sort_index()

            if(subset != 1):
                dfa = dfa.iloc[::subset]

            joined.append(dfa)

        print("Finished loading month: ", i+1)
    # Concatenate all daily Dataframes into one
    full_df = pd.concat(joined)
    # Store dataframe so it can be read quickly if needed again
    full_df.to_pickle("../Data/TidyData/year.pkl.xz", compression="infer")
    return full_df



# Get DataFrame containing data from the last 14 days
def load_last14():
    dfa = pd.DataFrame()

    base_url = "https://dev.azure.com/tankerkoenig/362e70d1-bafa-4cf7-a346-1f3613304973/_apis/git/repositories/0d6e7286-91e4-402c-af56-fa75be1f223d/items?path="
    params = "&versionDescriptor%5BversionOptions%5D=0&versionDescriptor%5BversionType%5D=0&versionDescriptor%5Bversion%5D=master&resolveLfs=true&%24format=octetStream&api-version=5.0&download=true"

    # Get last 14 days of price and station data and tidy it
    for i in range(14):
        _date = datetime.date.today() - datetime.timedelta(days=i+1)
        year = _date.strftime("%Y")
        month = _date.strftime("%m")
        day = _date.strftime("%d")
        url_prices = base_url+"/prices/" + year + "/" + month + "/" + year + "-" + month + "-" + day + "-prices.csv" + params
        url_stations = base_url+"/stations/" + year + "/" + month + "/" + year + "-" + month + "-" + day + "-stations.csv" + params
        df_prices = tidy_prices(pd.read_csv(url_prices))
        df_stations = tidy_stations(pd.read_csv(url_stations))

        # Join them
        df_joined = df_stations.set_index('uuid').join(df_prices.set_index('uuid'))
        df_joined.dropna(inplace=True)

        # Split the Timestamp
        df_joined['weekday'] = pd.to_datetime(df_joined.date)
        df_joined['year'] = df_joined['weekday'].dt.year
        df_joined['month'] = df_joined['weekday'].dt.month
        df_joined['day'] = df_joined['weekday'].dt.day
        df_joined['hour'] = df_joined['weekday'].dt.hour
        df_joined['minute'] = df_joined['weekday'].dt.minute
        df_joined['weekday'] = df_joined['weekday'].dt.dayofweek

        # Concatenate into full df
        dfa = pd.concat([dfa,df_joined], ignore_index=True)
        print("Loaded:", _date, "Remaining:", 13-i)

    return dfa



def tidy_prices(df):
    # Drop unneeded columns
    df = df.drop(columns=['dieselchange','e5change','e10change'])
    df = df.rename(columns={'station_uuid': 'uuid'})
    # Drop negative values
    df = df.drop(df[df.diesel <= 0].index)
    return df

def tidy_stations(df):
    # Drop unneeded columns
    df = df.drop(columns=['name','first_active','openingtimes_json','street','house_number'])
    # Drop false values
    df = df.drop(df[df.longitude < 5].index)
    df = df.drop(df[df.longitude > 16].index)
    df = df.drop(df[df.latitude < 48].index)
    df = df.drop(df[df.latitude > 56].index)
    return df