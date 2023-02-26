from core import load_year
import matplotlib.pyplot as plt

df = load_year(16)

daily_mean = df.resample("D").mean(numeric_only=True)
daily_mean.plot(y=["diesel", "e5", "e10"], kind="line")

df_narrow = df[["diesel", "e5", "e10"]]

fig, axs = plt.subplots(figsize=(12,4))
df_narrow_hourly = df_narrow.reset_index()
df_narrow_hourly = df_narrow_hourly.groupby(df_narrow_hourly["date"].dt.hour)["diesel"].mean()
df_narrow_hourly.plot(kind="line",rot=0,ax=axs)
plt.xlabel("Hour of the day")
plt.ylabel("Diesel price")
plt.show()

fig, axs = plt.subplots(figsize=(12,4))
df_narrow_daily = df_narrow.reset_index()
df_narrow_daily = df_narrow_daily.groupby(df_narrow_daily["date"].dt.dayofweek)["diesel"].mean()
df_narrow_daily.plot(kind="line",rot=0,ax=axs)
plt.xlabel("Day of the week")
plt.ylabel("Diesel price")
plt.show()