#!/usr/bin/env python
# coding: utf-8

# In[34]:


import xarray as xr

# import os
# import netCDF4
import geopandas as gpd
import matplotlib.pyplot as plt
import common_paths as cp

plt.style.use("seaborn-v0_8")

# from rasterio import features
# from affine import Affine


# In[33]:
# path = "../data/cmip6/"
cp.CMIP6
test_df = xr.open_dataset(
    cp.CMIP6.joinpath(
        "tx90pETCCDI_mon_MPI-ESM1-2-LR_ssp585_r10i1p1f1_b1981-2010_v20190710_201501-210012_v2-0.nc"
    )
)  # , engine="netcdf4")
test_df_2 = xr.open_dataset(
    cp.CMIP6.joinpath(
        "tasmax_EUR-11_MPI-M-MPI-ESM-LR_historical_r2i1p1_DWD-EPISODES2018_v1-r1_mon_195101-200512.nc"
    )
)
test_df_2


# In[15]:


df_ger = gpd.read_file(cp.CMIP6.joinpath("vg2500_geo84/vg2500_bld.shp"))
df_ger.head


# In[87]:


fig, ax = plt.subplots()

ger_plot = df_ger.plot(ax=ax, color="darkblue", alpha=0.8)


# In[82]:


print(df_ger.iloc[:, 3])
print(df_ger[["GEN", "geometry"]])


# In[91]:


df_ger["color"] = [
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


# In[92]:


df_ger.plot(color=df_ger["color"])


# In[ ]:
