from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import xarray as xr


def load_boundaries(path: Path) -> gpd.GeoDataFrame:
    return gpd.read_file(path)


def plot_boundaries(boundaries: gpd.GeoDataFrame, column: str | None = None):
    figure, axis = plt.subplots(figsize=(10, 10))
    boundaries.plot(ax=axis, column=column, legend=column is not None, cmap="viridis")
    axis.set_axis_off()
    return figure


def plot_climate_grid(path: Path, variable: str, time_index: int = 0):
    with xr.open_dataset(path, decode_times=True, use_cftime=True) as dataset:
        data = dataset[variable].isel(time=time_index).squeeze().load()
    figure, axis = plt.subplots(figsize=(10, 8))
    data.plot(ax=axis, cmap="coolwarm")
    axis.set_title(f"{variable} at time index {time_index}")
    return figure
