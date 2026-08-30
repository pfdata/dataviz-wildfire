from pathlib import Path

import numpy as np
import pandas as pd

from wildfire_analysis.modeling.training import DEFAULT_FEATURES
from wildfire_analysis.paths import DWD_DIR


PREDICTION_COLUMNS = {"nFires": "nr_predictions", "area": "area_predictions"}


def predict_future(
    models: dict[str, object],
    future: pd.DataFrame,
    features: tuple[str, ...] = DEFAULT_FEATURES,
) -> pd.DataFrame:
    missing = set(features).difference(future.columns)
    if missing:
        raise ValueError(f"Future data are missing features: {sorted(missing)}")
    predictions = future.loc[:, ["Year", "Month", *features]].copy()
    for target, model in models.items():
        column = PREDICTION_COLUMNS.get(target, f"{target}_predictions")
        predictions[column] = np.clip(
            model.predict(future.loc[:, list(features)]), 0, None
        )
    return predictions


def write_predictions(
    predictions: pd.DataFrame,
    path: Path = DWD_DIR / "final_predictions.csv",
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    predictions.to_csv(path, index=False)
    return path
