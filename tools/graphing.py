import matplotlib.pyplot as plt
import pandas as pd

#it appears the pitch angkle is often high at low wind speeds...
#see if I can get any info on how this specific wind turbine handles its pitch angle

#Wind speed (m/s),Power (kW),Blade angle (pitch position) A (°),Rotor speed (RPM)


def Three_Curves( blue_data, red_data = None, green_data = None, title = None, filename = None):


    fig, axes = plt.subplots(1, 3, figsize=(15, 5)) 

    y_labels = ['Power (kW)', 'Pitch angle (°)', 'Rotor speed (RPM)']
    x_label = 'Wind speed (m/s)'

    for ax, y_label in zip(axes, y_labels):
        if red_data is not None:
            ax.scatter(red_data[x_label], red_data[y_label],color='red', marker='o', s=5)
        ax.scatter(blue_data[x_label], blue_data[y_label],color='blue', marker='o', s=5)
        if green_data is not None:
            ax.scatter(green_data[x_label], green_data[y_label],color='red', marker='o', s=5)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        #ax.set_xlim(left=0)
        #ax.set_ylim(bottom=0)

    if filename is not None:
        plt.savefig(f"{filename}.png")
    if title is not None:
        plt.suptitle(title)
        plt.show()

def Four_By_Four():
    pass

if __name__ == "__main__":
    #blue_data = pd.read_csv('data/RECOV_kelmarsh_inliers.csv')
    #red_data = pd.read_csv('data/RECOV_kelmarsh_outliers.csv')

    #Three_Curves(1, blue_data,red_data)

    data = pd.read_csv('data/care/3.csv')
    #Three_Curves("t3 care rpm on bottom", data, filename="rpm on bottom")

    print(data.columns)
    fig, axes = plt.subplots(1, 1, figsize=(1, 5)) 

    y_labels = ['Power (kW)']
    x_label = 'power_30_avg'

    for ax, y_label in zip([axes], y_labels):
        ax.scatter(data[x_label], data[y_label],color='blue', marker='o', s=5)
    
    plt.suptitle("active power vs grid power")
    plt.show()