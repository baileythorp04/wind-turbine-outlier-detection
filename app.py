from process import process_data



#file structure for data is:
# data/{dataset}/{turbine number}.csv



def kelmarsh():
    #For new kelmarsh data, remember to remove top 9 empty rows, replace comma with semicolon, and remove Â
    #Then replace all � back to °

    n = 1 #turbine number
    dataset = "kelmarsh" #kelmarsh, care
    model = "SVMKNN" #KNN, SVMKNN

    nan_cols = ['Energy Export counter (kWh)', 'Energy Export (kWh)', 'Energy Import (kWh)', 'Energy Import counter (kWh)', 'Lost Production (Contractual Custom) (kWh)', 'Lost Production (Contractual Global) (kWh)', 'Potential power met mast anemometer (kW)', 'Potential power estimated (kW)', 'Potential power met mast anemometer MPC (kW)', 'Time-based Contractual Avail. (Global)', 'Time-based Contractual Avail. (Custom)', 'Production-based Contractual Avail. (Custom)', 'Production-based Contractual Avail. (Global)', 'Reactive Energy Export (kvarh)', 'Reactive Energy Export counter (kvarh)', 'Reactive Energy Import (kvarh)', 'Reactive Energy Import counter (kvarh)', 'Equivalent Full Load Hours counter (s)', 'Production Factor', 'Performance Index', 'Lost Production (Production-based IEC B.2.3) (kWh)', 'Production-based IEC B.2.3 (Users View)']

    important_cols = ["Date and time", "Wind speed (m/s)", "Power (kW)", 'Blade angle (pitch position) A (°)', "Rotor speed (RPM)"]
    #important columns must be:
    #   date and time
    #   wind speed
    #   power output
    #   pitch angle
    #   rotor speed


    process_data(n, dataset, model, important_cols, remove_cols=nan_cols, force_remake_files=False)



def care():

    n = 3 #turbine number
    dataset = "care" #kelmarsh, care
    model = "SVMKNN" #KNN, SVMKNN

    important_cols = ["time_stamp", "wind_speed_3_avg", "sensor_50", 'sensor_5_avg', "sensor_52_avg"]
    #important columns must be:
    #   date and time
    #   wind speed
    #   power output
    #   pitch angle
    #   rotor speed

    #title = f"{model} outlier detection"
    title = f"{model} outlier detection, only bad operation"
    

    process_data(n, dataset, model, important_cols, title, force_remake_files=True)
    

care()