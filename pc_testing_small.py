from sklearn.neighbors import KNeighborsRegressor as KNNR
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, root_mean_squared_error, mean_absolute_error
import pandas as pd
from tools.graphing import Three_Curves
import matplotlib.pyplot as plt



output_cols = ["Power (kW)", 'Pitch angle (°)', "Rotor speed (RPM)"]


filename = "3_KNN_inliers"
data = pd.read_csv(f"pc_test_data/{filename}.csv")


X = data[["Wind speed (m/s)"]]
y = data[["Power (kW)"]]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

reg = KNNR()
reg = reg.fit(X_train, y_train)

y_pred = reg.predict(X_test)

# R2 = r2_score(y_test, y_pred) # closer to 1.0 is better
# RMSE = root_mean_squared_error(y_test, y_pred)#lower is better
# MAE = mean_absolute_error(y_test, y_pred)#lower is better

# R2 = float('%.4f'%(R2))
# RMSE = float('%.4f'%(RMSE))
# MAE = float('%.4f'%(MAE))



fig, axes = plt.subplots(1, 3, figsize=(15, 5)) 

y_labels = ['Power (kW)']
x_label = 'Wind speed (m/s)'

blue_data = y_pred #numpy array
red_data = y_test #dataframe

print(X_test)
print(type(X_test))


for ax, y_label in zip(axes, y_labels):
    if red_data is not None:
        ax.scatter(X_test[x_label], red_data[y_label],color='red', marker='o', s=5)
    ax.scatter(X_test[x_label], blue_data,color='blue', marker='o', s=5)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    #ax.set_xlim(left=0)
    #ax.set_ylim(bottom=0)

graphfilename = None
plt.suptitle("predicted power from wind speed")
if graphfilename is not None:
    plt.savefig(f"{graphfilename}.png")
plt.show()