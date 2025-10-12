from pyod.models import knn
import pandas as pd
from tools.SVMKNN import SVMKNNDetector

#Wind speed (m/s),Power (kW),Blade angle (pitch position) A (°),Rotor speed (RPM)

def remove_outliers(data : pd.DataFrame, model):
    if 'Date and time' in data.columns:
        data = data.drop('Date and time', axis='columns')
    model.fit(data)

    y_train_pred = model.labels_  # binary labels (0: inliers, 1: outliers)
    y_train_scores = model.decision_scores_  # raw outlier scores

    #data['outlier'] = y_train_pred
    #data['outlier score'] = y_train_scores

    data_outliers = data[y_train_pred == 1].reset_index(drop=True)
    data_inliers = data[y_train_pred == 0].reset_index(drop=True)
    return data_inliers, data_outliers

def do_KNN_OD(data : pd.DataFrame):
    clf = knn.KNN(n_neighbors=30, method='median')
    return remove_outliers(data, clf)

def do_SVMKNN_OD(data : pd.DataFrame):
    clf = SVMKNNDetector(contamination=0.10, svm_kernel='rbf', svm_nu=0.1, svm_gamma='scale', 
        knn_n_neighbors=30, knn_method='median', gate_percentile=80)
    return remove_outliers(data, clf)


if __name__ == "__main__":
    data = pd.read_csv('data/RECOV_kelmarsh_preprocessed.csv')

    inliers, outliers = do_KNN_OD(data)

    pd.DataFrame.to_csv(outliers, 'data/RECOV_kelmarsh_outliers.csv')
    pd.DataFrame.to_csv(inliers, 'data/RECOV_kelmarsh_inliers.csv')

    #Cant do testing without ground truth. The paper gets ground truth by doing uisng many models and averaging/maxing the results
    #y_test_pred, y_test_pred_confidence = clf.predict(X_test, return_confidence=True)  # outlier labels (0 or 1) and confidence in the range of [0,1]

    # do data cleaning 
    # do KNN, SVM, SVM-KNN to see if I get similar results with ROC-AUC and mAP tests

    # create a NBM. with MLP or autoencoder/DBN? I thought KNN
    # test the NBM with RMSE, R^2, MAE
    # run models. hyperparameters?