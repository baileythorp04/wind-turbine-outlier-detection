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


#
def isolate_columns(data : pd.DataFrame, keep=[], remove=[]):

    nan_cols = ['Energy Export counter (kWh)', 'Energy Export (kWh)', 'Energy Import (kWh)', 'Energy Import counter (kWh)', 'Lost Production (Contractual Custom) (kWh)', 'Lost Production (Contractual Global) (kWh)', 'Potential power met mast anemometer (kW)', 'Potential power estimated (kW)', 'Potential power met mast anemometer MPC (kW)', 'Time-based Contractual Avail. (Global)', 'Time-based Contractual Avail. (Custom)', 'Production-based Contractual Avail. (Custom)', 'Production-based Contractual Avail. (Global)', 'Reactive Energy Export (kvarh)', 'Reactive Energy Export counter (kvarh)', 'Reactive Energy Import (kvarh)', 'Reactive Energy Import counter (kvarh)', 'Equivalent Full Load Hours counter (s)', 'Production Factor', 'Performance Index']
    #nan_cols = []
    for col in nan_cols:
        if col in data.columns:
            data = data.drop(labels=col, axis='columns')
        

    if len(keep) > 0:
        data = data[keep]
    
    if len(remove) > 0:
        data = data.drop(labels=remove, axis='columns')

    return data

def remove_extreme_outliers(data):

    data = data.dropna()
    data = data[data['Power (kW)'] > 0 ]
    data = data[data['Blade angle (pitch position) A (°)'] < 20]

    return data

def remove_bad_codes(data, codes):
    pass #filter data by power code = on/safe?


if __name__ == "__main__":
    columns_to_keep = ["Date and time", "Wind speed (m/s)", "Power (kW)", 'Blade angle (pitch position) A (°)', "Rotor speed (RPM)"]
    columns_to_remove = ["Date and time"]
    input_file_name = 'data/kelmarsh_2.csv'
    output_file_name = 'data/RECOV_kelmarsh_preprocessed.csv'

    data = pd.read_csv(input_file_name)

    data = isolate_columns(data, remove=columns_to_remove)
    data = remove_extreme_outliers(data)
    #data = remove_bad_codes(data, codes)

    pd.DataFrame.to_csv(data, output_file_name)

