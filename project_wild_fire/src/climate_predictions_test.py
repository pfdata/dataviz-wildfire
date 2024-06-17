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
            # print(data_array)
            latitudes = data_array["lat"]
            longitudes = data_array["lon"]
            values = data_array.values

            plt.figure(figsize=(10, 8))
            plt.imshow(
                values,
                extent=(
                    longitudes.min(),
                    longitudes.max(),
                    latitudes.min(),
                    latitudes.max(),
                ),
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
