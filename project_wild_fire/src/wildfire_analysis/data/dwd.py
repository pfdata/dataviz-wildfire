from collections.abc import Iterable

import pandas as pd
from wetterdienst import Period, Resolution
from wetterdienst.provider.dwd.observation import (
    DwdObservationParameter,
    DwdObservationRequest,
)


def fetch_monthly_observations(parameter: object, state: str) -> pd.DataFrame:
    request = DwdObservationRequest(
        parameter=parameter,
        resolution=Resolution.MONTHLY,
        period=Period.HISTORICAL,
    )
    stations = request.all().df
    if hasattr(stations, "to_pandas"):
        stations = stations.to_pandas()
    stations = pd.DataFrame(stations)
    station_ids = stations.loc[stations["state"] == state, "station_id"].tolist()
    if not station_ids:
        raise ValueError(f"DWD returned no monthly stations for state {state!r}")

    values = request.filter_by_station_id(station_ids).values.all().df
    if hasattr(values, "to_pandas"):
        values = values.to_pandas()
    observations = pd.DataFrame(values)
    if observations.empty:
        raise ValueError(f"DWD returned no observations for state {state!r}")
    return observations


def normalize_observations(observations: pd.DataFrame, feature_name: str) -> pd.DataFrame:
    required = {"date", "station_id", "value"}
    missing = required.difference(observations.columns)
    if missing:
        raise ValueError(f"DWD observations are missing columns: {sorted(missing)}")
    normalized = observations.loc[:, ["date", "station_id", "value"]].copy()
    normalized["date"] = pd.to_datetime(normalized["date"])
    normalized["Year"] = normalized["date"].dt.year
    normalized["Month"] = normalized["date"].dt.month
    return normalized.rename(columns={"value": feature_name}).drop(columns="date")


def combine_parameters(frames: Iterable[pd.DataFrame]) -> pd.DataFrame:
    frames = list(frames)
    if not frames:
        raise ValueError("At least one weather parameter is required")
    combined = frames[0].copy()
    for frame in frames[1:]:
        combined = combined.merge(
            frame,
            on=["Year", "Month", "station_id"],
            how="outer",
            validate="one_to_one",
        )
    return combined


__all__ = ["DwdObservationParameter", "combine_parameters", "fetch_monthly_observations", "normalize_observations"]
