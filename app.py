import pandas as pd
import os
from preprocessing import isolate_columns, remove_extreme_outliers
from outlier_removal import  remove_outliers_KNN
from graphing import Three_Curves

#For new data, remember to remove top 9 empty rows, replace comma with semicolon, and remove Â
#Then replace all � back to °

n = 2

if os.path.exists(f"data/kelmarsh_{n}_outliers.csv"):
    inliers = pd.read_csv(f"data/kelmarsh_{n}_inliers.csv")
    outliers = pd.read_csv(f"data/kelmarsh_{n}_outliers.csv")
else:
    data = pd.read_csv(f"data/kelmarsh_{n}.csv")
    data = isolate_columns(data, remove=["Date and time"])
    data = remove_extreme_outliers(data)

    #for some reason writing then reading from csv gets better results. try using dropduplicates to see the differences before and after
    data.to_csv("mid.csv") 
    data = pd.read_csv("mid.csv")

    inliers, outliers = remove_outliers_KNN(data)
    pd.DataFrame.to_csv(inliers, f"data/kelmarsh_{n}_inliers.csv")
    pd.DataFrame.to_csv(outliers, f"data/kelmarsh_{n}_outliers.csv")

Three_Curves({n}, inliers, outliers)