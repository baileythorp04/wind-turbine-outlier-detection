# knn_perf_curves.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from typing import Dict, Tuple
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def _knn_pipeline():
    return Pipeline([
        ("scaler", StandardScaler(with_mean=True, with_std=True)),
        ("knn", KNeighborsRegressor())
    ])


def _tune_and_fit_knn(X: np.ndarray, y: np.ndarray, random_state: int = 42):
    pipe = _knn_pipeline()
    # K grid: adjust to your sample size; denser data → larger k often okay
    param_grid = {
        "knn__n_neighbors": [10, 15, 20, 25, 30, 40],
        "knn__weights": ["distance", "uniform"]
    }
    gs = GridSearchCV(
        pipe,
        param_grid=param_grid,
        scoring="neg_mean_absolute_error",
        cv=5,
        n_jobs=-1,
        refit=True
    )
    gs.fit(X, y)
    return gs.best_estimator_, gs.best_params_


def _metrics(y_true, y_pred) -> Dict[str, float]:
    mae = mean_absolute_error(y_true, y_pred)
    rmse = mean_squared_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    return {"MAE": mae, "RMSE": rmse, "R2": r2}


def _bootstrap_pi(model, X: np.ndarray, y: np.ndarray, X_grid: np.ndarray,
                  n_boot: int = 1000, alpha: float = 0.05, rng: np.random.RandomState = None
                 ) -> Tuple[np.ndarray, np.ndarray]:
    """
    Residual bootstrap PI for pointwise uncertainty bands:
      - compute residuals on the *training* (or full) set
      - resample residuals with replacement
      - PI at grid x: yhat(x) ± z * std(residuals)
    Uses normal approx with z=1.96 for 95% by default.
    """
    if rng is None:
        rng = np.random.RandomState(42)

    # Fit preds and residuals on X,y (assumed model is already fitted)
    y_hat = model.predict(X)
    residuals = (y - y_hat).ravel()

    # Standard deviation of bootstrap residuals
    # (you can do full resample but a simple σ works well and is fast)
    sigma = residuals.std(ddof=1)
    z = 1.96 if np.isclose(alpha, 0.05) else abs(np.quantile(np.random.normal(size=200000), 1 - alpha/2))

    y_grid = model.predict(X_grid).ravel()
    lo = y_grid - z * sigma
    hi = y_grid + z * sigma
    return lo, hi


def fit_performance_curves_knn(
    df: pd.DataFrame,
    wind_col: str = "wind_speed",
    power_col: str = "power",
    pitch_col: str = "pitch_angle",
    rpm_col: str = "rotor_speed",
    test_size: float = 0.3,
    random_state: int = 42,
    compute_pi: bool = True,
):
    """
    Fit KNN regressors for three curves:
      - Power vs Wind
      - Pitch vs Wind
      - Rotor Speed vs Wind

    Assumes df already has outliers removed.

    Returns:
      models: dict of fitted models by target name
      metrics: dict of MAE/RMSE/R2 per target (evaluated on holdout)
      grid: dict with X_grid and y_hat(yhat_lo, yhat_hi) per target for plotting
    """
    # Keep just the columns we need & drop missing
    cols = [wind_col, power_col, pitch_col, rpm_col]
    data = df[cols].dropna().copy()

    # Basic dtype coercion (safety)
    for c in cols:
        if c != pitch_col:  # pitch might be small negatives; still numeric
            data[c] = pd.to_numeric(data[c], errors="coerce")
    data = data.dropna()

    # Train/test split on wind for all targets
    X = data[[wind_col]].values
    y_power = data[power_col].values
    y_pitch = data[pitch_col].values
    y_rpm = data[rpm_col].values

    X_tr, X_te, yP_tr, yP_te = train_test_split(X, y_power, test_size=test_size, random_state=random_state)
    _,    _,  yA_tr, yA_te = train_test_split(X, y_pitch, test_size=test_size, random_state=random_state)
    _,    _,  yR_tr, yR_te = train_test_split(X, y_rpm,   test_size=test_size, random_state=random_state)

    models, params, metrics = {}, {}, {}

    # ---- Power vs Wind ----
    mP, pP = _tune_and_fit_knn(X_tr, yP_tr, random_state)
    yP_hat = mP.predict(X_te)
    models["power"], params["power"], metrics["power"] = mP, pP, _metrics(yP_te, yP_hat)

    # ---- Pitch vs Wind ----
    mA, pA = _tune_and_fit_knn(X_tr, yA_tr, random_state)
    yA_hat = mA.predict(X_te)
    models["pitch"], params["pitch"], metrics["pitch"] = mA, pA, _metrics(yA_te, yA_hat)

    # ---- Rotor Speed vs Wind ----
    mR, pR = _tune_and_fit_knn(X_tr, yR_tr, random_state)
    yR_hat = mR.predict(X_te)
    models["rpm"], params["rpm"], metrics["rpm"] = mR, pR, _metrics(yR_te, yR_hat)

    # Smooth grid for plotting
    w_min, w_max = float(X.min()), float(X.max())
    w_grid = np.linspace(w_min, w_max, 400).reshape(-1, 1)

    grid = {
        "wind": w_grid.ravel(),
        "power": {"yhat": models["power"].predict(w_grid).ravel()},
        "pitch": {"yhat": models["pitch"].predict(w_grid).ravel()},
        "rpm":   {"yhat": models["rpm"].predict(w_grid).ravel()},
    }

    if compute_pi:
        lo, hi = _bootstrap_pi(models["power"], X_tr, yP_tr, w_grid)
        grid["power"]["lo"], grid["power"]["hi"] = lo, hi

        lo, hi = _bootstrap_pi(models["pitch"], X_tr, yA_tr, w_grid)
        grid["pitch"]["lo"], grid["pitch"]["hi"] = lo, hi

        lo, hi = _bootstrap_pi(models["rpm"], X_tr, yR_tr, w_grid)
        grid["rpm"]["lo"], grid["rpm"]["hi"] = lo, hi

    return models, params, metrics, grid


def plot_curves(df: pd.DataFrame, grid: Dict, wind_col="wind_speed",
                power_col="power", pitch_col="pitch_angle", rpm_col="rotor_speed",
                show_pi: bool = True):
    fig, axes = plt.subplots(1, 3, figsize=(16, 4), sharex=False)

    # Power vs Wind
    ax = axes[0]
    ax.scatter(df[wind_col], df[power_col], s=8, alpha=0.35)
    ax.plot(grid["wind"], grid["power"]["yhat"])
    if show_pi and "lo" in grid["power"]:
        ax.fill_between(grid["wind"], grid["power"]["lo"], grid["power"]["hi"], alpha=0.2)
    ax.set_xlabel("Wind speed")
    ax.set_ylabel("Power")

    # Pitch vs Wind
    ax = axes[1]
    ax.scatter(df[wind_col], df[pitch_col], s=8, alpha=0.35)
    ax.plot(grid["wind"], grid["pitch"]["yhat"])
    if show_pi and "lo" in grid["pitch"]:
        ax.fill_between(grid["wind"], grid["pitch"]["lo"], grid["pitch"]["hi"], alpha=0.2)
    ax.set_xlabel("Wind speed")
    ax.set_ylabel("Pitch angle")

    # Rotor Speed vs Wind
    ax = axes[2]
    ax.scatter(df[wind_col], df[rpm_col], s=8, alpha=0.35)
    ax.plot(grid["wind"], grid["rpm"]["yhat"])
    if show_pi and "lo" in grid["rpm"]:
        ax.fill_between(grid["wind"], grid["rpm"]["lo"], grid["rpm"]["hi"], alpha=0.2)
    ax.set_xlabel("Wind speed")
    ax.set_ylabel("Rotor speed (RPM)")

    fig.tight_layout()
    plt.show()

["Date and time", "Wind speed (m/s)", "Power (kW)", 'Blade angle (pitch position) A (°)', "Rotor speed (RPM)"]
# ---- Example usage ----
if __name__ == "__main__":
    df = pd.read_csv("data/kelmarsh_1_KNN_inliers.csv")
    # df should already be filtered (outliers removed)
    # Expected columns; rename here if yours differ
    # df = pd.read_csv("your_clean_scada.csv")
    df.rename(columns={"Wind speed (m/s)": "wind_speed", "Power (kW)" : "power", 'Blade angle (pitch position) A (°)' : "pitch_angle", "Rotor speed (RPM)" : "rotor_speed" }, inplace=True)

    # Dummy structure hint:
    # df = pd.DataFrame({
    #     "wind_speed": ...,
    #     "power": ...,
    #     "pitch_angle": ...,
    #     "rotor_speed": ...
    # })

    models, params, metrics, grid = fit_performance_curves_knn(df)
    print("Best params:", params)
    print("Metrics:", metrics)
    plot_curves(df, grid, show_pi=True)
    
