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


    for col in remove:
        if col in data.columns:
            data = data.drop(labels=col, axis='columns')
        

    if len(keep) > 0:
        data = data[keep]

    

    return data

def rename_columns(data : pd.DataFrame,  important_cols):
    #rename date&time and the 4 graphed columns
    correct_important_cols = ["Date and time", "Wind speed (m/s)", "Power (kW)", 'Pitch angle (°)', "Rotor speed (RPM)"]
    if len(important_cols) == len(correct_important_cols):
        for old_col, new_col in zip(important_cols, correct_important_cols):
            data.rename(columns={old_col: new_col}, inplace=True)
    else:
        print("Error: Did not provide exactly 5 important columns to rename to standard names")
    return data


def remove_extreme_outliers(data):

    data = data.dropna()
    data = data[data['Power (kW)'] > 0 ]
    data = data[data['Pitch angle (°)'] < 20]

    return data

def remove_bad_codes(data, codes):
    pass #filter data by power code = on/safe?


if __name__ == "__main__":
    columns_to_keep = ["Date and time", "Wind speed (m/s)", "Power (kW)", 'Blade angle (pitch position) A (°)', "Rotor speed (RPM)"]
    columns_to_remove = ["Date and time"]
    input_file_name = 'data/kelmarsh_1.csv'
    output_file_name = 'data/kelmarsh_preprocessed.csv'

    data = pd.read_csv(input_file_name)

    data = isolate_columns(data, remove=columns_to_remove)
    data = remove_extreme_outliers(data)
    #data = remove_bad_codes(data, codes)

    pd.DataFrame.to_csv(data, output_file_name)

