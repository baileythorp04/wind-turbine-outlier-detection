# import data
from pyod.models.knn import KNN
import numpy as np
import pandas as pd
from tools.kelmarsh_stopped_removal import remove_stopped_data
from tools.graphing import Three_Curves

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




def remove_extreme_outliers(data : pd.DataFrame):

    data = data.dropna()
    data = data[data['Power (kW)'] > 0 ]
    data = data[data['Pitch angle (°)'] < 20]
    #data = data[data['Rotor speed (RPM)'] > 8] #11 for care, 8 for kelmarsh


    #CARE dataset only
    if 'status_type_id' in data.columns:
        print("CARE exlusive prep happening")
        data = data[(data['status_type_id'].isin([0]))]

        data = data[data['train_test'] == 'train']
        data.drop('train_test', axis='columns', inplace=True)

        data.drop(labels=['asset_id','id','status_type_id'], axis='columns', inplace=True)
    else:
        print("kelmarsh exclusive prep happening")
        data, removed_data = remove_stopped_data(data)
        
        Three_Curves("removed stopped data in blue", inlier_data=removed_data, outlier_data=data, filename="stopped codes plot, less")
        print("stop here")
        

    

    return data

def remove_bad_codes(data, codes):
    pass #filter data by power code = on/safe?


if __name__ == "__main__":
    columns_to_keep = ["Date and time", "Wind speed (m/s)", "Power (kW)", 'Blade angle (pitch position) A (°)', "Rotor speed (RPM)"]
    columns_to_remove = ["Date and time"]
    input_file_name = 'data/kelmarsh_1.csv'
    output_file_name = 'data/kelmarsh_preprocessed.csv'

    data = pd.read_csv(input_file_name)

    #data = isolate_columns(data, remove=columns_to_remove)
    data = remove_extreme_outliers(data)
    #data = remove_bad_codes(data, codes)

    pd.DataFrame.to_csv(data, output_file_name)

