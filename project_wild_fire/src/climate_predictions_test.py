import common_paths  # Assuming this is a custom module with common paths defined
import geopandas as gpd
import matplotlib.pyplot as plt
import xarray as xr


class GeoDataFrameVisualizer:
    def __init__(self, shapefile_path):
        self.shapefile_path = shapefile_path
        self.df_ger = None

    def read_shapefile(self):
        """Reads the GeoDataFrame from the shapefile."""
        self.df_ger = gpd.read_file(self.shapefile_path)

    def assign_colors(self, colors):
        """Assigns colors to the GeoDataFrame."""
        if self.df_ger is None:
            raise ValueError(
                "GeoDataFrame not initialized. Call read_shapefile() first."
            )

        if len(colors) < len(self.df_ger):
            raise ValueError("Not enough colors provided for all geometries.")

        self.df_ger["color"] = colors[: len(self.df_ger)]

    def plot_geodataframe(
        self, figsize=(10, 10), cmap="tab20", title="GeoDataFrame Plot"
    ):
        """Plots the GeoDataFrame with color coding."""
        if self.df_ger is None:
            raise ValueError(
                "GeoDataFrame not initialized. Call read_shapefile() first."
            )

        fig, ax = plt.subplots(figsize=figsize)
        self.df_ger.plot(ax=ax, column="color", legend=True, cmap=cmap)
        plt.title(title)
        plt.show()

    def plot_heatmap(self, nc_file_path, variable_name, time_index=0, cmap="coolwarm"):
        """Plots a heatmap from a NetCDF file."""
        # Open the xarray dataset
        dataset = xr.open_dataset(nc_file_path, decode_times=True, use_cftime=True)

        try:
            # Extract necessary data variables
            data_array = dataset[variable_name].isel(time=time_index)
            data_array = (
                data_array.where(-10 <= data_array.rlon, drop=True)
                .where(data_array.rlon <= 0, drop=True)
                .where(-6 <= data_array.rlat, drop=True)
                .where(data_array.rlat <= 8, drop=True)
                .squeeze()
            )
            values = data_array.values

            plt.figure(figsize=(10, 8))
            plt.imshow(
                values,
                cmap=cmap,
                origin="lower",
            )
            plt.colorbar(label=f"{variable_name} ({data_array.units})")
            plt.xlabel("Longitude")
            plt.ylabel("Latitude")
            plt.title(f"Heatmap of {variable_name}")
            plt.show()

        finally:
            # Ensure the dataset is closed after plotting
            dataset.close()


if __name__ == "__main__":
    shapefile_path = common_paths.CMIP6.joinpath("vg2500_geo84/vg2500_bld.shp")
    nc_file_path = common_paths.CMIP6.joinpath(
        "tasmax_EUR-11_MPI-M-MPI-ESM-LR_historical_r2i1p1_DWD-EPISODES2018_v1-r1_mon_195101-200512.nc"
    )
    pr_file_path = common_paths.CLIMA_MODEL.joinpath("PR_data_climatemodel.nc")
    colors = [
        "blue",
        "orange",
        "yellow",
        "red",
        "purple",
        "green",
        "pink",
        "black",
        "white",
        "grey",
        "violet",
        "maroon",
        "olive",
        "cyan",
        "magenta",
        "teal",
    ]
    visualizer = GeoDataFrameVisualizer(shapefile_path)
    visualizer.read_shapefile()
    visualizer.assign_colors(colors)
    # visualizer.plot_geodataframe(title="Germany Map with Color Coding")
    visualizer.plot_heatmap(
        pr_file_path, variable_name="pr", time_index=0, cmap="coolwarm"
    )
