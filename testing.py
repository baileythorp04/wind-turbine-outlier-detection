import pandas as pd
import os
from preprocessing import isolate_columns, remove_extreme_outliers
from outlier_removal import  remove_outliers
from graphing import Three_Curves


n = 1

data = pd.read_csv(f"data/kelmarsh_{n}.csv")
#data = isolate_columns(data, remove=["Date and time"])
#data = remove_extreme_outliers(data)


#data = data[(data['Rotor speed (RPM)'] < 7)]
#data = data[(data['Wind speed (m/s)'] < 3)]

data = isolate_columns(data)

#data = data.dropna()
data = data[data.isna().any(axis=1)]
data = data[data['Power (kW)'] > 0 ]
data = data[data['Blade angle (pitch position) A (°)'] < 20]


pd.DataFrame.to_csv(data, "mid.csv")
data = pd.read_csv("mid.csv")


modifier = "NaN only"
Three_Curves(f"Turbine {n}, {modifier}", data)