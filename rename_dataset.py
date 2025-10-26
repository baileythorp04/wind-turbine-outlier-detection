import pandas as pd
from tools.preprocessing import *

#important columns must be:
#   date and time
#   wind speed
#   power output
#   pitch angle
#   rotor speed
    
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


def kelmarsh(n):
    
    #For new kelmarsh data, remember to remove top 9 empty rows, replace comma with semicolon, and remove Â
    #Then replace all � back to °


    nan_cols = ['Energy Export counter (kWh)', 'Energy Export (kWh)', 'Energy Import (kWh)', 'Energy Import counter (kWh)', 'Lost Production (Contractual Custom) (kWh)', 'Lost Production (Contractual Global) (kWh)', 'Potential power met mast anemometer (kW)', 'Potential power estimated (kW)', 'Potential power met mast anemometer MPC (kW)', 'Time-based Contractual Avail. (Global)', 'Time-based Contractual Avail. (Custom)', 'Production-based Contractual Avail. (Custom)', 'Production-based Contractual Avail. (Global)', 'Reactive Energy Export (kvarh)', 'Reactive Energy Export counter (kvarh)', 'Reactive Energy Import (kvarh)', 'Reactive Energy Import counter (kvarh)', 'Equivalent Full Load Hours counter (s)', 'Production Factor', 'Performance Index', 'Lost Production (Production-based IEC B.2.3) (kWh)', 'Production-based IEC B.2.3 (Users View)']
    important_cols = ["Date and time", "Wind speed (m/s)", "Power (kW)", 'Blade angle (pitch position) A (°)', "Rotor speed (RPM)"]


    data = pd.read_csv(f"data/kelmarsh/{n}_original.csv")
    data = isolate_columns(data, remove=nan_cols) 
    data = rename_columns(data, important_cols)
    data.to_csv(f"data/kelmarsh/{n}.csv", index=False)



def care(n):

    important_cols = ["time_stamp", "wind_speed_3_avg", "power_30_avg", 'sensor_5_avg', "sensor_52_avg"]
# replace sensor_50 with power_30_avg for kW instead of wH

    data = pd.read_csv(f"data/care/{n}_original.csv")

    remove_cols = [col for col in data.columns if col.endswith(('max', 'min', 'std'))]




    data = isolate_columns(data, remove=remove_cols) 
    data = rename_columns(data, important_cols)
    data = remove_extreme_outliers(data)
    data.to_csv(f"data/care/{n}_cutlowrpm.csv", index=False)


#kelmarsh(1)
care(3)

