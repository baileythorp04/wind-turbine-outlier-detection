import pandas as pd
import os
from preprocessing import isolate_columns, remove_extreme_outliers
from outlier_removal import  remove_outliers_KNN
from graphing import Three_Curves


n = 1

data = pd.read_csv(f"data/kelmarsh_{n}.csv")
#data = isolate_columns(data, remove=["Date and time"])
#data = remove_extreme_outliers(data)


data = data[(data['Rotor speed (RPM)'] < 7)]


modifier = "low rotor speed only"
Three_Curves(f"Turbine {n}, {modifier}", data)