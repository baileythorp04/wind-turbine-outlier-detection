import pandas as pd
import os
from preprocessing import isolate_columns, remove_extreme_outliers
from outlier_removal import do_KNN_OD, do_SVMKNN_OD
from graphing import Three_Curves

#For new data, remember to remove top 9 empty rows, replace comma with semicolon, and remove Â
#Then replace all � back to °

n = 1 #turbine number
model = "SVMKNN"
force_remake_files = True

if os.path.exists(f"data/kelmarsh_{n}_{model}_outliers.csv") and not force_remake_files:
    inliers = pd.read_csv(f"data/kelmarsh_{n}_{model}_inliers.csv")
    outliers = pd.read_csv(f"data/kelmarsh_{n}_{model}_outliers.csv")
else:
    data = pd.read_csv(f"data/kelmarsh_{n}.csv")
    data = isolate_columns(data, remove=["Date and time"])
    data = remove_extreme_outliers(data)

    #for some reason writing then reading from csv gets better results. try using dropduplicates to see the differences before and after
    data.to_csv("mid.csv") 
    data = pd.read_csv("mid.csv")

    if model == "KNN":
        inliers, outliers = do_KNN_OD(data)
    elif model == "SVMKNN":
        inliers, outliers = do_SVMKNN_OD(data)

    pd.DataFrame.to_csv(inliers, f"data/kelmarsh_{n}_{model}_inliers.csv")
    pd.DataFrame.to_csv(outliers, f"data/kelmarsh_{n}_{model}_outliers.csv")

modifier = f"{model} outlier detection"
filename = f"t{n}_{model}"
#filename = f"t{n}_{modifier}"

Three_Curves(f"Turbine {n}, {modifier}", inliers, outliers, filename)