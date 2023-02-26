# -*- coding: utf-8 -*-
import os
from pathlib import Path
import pandas as pd

def load_year(subset = 1):
    #If data ha been read before return stored Dataframe
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

    #Iterate through month folders
    for i in range(0,12):
        full_path_prices = prices_path + os.fsdecode(prices_2022[i]) + "/"
        full_path_stations = stations_path + os.fsdecode(prices_2022[i]) + "/"
        prices_month = os.listdir(os.fsencode(prices_path + os.fsdecode(prices_2022[i])))
        stations_month = os.listdir(os.fsencode(stations_path + os.fsdecode(stations_2022[i])))

        #Iterate through daily CSVs in month folder
        for j in range(0,len(prices_month)):
            filename_price = os.fsdecode(prices_month[j])
            filename_station = os.fsdecode(stations_month[j])

            #Load and tidy price and station CSV
            dfp = tidy_prices(pd.read_csv(full_path_prices + os.fsdecode(prices_month[j])))
            dfs = tidy_stations(pd.read_csv(full_path_stations + os.fsdecode(stations_month[j])))
            
            #Join them
            dfa = dfs.set_index('uuid').join(dfp.set_index('uuid'))
            dfa = dfa.dropna()
            
            #Convert index to DateTimeIndex using date column
            dfa["uuid"] = dfa.index
            dfa.index = pd.to_datetime(dfa["date"].str[:19])
            dfa["hour"] = pd.DatetimeIndex(dfa['date']).hour
            dfa = dfa.drop(columns=["date"])
            dfa = dfa.sort_index()

            if(subset != 1):
                dfa = dfa.iloc[::subset]

            joined.append(dfa)

        print("Finished loading month: ", i+1)
    #Concatenate all daily Dataframes into one
    full_df = pd.concat(joined)
    #Store dataframe so it can be read quickly if needed again
    full_df.to_pickle("../Data/TidyData/year.pkl.xz", compression="infer")
    return full_df

def tidy_prices(df):
    df = df.drop(columns=['dieselchange','e5change','e10change'])
    df = df.rename(columns={'station_uuid': 'uuid'})
    df = df.drop(df[df.diesel <= 0].index)
    return df

def tidy_stations(df):
    df = df.drop(columns=['name','first_active','openingtimes_json','street','house_number'])
    df = df.drop(df[df.longitude < 5].index)
    df = df.drop(df[df.longitude > 16].index)
    df = df.drop(df[df.latitude < 48].index)
    df = df.drop(df[df.latitude > 56].index)
    return df