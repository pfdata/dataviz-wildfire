import pandas as pd

from wildfire_analysis.modeling.prediction import predict_future
from wildfire_analysis.modeling.training import fit_target_models


def test_models_produce_monthly_nonnegative_predictions() -> None:
    training = pd.DataFrame(
        {
            "Year": range(2000, 2012),
            "Month": [1] * 12,
            "pr": range(10, 22),
            "sfcWind": [3.0] * 12,
            "tasmax": range(280, 292),
            "nFires": range(1, 13),
            "area": range(2, 14),
        }
    )
    future = training.loc[[0], ["Year", "Month", "pr", "sfcWind", "tasmax"]]
    models = fit_target_models(training, model_name="Linear regression")

    result = predict_future(models, future)

    assert {"nr_predictions", "area_predictions"}.issubset(result.columns)
    assert (result[["nr_predictions", "area_predictions"]] >= 0).all().all()
