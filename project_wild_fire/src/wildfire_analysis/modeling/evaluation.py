import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.model_selection import TimeSeriesSplit

from wildfire_analysis.modeling.registry import build_regressors


def regression_metrics(observed: pd.Series, predicted: np.ndarray) -> dict[str, float]:
    return {
        "MAE": mean_absolute_error(observed, predicted),
        "RMSE": root_mean_squared_error(observed, predicted),
        "R2": r2_score(observed, predicted),
    }


def evaluate_regressors(
    frame: pd.DataFrame,
    features: list[str],
    target: str,
    n_splits: int = 5,
) -> pd.DataFrame:
    ordered = frame.sort_values(["Year", "Month"]).reset_index(drop=True)
    if len(ordered) <= n_splits:
        raise ValueError("Not enough monthly observations for temporal cross-validation")
    splitter = TimeSeriesSplit(n_splits=n_splits)
    rows = []
    for model_name, estimator in build_regressors().items():
        fold_metrics = []
        for fold, (train_index, test_index) in enumerate(splitter.split(ordered), start=1):
            model = clone(estimator)
            model.fit(ordered.loc[train_index, features], ordered.loc[train_index, target])
            predictions = np.clip(model.predict(ordered.loc[test_index, features]), 0, None)
            fold_metrics.append(
                {
                    "Model": model_name,
                    "Fold": fold,
                    **regression_metrics(ordered.loc[test_index, target], predictions),
                }
            )
        rows.extend(fold_metrics)
    return pd.DataFrame(rows)


def summarize_evaluation(scores: pd.DataFrame) -> pd.DataFrame:
    return (
        scores.groupby("Model", as_index=False)[["MAE", "RMSE", "R2"]]
        .mean()
        .sort_values("MAE")
        .reset_index(drop=True)
    )
