import pandas as pd
from datetime import datetime, timedelta

def remove_stopped_data(data : pd.DataFrame):
    codes = pd.read_csv("data/kelmarsh/codes/codes_kelmarsh_1.csv")

    bad_datetimes = []
    code_date_format = "%Y-%m-%d %H:%M:%S"


    for index, row in codes.iterrows():
        if (row['Service contract category'] == "External stop (low wind speed)  (5)"):
            datetime_obj = datetime.strptime(row['Timestamp start'], code_date_format)
            
            bad_datetimes.append(datetime_obj)
    
    latest_bad_datetime_index = 0
    removed_rotor_speeds = []
    rows_to_remove = []

    data_date_format = "%d/%m/%Y %H:%M"

    for index, row in data.iterrows():
        row_datetime = datetime.strptime(row['Date and time'], data_date_format)

        if row_datetime > bad_datetimes[latest_bad_datetime_index] + timedelta(minutes=30): #but if more than 30 minutes after, move to next bad_datetime
                latest_bad_datetime_index += 1
                continue
        
        if row_datetime > bad_datetimes[latest_bad_datetime_index]: #if this row is after the next bad datetime:
            rows_to_remove.append(index) 
            removed_rotor_speeds.append(row['Rotor speed (RPM)'])
            latest_bad_datetime_index += 1 #and move on to the next bad datetime

        if latest_bad_datetime_index >= len(bad_datetimes):
            break
        
    removed_data = data.loc[data.index.isin(rows_to_remove)]

    data.drop(rows_to_remove, inplace=True)



    print(f"Rows removed from stopping: {len(removed_rotor_speeds)}")

    return data, removed_data



#for each line in status_data which says "External stop (low wind speed)  (5)"
#   remove the line from input_data which immediately follows it