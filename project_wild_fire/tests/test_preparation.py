import pandas as pd
import pytest

from wildfire_analysis.data.preparation import aggregate_historical_state_month


def test_station_rows_are_aggregated_before_modeling() -> None:
    frame = pd.DataFrame(
        {
            "Year": [2000, 2000],
            "Month": [1, 1],
            "station_id": ["a", "b"],
            "pr": [10.0, 20.0],
            "sfcWind": [2.0, 4.0],
            "tasmax": [280.0, 282.0],
            "nFires": [5.0, 5.0],
            "area": [3.0, 3.0],
        }
    )

    result = aggregate_historical_state_month(frame)

    assert result.to_dict("records") == [
        {
            "Year": 2000,
            "Month": 1,
            "pr": 15.0,
            "sfcWind": 3.0,
            "tasmax": 281.0,
            "nFires": 5.0,
            "area": 3.0,
        }
    ]


def test_inconsistent_monthly_targets_are_rejected() -> None:
    frame = pd.DataFrame(
        {
            "Year": [2000, 2000],
            "Month": [1, 1],
            "pr": [10.0, 20.0],
            "sfcWind": [2.0, 4.0],
            "tasmax": [280.0, 282.0],
            "nFires": [5.0, 6.0],
            "area": [3.0, 3.0],
        }
    )

    with pytest.raises(ValueError, match="targets differ"):
        aggregate_historical_state_month(frame)
