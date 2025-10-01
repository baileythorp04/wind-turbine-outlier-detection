import matplotlib.pyplot as plt
import pandas as pd

#it appears the pitch angkle is often high at low wind speeds...

#Wind speed (m/s),Power (kW),Blade angle (pitch position) A (°),Rotor speed (RPM)

def Three_Curves():
    data = pd.read_csv('data/Turbine_Data.csv')

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5)) 
    ax1.scatter(data['Wind speed (m/s)'], data['Power (kW)'],color='blue', marker='o')
    ax1.set_xlabel('Wind speed (m/s)')
    ax1.set_ylabel('Power (Kw)')
    ax1.set_xlim(left=0)
    ax1.set_ylim(bottom=0)

    ax2.scatter(data['Wind speed (m/s)'], data['Blade angle (pitch position) A (°)'], color='blue', marker='o')
    ax2.set_xlabel('Wind speed (m/s)')
    ax2.set_ylabel('Blade angle (pitch position) (°)')
    ax2.set_xlim(left=0)
    ax2.set_ylim(bottom=0)

    ax3.scatter(data['Wind speed (m/s)'], data['Rotor speed (RPM)'], color='blue', marker='o')
    ax3.set_xlabel('Wind speed (m/s)')
    ax3.set_ylabel('Rotor speed (RPM)')
    ax3.set_xlim(left=0)
    ax3.set_ylim(bottom=0)

    plt.show()

def Four_By_Four():
    pass

Three_Curves()