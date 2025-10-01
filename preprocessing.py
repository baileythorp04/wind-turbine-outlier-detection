# import data
from pyod.models.knn import KNN
import numpy as np
import pandas as pd

# isolate relevant columns:
    # date and time : Date and time
    # wind speed : Wind speed (m/s)
    # power output : Power (kW)
    # pitch angle : Blade angle (pitch position) A (°), Blade angle (pitch position) B (Â°), Blade angle (pitch position) C (Â°)
    # rotor speed : Rotor speed (RPM)

#them remove bad data if:
        # pitch > 20
        # power is negative
        # any missing value

def preprocess_data(columns, input_file, output_file):
    all_data = pd.read_csv(input_file)

    filtered_data = all_data[columns]
    print(f"head: {filtered_data.columns}")

    #pd.DataFrame.to_csv(filtered_data, 'data/Turbine_Data.csv')
    #filtered_data = pd.read_csv('data/Turbine_Data.csv')


    print(filtered_data.shape)
    data = filtered_data.dropna()
    print(data.shape)
    data = data[data['Power (kW)'] > 0 ]
    print(data.shape)
    data = data[data['Blade angle (pitch position) A (°)'] < 20]
    print(data.shape)

    pd.DataFrame.to_csv(data, 'data/Turbine_Data_preprocessed.csv')


columns_to_keep = ["Date and time", "Wind speed (m/s)", "Power (kW)", 'Blade angle (pitch position) A (°)', "Rotor speed (RPM)"]
input_file_name = 'data/Turbine_Data_All.csv'
output_file_name = 'data/Turbine_Data_Preprocessed.csv'

preprocess_data(columns_to_keep, input_file_name, output_file_name)