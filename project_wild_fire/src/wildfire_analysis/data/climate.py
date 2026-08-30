from pathlib import Path

import pandas as pd

from wildfire_analysis.paths import DWD_DIR


WEATHER_FEATURES = ("pr", "sfcWind", "tasmax")


def precipitation_flux_to_monthly_total(
    flux: pd.Series, year: pd.Series, month: pd.Series
) -> pd.Series:
    dates = pd.to_datetime(
        {"year": year.astype(int), "month": month.astype(int), "day": 1}
    )
    return flux.astype(float) * dates.dt.days_in_month * 24 * 60 * 60


def load_future_climate(
    path: Path = DWD_DIR / "future_Brandenburg.csv",
) -> pd.DataFrame:
    frame = pd.read_csv(path, index_col=0)
    required = {"Year", "Month", *WEATHER_FEATURES}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Future climate data are missing columns: {sorted(missing)}")
    frame = frame.copy()
    frame["pr"] = precipitation_flux_to_monthly_total(
        frame["pr"], frame["Year"], frame["Month"]
    )
    return frame


def aggregate_future_state_month(frame: pd.DataFrame) -> pd.DataFrame:
    return (
        frame.groupby(["Year", "Month"], as_index=False)[list(WEATHER_FEATURES)]
        .mean()
        .sort_values(["Year", "Month"])
        .reset_index(drop=True)
    )
