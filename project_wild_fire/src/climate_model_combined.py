import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import common_paths


data_pr = xr.open_dataset(common_paths.CLIMA_MODEL.joinpath("PR_data_climatemodel.nc"))
data_pr_array = data_pr["pr"]  # dataarray
# print(data_pr)

# variables in dataset
# data_pr.data_vars
# data_pr.info()
# data_pr.pr[0]


# Wertebereich herausfinden

# rlon = data_pr["rlon"]
# rlat = data_pr["rlat"]
# # Drucke die minimalen und maximalen Werte der rlon&rlat-Koordinate aus
# print(f"Min rlon: {rlon.min().item()}")
# print(f"Max rlon: {rlon.max().item()}")
# print(f"Min rlat: {rlat.min().item()}")
# print(f"Max rlat: {rlat.max().item()}")

# andere Möglichkeit für Wertebereich
# data_pr.pr.coords


# sel select values by label
# Slice Right Time
data_pr_2030 = data_pr.sel(time=slice("2024-01-16", "2054-01-16"))
# Slice degrees beiing out of germany
data_pr_2030_zoom = data_pr_2030.sel(rlon=slice(-9, -1), rlat=slice(-5, 6))
# data_pr_2030_zoom.pr.coords
# data_pr_2030_zoom.pr[60].plot
# # data_pr_2030_zoom.pr[5].plot()
# # data_pr_2030_zoom.pr[200].plot()
# data_pr_2030_zoom.pr


# In[ ]:


# Not working just for Test

# Lon & Lat for Berlin 52.520008, 13.404954.
rlat_val = 300
rlon_val = 300

# Neues Datenset für bestimmten Ort extrahieren
pr_data = data_pr["pr"].sel(rlat=rlat_val, rlon=rlon_val, method="nearest")

# Diagramm das läuft noch nicht vor allem x-achse falscher input
plt.figure()
plt.plot(data_pr["time"], pr_data, label="Precipitation")
plt.xlabel("Time")
plt.ylabel("Precipitation (mm)")
plt.title("Precipitation over Time at rlat={}, rlon{}".format(rlat_val, rlon_val))
plt.grid()
plt.show()

# print(data_pr)
# time_data = data_pr["time"].to_dataframe()
# # von 2006 bis 2100
# print(time_data)
