import pandas as pd
import os
from tools.preprocessing import isolate_columns, rename_columns, remove_extreme_outliers
from tools.outlier_removal import do_KNN_OD, do_SVMKNN_OD
from tools.graphing import Three_Curves

n = 1 #turbine number
dataset = "kelmarsh" #kelmarsh, care
model = "KNN" #KNN, SVMKNN
force_remake_files = True

graph_title = f"Turbine {n}, {model}_rotor_under_11_removed"
filename = f"graphs/{dataset}/t{n}_{graph_title}"


#### Run a model on raw data to get inliers and outliers ####
if os.path.exists(f"data/{dataset}/{n}_{model}_outliers.csv") and not force_remake_files:
    inliers = pd.read_csv(f"data/{dataset}/{n}_{model}_inliers.csv")
    outliers = pd.read_csv(f"data/{dataset}/{n}_{model}_outliers.csv")
else:

    data = pd.read_csv(f"data/{dataset}/{n}.csv")
    data = remove_extreme_outliers(data)

    if model == "KNN":
        inliers, outliers = do_KNN_OD(data)
    elif model == "SVMKNN":
        inliers, outliers = do_SVMKNN_OD(data)

    pd.DataFrame.to_csv(inliers, f"data/{dataset}/{n}_{model}_inliers.csv")
    pd.DataFrame.to_csv(outliers, f"data/{dataset}/{n}_{model}_outliers.csv")


Three_Curves(graph_title, inliers, outliers, filename)




