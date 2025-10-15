import pandas as pd
import os
from tools.preprocessing import remove_extreme_outliers
from tools.outlier_removal import do_KNN_OD, do_SVMKNN_OD
from tools.graphing import Three_Curves
from tools.kelmarsh_stopped_removal import remove_stopped_data


n = 3 #turbine number
dataset = "care" #kelmarsh, care
model = "KNN" #KNN, SVMKNN
force_remake_files = True

graph_title = f"Turbine {n}, {model} outlier detection"
filename = f"graphs/{dataset}/t{n}_{model}_cutlowrpm"


#### Run a model on raw data to get inliers and outliers ####
if os.path.exists(f"data/{dataset}/{n}_{model}_outliers.csv") and not force_remake_files:
    inliers = pd.read_csv(f"data/{dataset}/{n}_{model}_inliers.csv")
    outliers = pd.read_csv(f"data/{dataset}/{n}_{model}_outliers.csv")
else:

    data = pd.read_csv(f"data/{dataset}/{n}.csv")
    data = remove_extreme_outliers(data)

    pd.DataFrame.to_csv(data, f"data/{dataset}/{n}_cutlowrpm.csv", index=False)

    if model == "KNN":
        inliers, outliers = do_KNN_OD(data)
    elif model == "SVMKNN":
        inliers, outliers = do_SVMKNN_OD(data)

    pd.DataFrame.to_csv(inliers, f"data/{dataset}/{n}_{model}_inliers_cutlowrpm.csv", index=False)
    pd.DataFrame.to_csv(outliers, f"data/{dataset}/{n}_{model}_outliers_cutlowrpm.csv", index=False)


    ##### testing removing stop status data ####
    #data, removed_data = remove_stopped_data(data)    
    #Three_Curves("removed stopped data in blue", red_data=removed_data, blue_data=data, filename="stopped codes plot, less")
    #print("stop here")
        


Three_Curves(graph_title, inliers, outliers, filename=filename)




