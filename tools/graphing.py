import matplotlib.pyplot as plt
import pandas as pd

#it appears the pitch angkle is often high at low wind speeds...
#see if I can get any info on how this specific wind turbine handles its pitch angle

#Wind speed (m/s),Power (kW),Blade angle (pitch position) A (°),Rotor speed (RPM)


def Three_Curves(title, inlier_data, outlier_data = None, filename = None):


    fig, axes = plt.subplots(1, 3, figsize=(15, 5)) 

    y_labels = ['Power (kW)', 'Pitch angle (°)', 'Rotor speed (RPM)']

    for ax, y_label in zip(axes, y_labels):
        if outlier_data is not None:
            ax.scatter(outlier_data['Wind speed (m/s)'], outlier_data[y_label],color='red', marker='o', s=5)
        ax.scatter(inlier_data['Wind speed (m/s)'], inlier_data[y_label],color='blue', marker='o', s=5)
        ax.set_xlabel('Wind speed (m/s)')
        ax.set_ylabel(y_label)
        #ax.set_xlim(left=0)
        #ax.set_ylim(bottom=0)

    plt.suptitle(title)
    if filename is not None:
        plt.savefig(f"graphs/{filename}.png")
    plt.show()

def Four_By_Four():
    pass

if __name__ == "__main__":
    #inlier_data = pd.read_csv('data/RECOV_kelmarsh_inliers.csv')
    #outlier_data = pd.read_csv('data/RECOV_kelmarsh_outliers.csv')

    #Three_Curves(1, inlier_data,outlier_data)

    og_data = pd.read_csv('data/kelmarsh_2.csv')
    Three_Curves("Turbine 2, unmodified", og_data)