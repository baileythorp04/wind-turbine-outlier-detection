import pandas as pd
import os
from sklearn.model_selection import train_test_split
from tools.preprocessing import remove_extreme_outliers
from tools.outlier_removal import do_KNN_OD, do_SVMKNN_OD
from tools.graphing import Three_Curves
from tools.kelmarsh_stopped_removal import remove_stopped_data

n = 3 #turbine number
dataset = "care" #kelmarsh, care
#model = "KNN" #KNN, SVMKNN
cutlowrpm = True

force_remake_files = True

#graph_title = f"Turbine {n}, {model} outlier detection"
#filename = f"graphs/{dataset}/t{n}_{model}_onlylowrpm"

datafile_mods = ["", "cutlowrpm", "extreme_outliers_removed" ]
models = ["KNN", "SVMKNN"]


#### Run a model on raw data to get inliers and outliers ####
def run_model(data, n, dataset, model, cutlowrpm, graph_title, filename, t, datafile_modifier="",):

    
    data = remove_extreme_outliers(data, cutlowrpm)

    pd.DataFrame.to_csv(data, f"data/{dataset}/{n}_cutlowrpm.csv", index=False)

    if model == "KNN":
        inliers, outliers = do_KNN_OD(data)
    elif model == "SVMKNN":
        inliers, outliers = do_SVMKNN_OD(data)

    pd.DataFrame.to_csv(inliers, f"data/{dataset}/tt/{n}_{model}_inliers_{datafile_modifier}_{t}.csv", index=False)
    #pd.DataFrame.to_csv(outliers, f"data/{dataset}/tt/{n}_{model}_outliers_{datafile_modifier}_{t}.csv", index=False)

    


    #Three_Curves(graph_title, inliers, outliers, filename=filename)

#for cutrpm in [True, False]:
for model in models:
    data = pd.read_csv(f"data/{dataset}/{n}.csv")
    train, test = train_test_split(data, test_size=0.3)

    run_model(train, n, dataset, model, False, None, None, "train", "" )
    run_model(test, n, dataset, model, False, None, None, "test", "" )



