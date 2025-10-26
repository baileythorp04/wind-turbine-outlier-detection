according to https://wes.copernicus.org/articles/8/893/2023/, do preprocessing (knn or svmknn) on training and testing separately when splitting t/t for making an NBM

you DESPERATELY need to redo all the test data csv's now that youre using power_30_avg instead of sensor_50.
Redo the R2 RMSE and MAE results but with real power production to see if its better.

Remake the PC graph but have the blue line be made with evenly spaces wind speeds (not test data) so it looks better



try bootstrapping

make a 4x4 graph if you want