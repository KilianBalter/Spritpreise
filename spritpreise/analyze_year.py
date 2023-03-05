from core import load_year
import pandas as pd
import matplotlib.pyplot as plt
import functools as ft

# Warning: 2022 data must already be downloaded in ../Data/RawData/2022-prices and ../Data/RawData/2022-stations
#          About 10GB RAM required
# Load every 16th datapoint of 2022
df = load_year(16)

# Calculate average price per day over whole year
daily_mean = df.resample("D").mean(numeric_only=True)
daily_mean.plot(y=["diesel", "e5", "e10"], kind="line", figsize=(12,5), ylim=0, ylabel="Price", xlabel="")

df_narrow = df[["diesel", "e5", "e10"]]

# Calculate average prices per hour over whole year
fig, axs = plt.subplots(figsize=(12,4))
df_narrow_hourly = df_narrow.reset_index()
df_narrow_hourly = df_narrow_hourly.groupby(df_narrow_hourly["date"].dt.hour)["diesel"].mean()
df_narrow_hourly.plot(kind="line",rot=0,ax=axs)
plt.xlabel("Hour of the day")
plt.ylabel("Diesel price")

# Calculate average price per day over whole year
fig, axs = plt.subplots(figsize=(12,4))
df_narrow_daily = df_narrow.reset_index()
df_narrow_daily = df_narrow_daily.groupby(df_narrow_daily["date"].dt.dayofweek)["diesel"].mean()
df_narrow_daily.plot(kind="line",rot=0,ax=axs)
plt.xlabel("Day of the week")
plt.ylabel("Diesel price")

# Calculate average price per hour per day over whole year
# Monday
df_narrow_hourly_monday = df_narrow.copy()
df_narrow_hourly_monday['dateBackup'] = df_narrow_hourly_monday.index
df_narrow_hourly_monday = df_narrow_hourly_monday[df_narrow_hourly_monday['dateBackup'].dt.dayofweek == 0]
df_narrow_hourly_monday = df_narrow_hourly_monday.groupby(df_narrow_hourly_monday["dateBackup"].dt.hour)["diesel"].mean()

# Tuesday
df_narrow_hourly_tuesday = df_narrow.copy()
df_narrow_hourly_tuesday['dateBackup'] = df_narrow_hourly_tuesday.index
df_narrow_hourly_tuesday = df_narrow_hourly_tuesday[df_narrow_hourly_tuesday['dateBackup'].dt.dayofweek == 1]
df_narrow_hourly_tuesday = df_narrow_hourly_tuesday.groupby(df_narrow_hourly_tuesday["dateBackup"].dt.hour)["diesel"].mean()

# Wednesday
df_narrow_hourly_wednesday = df_narrow.copy()
df_narrow_hourly_wednesday['dateBackup'] = df_narrow_hourly_wednesday.index
df_narrow_hourly_wednesday = df_narrow_hourly_wednesday[df_narrow_hourly_wednesday['dateBackup'].dt.dayofweek == 2]
df_narrow_hourly_wednesday = df_narrow_hourly_wednesday.groupby(df_narrow_hourly_wednesday["dateBackup"].dt.hour)["diesel"].mean()

# Thursday
df_narrow_hourly_thursday = df_narrow.copy()
df_narrow_hourly_thursday['dateBackup'] = df_narrow_hourly_thursday.index
df_narrow_hourly_thursday = df_narrow_hourly_thursday[df_narrow_hourly_thursday['dateBackup'].dt.dayofweek == 3]
df_narrow_hourly_thursday = df_narrow_hourly_thursday.groupby(df_narrow_hourly_thursday["dateBackup"].dt.hour)["diesel"].mean()

# Friday
df_narrow_hourly_friday = df_narrow.copy()
df_narrow_hourly_friday['dateBackup'] = df_narrow_hourly_friday.index
df_narrow_hourly_friday = df_narrow_hourly_friday[df_narrow_hourly_friday['dateBackup'].dt.dayofweek == 4]
df_narrow_hourly_friday = df_narrow_hourly_friday.groupby(df_narrow_hourly_friday["dateBackup"].dt.hour)["diesel"].mean()

# Saturday
df_narrow_hourly_saturday = df_narrow.copy()
df_narrow_hourly_saturday['dateBackup'] = df_narrow_hourly_saturday.index
df_narrow_hourly_saturday = df_narrow_hourly_saturday[df_narrow_hourly_saturday['dateBackup'].dt.dayofweek == 5]
df_narrow_hourly_saturday = df_narrow_hourly_saturday.groupby(df_narrow_hourly_saturday["dateBackup"].dt.hour)["diesel"].mean()

# Sunday
df_narrow_hourly_sunday = df_narrow.copy()
df_narrow_hourly_sunday['dateBackup'] = df_narrow_hourly_sunday.index
df_narrow_hourly_sunday = df_narrow_hourly_sunday[df_narrow_hourly_sunday['dateBackup'].dt.dayofweek == 6]
df_narrow_hourly_sunday = df_narrow_hourly_sunday.groupby(df_narrow_hourly_sunday["dateBackup"].dt.hour)["diesel"].mean()

# Combine
monday = pd.DataFrame({'hour':df_narrow_hourly_monday.index, 'monday':df_narrow_hourly_monday.values})
tuesday = pd.DataFrame({'hour':df_narrow_hourly_tuesday.index, 'tuesday':df_narrow_hourly_tuesday.values})
wednesday = pd.DataFrame({'hour':df_narrow_hourly_wednesday.index, 'wednesday':df_narrow_hourly_wednesday.values})
thursday = pd.DataFrame({'hour':df_narrow_hourly_thursday.index, 'thursday':df_narrow_hourly_thursday.values})
friday = pd.DataFrame({'hour':df_narrow_hourly_friday.index, 'friday':df_narrow_hourly_friday.values})
saturday = pd.DataFrame({'hour':df_narrow_hourly_saturday.index, 'saturday':df_narrow_hourly_saturday.values})
sunday = pd.DataFrame({'hour':df_narrow_hourly_sunday.index, 'sunday':df_narrow_hourly_sunday.values})

dfs = [monday, tuesday, wednesday, thursday, friday, saturday, sunday]
df_final = ft.reduce(lambda left, right: pd.merge(left, right, on='hour'), dfs)

ax = df_final.plot(y=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'], figsize=(12,4))
ax.set_ylabel('Diesel Price')
ax.set_xlabel('Hour of the day')

# Show all plots
plt.show()