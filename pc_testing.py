from sklearn.neighbors import KNeighborsRegressor as KNNR
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, root_mean_squared_error, mean_absolute_error
import pandas as pd
from tools.graphing import Three_Curves

data_file_names = ["3_original_renamed", "3", "3_KNN_inliers", "3_SVMKNN_inliers", "3_cutlowrpm", "3_KNN_inliers_cutlowrpm", "3_SVMKNN_inliers_cutlowrpm",]
output_cols = ["Power (kW)", 'Pitch angle (°)', "Rotor speed (RPM)"]


i = 0
df = pd.DataFrame(columns=['R2', 'RMSE', 'MAE'])


for filename in data_file_names:
    data = pd.read_csv(f"pc_test_data/{filename}.csv")

    pred_graph_df = pd.DataFrame()
    real_graph_df = pd.DataFrame()

    for output_col in output_cols:
        print(f"testing {filename} with {output_col}.", end=" ")

        #X is input data      
        #Y is output data
        X = data[["Wind speed (m/s)"]] 
        y = data[[output_col]]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        reg = KNNR()
        reg = reg.fit(X_train, y_train)

        y_pred = reg.predict(X_test)

        R2 = r2_score(y_test, y_pred) # closer to 1.0 is better
        RMSE = root_mean_squared_error(y_test, y_pred)#lower is better
        MAE = mean_absolute_error(y_test, y_pred)#lower is better

        R2 = float('%.4f'%(R2))
        RMSE = float('%.4f'%(RMSE))
        MAE = float('%.4f'%(MAE))

        print(f"R2 = {R2}, RMSE = {RMSE}, MAE = {MAE}")

        df.loc[len(df)] = [R2, RMSE, MAE]
        
        pred_graph_df[output_col] = y_pred[:, 0]
        real_graph_df[output_col] = y_test[y_test.columns[0]]


        pred_graph_df["Wind speed (m/s)"] = X_test[X_test.columns[0]]
        real_graph_df["Wind speed (m/s)"] = X_test[X_test.columns[0]]
        i += 1

    Three_Curves(f"testing of {filename}", blue_data=pred_graph_df, red_data=real_graph_df, filename=f"testing_{filename}")








output_df = df.T

output_df.to_csv("raw_results.csv")




#get a knn PC model
#for every dataset:
#split it to test-train
#get the RMSE and R2 from testing