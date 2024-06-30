from wetterdienst.provider.dwd.observation import (
    DwdObservationRequest,
    DwdObservationParameter,
)
from wetterdienst import Period, Resolution
import polars as pl
import datetime as dt


def fetch_observation_data(parameter, state):
    # Define the parameters for the request
    observations_meta = DwdObservationRequest(
        parameter=parameter,
        resolution=Resolution.MONTHLY,
        period=Period.HISTORICAL,
    )

    # Fetch the metadata and convert to a Polars DataFrame
    stations_df = pl.DataFrame(observations_meta.all().df)

    # Filter by state
    filtered_df = stations_df.filter(pl.col("state") == state)

    # Extract station IDs from the filtered DataFrame
    station_ids = filtered_df["station_id"].to_list()

    # Define the request to fetch observation data
    observations_data_request = DwdObservationRequest(
        parameter=parameter,
        resolution=Resolution.MONTHLY,
        period=Period.HISTORICAL,
    ).filter_by_station_id(station_ids)

    # Fetch the observation data and convert to a Polars DataFrame
    observations_data_df = pl.DataFrame(observations_data_request.values.all().df)

    return observations_data_df.to_pandas()
