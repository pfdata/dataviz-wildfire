from collections.abc import Iterable

import pandas as pd
from sklearn.base import clone

from wildfire_analysis.modeling.registry import build_regressors


DEFAULT_FEATURES = ("pr", "sfcWind", "tasmax")
DEFAULT_TARGETS = ("nFires", "area")


def fit_target_models(
    frame: pd.DataFrame,
    features: Iterable[str] = DEFAULT_FEATURES,
    targets: Iterable[str] = DEFAULT_TARGETS,
    model_name: str = "Gradient boosting",
) -> dict[str, object]:
    features = list(features)
    required = {*features, *targets}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Training data are missing columns: {sorted(missing)}")
    regressors = build_regressors()
    if model_name not in regressors:
        raise ValueError(f"Unknown model {model_name!r}; expected one of {sorted(regressors)}")

    models = {}
    for target in targets:
        model = clone(regressors[model_name])
        model.fit(frame[features], frame[target])
        models[target] = model
    return models
