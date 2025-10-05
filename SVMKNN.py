import numpy as np
from sklearn.preprocessing import StandardScaler
from pyod.models.ocsvm import OCSVM
from pyod.models.knn import KNN
from pyod.utils.data import get_outliers_inliers
from pyod.utils.utility import standardizer
from pyod.models.combination import aom, moa, average, maximization

# ChatGPT wrote this

class SVMKNNDetector:
    """
    Hybrid outlier detector:
    - Fit OCSVM and KNN on the same data.
    - Compute standardized scores for both.
    - If |SVM margin| is "large" (confident), use SVM score.
      Else (near hyperplane), use KNN distance-based score.
    - Also exposes A/M/AOM/MOA ensemble combinations of the two.
    """
    def __init__(self,
                 contamination=0.1,
                 svm_kernel='rbf',
                 svm_nu=0.5,
                 svm_gamma='scale',
                 knn_n_neighbors=15,
                 knn_method='largest',
                 gate_percentile=60):
        """
        gate_percentile: percentile on |svm_margin| to define 'near boundary'.
                         e.g., 60 => lower 60% of |margin| uses KNN.
        """
        self.contamination = contamination
        self.svm = OCSVM(kernel=svm_kernel, nu=svm_nu, gamma=svm_gamma,
                         contamination=contamination)
        self.knn = KNN(n_neighbors=knn_n_neighbors,
                       method=knn_method,  # 'largest' uses k-th NN distance
                       contamination=contamination)
        self.scaler_ = None
        self.gate_percentile = gate_percentile

        # learned at fit-time
        self.decision_scores_ = None           # hybrid scores (higher = more outlier)
        self.labels_ = None                    # 0=inlier, 1=outlier
        self.svm_scores_ = None
        self.knn_scores_ = None
        self.svm_margin_abs_ = None
        self.gate_threshold_ = None

        # ensembles for convenience
        self.score_avg_ = None
        self.score_max_ = None
        self.score_aom_ = None
        self.score_moa_ = None

    def fit(self, X):
        # Optional: standardize features (common for distance + kernel methods)
        self.scaler_ = StandardScaler().fit(X)
        Xs = self.scaler_.transform(X)

        # Fit base detectors
        self.svm.fit(Xs)
        self.knn.fit(Xs)

        # Raw decision scores (PyOD: higher = more abnormal)
        svm_scores = self.svm.decision_scores_.astype(float)
        knn_scores = self.knn.decision_scores_.astype(float)

        # Standardize model scores to comparable z-scales
        S = np.vstack([svm_scores, knn_scores]).T
        S_std = (S - S.mean(axis=0)) / (S.std(axis=0) + 1e-12)
        svm_z = S_std[:, 0]
        knn_z = S_std[:, 1]

        # Compute absolute SVM margins (distance from hyperplane).
        # PyOD's OCSVM stores raw decision_function on training as decision_scores_.
        # Higher positive => more outlier, but margin proxy is absolute raw f(x).
        # We use absolute *unstandardized* magnitude for gating.
        svm_margin_abs = np.abs(self.svm.decision_scores_)
        gate_thr = np.percentile(svm_margin_abs, self.gate_percentile)

        # Gate: if |margin| < gate_thr (near boundary) => use KNN; else => use SVM
        use_knn = svm_margin_abs < gate_thr
        hybrid = np.where(use_knn, knn_z, svm_z)

        # Save
        self.svm_scores_ = svm_z
        self.knn_scores_ = knn_z
        self.svm_margin_abs_ = svm_margin_abs
        self.gate_threshold_ = gate_thr
        self.decision_scores_ = hybrid

        # Threshold to labels by contamination (same policy as PyOD)
        thr = np.percentile(self.decision_scores_, 100 * (1 - self.contamination))
        self.labels_ = (self.decision_scores_ >= thr).astype(int)

        # Also compute ensemble combos (over the two base scores)
        self.score_avg_ = average(S_std)
        self.score_max_ = maximization(S_std)
        # For AOM/MOA, we need multiple "detectors"; we only have 2, so make 2 groups.
        self.score_aom_ = aom(S_std, n_buckets=2)
        self.score_moa_ = moa(S_std, n_buckets=2)
        return self

    def decision_function(self, X):
        """Get outlier scores for new data (higher = more abnormal)."""
        Xs = self.scaler_.transform(X)
        svm_scores = self.svm.decision_function(Xs).ravel()
        knn_scores = self.knn.decision_function(Xs).ravel()

        # standardize with train-time stats of base scores
        # to keep it simple, recompute z with current batch stats
        S = np.vstack([svm_scores, knn_scores]).T
        S_std = (S - S.mean(axis=0)) / (S.std(axis=0) + 1e-12)
        svm_z = S_std[:, 0]
        knn_z = S_std[:, 1]

        # margin proxy for gating at inference
        svm_margin_abs = np.abs(svm_scores)
        use_knn = svm_margin_abs < self.gate_threshold_
        hybrid = np.where(use_knn, knn_z, svm_z)
        return hybrid

    def predict(self, X):
        scores = self.decision_function(X)
        thr = np.percentile(self.decision_scores_, 100 * (1 - self.contamination))
        return (scores >= thr).astype(int)
