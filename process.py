import pandas as pd
import os
from tools.preprocessing import isolate_columns, rename_columns, remove_extreme_outliers
from tools.outlier_removal import do_KNN_OD, do_SVMKNN_OD
from tools.graphing import Three_Curves

def process_data(n, dataset, model, important_cols, title_modifier, remove_cols=[], force_remake_files=False):
        
    #### Run a model on raw data to get inliers and outliers ####
    if os.path.exists(f"data/{dataset}/{n}_{model}_outliers.csv") and not force_remake_files:
        inliers = pd.read_csv(f"data/{dataset}/{n}_{model}_inliers.csv")
        outliers = pd.read_csv(f"data/{dataset}/{n}_{model}_outliers.csv")
    else:
        data = pd.read_csv(f"data/{dataset}/{n}.csv")
        data = isolate_columns(data, remove=remove_cols)
        data = rename_columns(data, important_cols)
        data = remove_extreme_outliers(data)

        #for some reason writing then reading from csv gets better results. try using dropduplicates to see the differences before and after
        #data.to_csv("mid.csv") 
        #data = pd.read_csv("mid.csv")

        if model == "KNN":
            inliers, outliers = do_KNN_OD(data)
        elif model == "SVMKNN":
            inliers, outliers = do_SVMKNN_OD(data)

        pd.DataFrame.to_csv(inliers, f"data/{dataset}/{n}_{model}_inliers.csv")
        pd.DataFrame.to_csv(outliers, f"data/{dataset}/{n}_{model}_outliers.csv")

    filename = f"{dataset}/t{n}_{title_modifier}"

    Three_Curves(f"Turbine {n}, {title_modifier}", inliers, outliers, filename)




