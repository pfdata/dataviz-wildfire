#!/usr/bin/env python
# coding: utf-8

# In[2]:


import xarray as xr
import os
import netCDF4
import matplotlib.pyplot as pltimport 
import numpy as np
import cftime


# In[3]:


path ='../data/episodes/'
xr_humidity=xr.open_dataset(path + 'hurs_EUR-11_MPI-M-MPI-ESM-LR_historical_r1i1p1_DWD-EPISODES2018_v1-r1_mon_195101-200512.nc', decode_times=True, use_cftime=True)
xr_precipitation=xr.open_dataset(path + 'pr_EUR-11_MPI-M-MPI-ESM-LR_historical_r1i1p1_DWD-EPISODES2018_v1-r1_mon_195101-200512.nc', decode_times=True, use_cftime=True)
xr_wind=xr.open_dataset(path + 'sfcWind_EUR-11_MPI-M-MPI-ESM-LR_historical_r1i1p1_DWD-EPISODES2018_v1-r1_mon_195101-200512.nc', decode_times=True, use_cftime=True)
xr_mean_temp=xr.open_dataset(path + 'tas_EUR-11_MPI-M-MPI-ESM-LR_historical_r1i1p1_DWD-EPISODES2018_v1-r1_mon_195101-200512.nc', decode_times=True, use_cftime=True)
xr_max_temp=xr.open_dataset(path + 'tasmax_EUR-11_MPI-M-MPI-ESM-LR_historical_r1i1p1_DWD-EPISODES2018_v1-r1_mon_195101-200512.nc', decode_times=True, use_cftime=True)
xr_min_temp=xr.open_dataset(path + 'tasmin_EUR-11_MPI-M-MPI-ESM-LR_historical_r1i1p1_DWD-EPISODES2018_v1-r1_mon_195101-200512.nc', decode_times=True, use_cftime=True)


# In[4]:


xr_humidity


# In[5]:


xr_precipitation


# In[6]:


xr_wind


# In[7]:


xr_mean_temp


# In[8]:


xr_max_temp


# In[9]:


xr_min_temp


# In[ ]:




