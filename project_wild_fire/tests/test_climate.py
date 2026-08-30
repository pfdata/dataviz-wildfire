import pandas as pd

from wildfire_analysis.data.climate import (
    aggregate_future_state_month,
    precipitation_flux_to_monthly_total,
)


def test_precipitation_uses_calendar_month_length() -> None:
    result = precipitation_flux_to_monthly_total(
        pd.Series([1.0, 1.0]),
        pd.Series([2024, 2024]),
        pd.Series([2, 3]),
    )

    assert result.tolist() == [29 * 86_400, 31 * 86_400]


def test_future_grid_is_aggregated_to_one_month() -> None:
    frame = pd.DataFrame(
        {
            "Year": [2024, 2024],
            "Month": [1, 1],
            "pr": [10.0, 20.0],
            "sfcWind": [2.0, 4.0],
            "tasmax": [280.0, 282.0],
        }
    )

    result = aggregate_future_state_month(frame)

    assert result.to_dict("records") == [
        {"Year": 2024, "Month": 1, "pr": 15.0, "sfcWind": 3.0, "tasmax": 281.0}
    ]
