import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import datetime
from core import load_last14

# Load last 14 days
dfa = load_last14()
    
# Feature Engineering
dfa['date'] = dfa['date'].str.slice(start = 0, stop = 19)
dfa['date'] = pd.to_datetime(dfa['date'])
dfa['age'] = (pd.to_datetime(datetime.date.today())-dfa['date'])
dfa['age'] = dfa['age'].dt.days
dfa['age'] = dfa['age']+1
dfa = pd.get_dummies(dfa,prefix=['weekday'], columns = ['weekday'])   #One-hot encoder for weekdays
dfa['quad_hour'] = dfa['hour']**2   # hour as quadratic feature

# Setup model
features = dfa[['weekday_0', 'weekday_1', 'weekday_2', 'weekday_3', 'weekday_4', 'weekday_5', 'weekday_6', 'age', 'hour', 'quad_hour']]
model = LinearRegression()
model.fit(features, dfa["diesel"])

# Setup Dataframe to predict the prices of the day
pred_df = pd.DataFrame(columns=['weekday_0', 'weekday_1', 'weekday_2', 'weekday_3', 'weekday_4', 'weekday_5', 'weekday_6', 'age', 'hour', 'quad_hour'])
weekday = datetime.date.today().weekday()
column_name = 'weekday_' + str(weekday)
for i in range(24):
    pred_df.loc[len(pred_df)] = [0, 0, 0, 0, 0, 0, 0, 0, i, i**2]
    pred_df[column_name] = 1

# Output
a = model.predict(pred_df)
df_final = pd.DataFrame()
df_final["diesel"] = a
df_final.plot(use_index=True)
plt.xlabel("Hour of the day")
plt.ylabel("Price")
plt.show()