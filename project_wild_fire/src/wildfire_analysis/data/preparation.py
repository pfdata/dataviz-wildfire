from collections.abc import Mapping
from pathlib import Path

import pandas as pd

from wildfire_analysis.data.bmel import load_monthly_wildfires
from wildfire_analysis.paths import DWD_DIR


WEATHER_FEATURES = ("pr", "sfcWind", "tasmax")


def beaufort_to_metres_per_second(values: pd.Series) -> pd.Series:
    return 0.836 * values.astype(float).pow(1.5)


def aggregate_historical_state_month(frame: pd.DataFrame) -> pd.DataFrame:
    required = {"Year", "Month", "nFires", "area", *WEATHER_FEATURES}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Historical data are missing columns: {sorted(missing)}")

    target_variation = frame.groupby(["Year", "Month"])[["nFires", "area"]].nunique()
    if (target_variation > 1).any().any():
        raise ValueError("Wildfire targets differ between stations for the same month")

    aggregations = {feature: "mean" for feature in WEATHER_FEATURES}
    aggregations.update({"nFires": "first", "area": "first"})
    return (
        frame.groupby(["Year", "Month"], as_index=False).agg(aggregations)
        .dropna()
        .sort_values(["Year", "Month"])
        .reset_index(drop=True)
    )


def load_historical_state_month(
    path: Path = DWD_DIR / "data_Brandenburg.csv",
) -> pd.DataFrame:
    return aggregate_historical_state_month(pd.read_csv(path, index_col=0))


def build_historical_state_month(
    parameters: Mapping[str, object], state: str
) -> pd.DataFrame:
    from wildfire_analysis.data.dwd import (
        combine_parameters,
        fetch_monthly_observations,
        normalize_observations,
    )

    observations = [
        normalize_observations(fetch_monthly_observations(parameter, state), name)
        for name, parameter in parameters.items()
    ]
    weather = combine_parameters(observations)
    if "sfcWind" in weather:
        weather["sfcWind"] = beaufort_to_metres_per_second(weather["sfcWind"])
    weather_monthly = weather.groupby(["Year", "Month"], as_index=False)[
        list(parameters)
    ].mean()

    wildfires = load_monthly_wildfires()
    wildfires = wildfires.loc[wildfires["Land"] == state].drop(columns="Land")
    merged = weather_monthly.merge(
        wildfires,
        on=["Year", "Month"],
        how="inner",
        validate="one_to_one",
    )
    return merged.dropna().sort_values(["Year", "Month"]).reset_index(drop=True)
