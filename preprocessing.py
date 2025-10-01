# import data
from pyod.models.knn import KNN
import numpy as np
import pandas as pd


# all_data = pd.read_csv('data/Turbine_Data_All.csv')

# important_columns = ["Date and time", "Wind speed (m/s)", "Power (kW)", 'Blade angle (pitch position) A (°)', "Rotor speed (RPM)"]

# filtered_data = all_data[important_columns]
# print(f"head: {filtered_data.columns}")

# pd.DataFrame.to_csv(filtered_data, 'data/Turbine_Data.csv')

# isolate relevant columns:
    # date and time : Date and time
    # wind speed : Wind speed (m/s)
    # power output : Power (kW)
    # pitch angle : Blade angle (pitch position) A (°), Blade angle (pitch position) B (Â°), Blade angle (pitch position) C (Â°)
    # rotor speed : Rotor speed (RPM)

data = pd.read_csv('data/Turbine_Data.csv')
print(data.shape)
data = data.dropna()
print(data.shape)
data = data[data['Power (kW)'] > 0 ]
print(data.shape)
data = data[data['Blade angle (pitch position) A (°)'] < 20]
print(data.shape)

#pd.DataFrame.to_csv(data, 'data/Turbine_Data_preprocessed.csv')




#maybe some pre-processing of removing negative values 
#remove if:
    # pitch > 20
    # power is negative
    # any missing value

#knn = KNN()

# do data cleaning 
# do KNN, SVM, SVM-KNN to see if I get similar results with ROC-AUC and mAP tests

# create a NBM. with MLP or autoencoder/DBN? I thought KNN
# test the NBM with RMSE, R^2, MAE
# run models. hyperparameters?