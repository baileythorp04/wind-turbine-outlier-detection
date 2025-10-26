from sklearn.neighbors import KNeighborsRegressor as KNNR
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, root_mean_squared_error, mean_absolute_error
import pandas as pd
import numpy as np
from tools.graphing import Three_Curves
import matplotlib.pyplot as plt

#data_file_names = ["3_original_renamed", "3_extreme_outliers_removed", "3_KNN_inliers", "3_SVMKNN_inliers", "3_cutlowrpm", "3_KNN_inliers_cutlowrpm", "3_SVMKNN_inliers_cutlowrpm",]
data_file_names = ["3_KNN_inliers", "3_SVMKNN_inliers", "3_KNN_inliers_cutlowrpm", "3_SVMKNN_inliers_cutlowrpm",]
output_cols = ["Power (kW)", 'Pitch angle (°)', "Rotor speed (RPM)"]


###### try simple with just one regression test and one graph ######



i = 0
df = pd.DataFrame(columns=['R2', 'RMSE', 'MAE'])


for filename in data_file_names:
    ### graph setup ###
    fig, axes = plt.subplots(1, 3, figsize=(15, 5)) 
    train = pd.read_csv(f"data/care/tt/{filename}_train.csv")
    test = pd.read_csv(f"data/care/tt/{filename}_test.csv")

    for ax, output_col in zip(axes, output_cols):

        print(f"testing {filename} with {output_col}.", end=" ")

        ### testing model setup ###

        #X is input data      
        #Y is output data
        X_train = train[["Wind speed (m/s)"]] 
        y_train = train[[output_col]]

        X_test = test[["Wind speed (m/s)"]] 
        y_test = test[[output_col]]

        reg = KNNR()
        reg = reg.fit(X_train, y_train)



        #### testing ####
        y_pred = reg.predict(X_test)

        R2 = r2_score(y_test, y_pred) # closer to 1.0 is better
        RMSE = root_mean_squared_error(y_test, y_pred)#lower is better
        MAE = mean_absolute_error(y_test, y_pred)#lower is better

        R2 = float('%.4f'%(R2))
        RMSE = float('%.4f'%(RMSE))
        MAE = float('%.4f'%(MAE))

        print(f"R2 = {R2}, RMSE = {RMSE}, MAE = {MAE}")

        df.loc[len(df)] = [R2, RMSE, MAE]
        
        a = pd.DataFrame()
        a.columns

        #### graphing ####
        mn = min(X_test[X_test.columns[0]]) #convert dataframe of one column into array
        mx = max(X_test[X_test.columns[0]])
        values = np.linspace(mn, mx, num=1000)

        y_label = output_col
        x_label = 'Wind speed (m/s)'

        X_curve = pd.DataFrame(values, columns=[x_label])
        y_curve = reg.predict(X_curve)


        ax.scatter(X_test[x_label], y_test[y_label], color='red', marker='o', s=5)
        ax.scatter(X_curve[x_label], y_curve,color='blue', marker='o', s=5)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        #ax.set_xlim(left=0)
        #ax.set_ylim(bottom=0)
        i += 1

    #### graphing ####
    plt.suptitle(f"predicted power from wind speed - {filename}")
    if filename is not None:
        plt.savefig(f"tt_{filename}.png")
    #plt.show()







output_df = df.T

output_df.to_csv("raw_results_tt.csv")




#get a knn PC model
#for every dataset:
#split it to test-train
#get the RMSE and R2 from testing