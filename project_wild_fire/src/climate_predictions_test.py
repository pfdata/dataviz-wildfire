#!/usr/bin/env python
# coding: utf-8

# In[1]:


import xarray as xr
import os
import netCDF4
import geopandas as gpd
import matplotlib.pyplot as plt
plt.style.use('seaborn-v0_8')
import plotly.express as pl
import cftime
import cartopy.crs as ccrs
import matplotlib.pyplot as pltimport 
import numpy as np


# In[2]:


path ='../data/cmip6/'
test_df=xr.open_dataset(path + 'tx90pETCCDI_mon_MPI-ESM1-2-LR_ssp585_r10i1p1f1_b1981-2010_v20190710_201501-210012_v2-0.nc')
test_xr=xr.open_dataset('../data/cmip6/tasmax_EUR-11_MPI-M-MPI-ESM-LR_historical_r2i1p1_DWD-EPISODES2018_v1-r1_mon_195101-200512.nc', decode_times=True, use_cftime=True)
test_xr


# In[3]:


df_ger = gpd.read_file(path + 'vg2500_geo84/vg2500_bld.shp')
df_ger.head


# In[4]:


fig, ax = plt.subplots()

ger_plot = df_ger.plot(ax=ax, color='darkblue', alpha=0.8)


# In[5]:


print(df_ger.iloc[:,3])
print(df_ger[['GEN','geometry']])


# In[6]:


df_ger['color'] = ['blue', 'orange', 'yellow', 'red', 'purple', 'green', 'pink', 'black', 'white', 'grey', 'violet', 'maroon', 'olive', 'cyan', 'magenta', 'teal']
df_ger.plot(color=df_ger['color'])


# In[7]:


df_ger.geometry.where(df_ger.GEN == 'Bremen').geometry.values


# In[ ]:





# In[8]:


test_xr.info


# In[11]:


test_xr['tasmax'].sel(time=cftime.DatetimeProlepticGregorian(1995, 4, 16, 0, 0, 0, 0, has_year_zero=True), )


# #### print(test_xr['tasmax'])
# print(test_xr['rlat'])

# In[12]:


test_xr.time.values


# In[13]:


test_xr['tasmax'].sel(time=cftime.DatetimeProlepticGregorian(2005, 3, 16, 12, 0, 0, 0, has_year_zero=True)).plot(cmap = 'coolwarm', size=20)


# In[29]:


a=test_xr.where(-10<=test_xr.rlon, drop =True).where(test_xr.rlon<=0, drop =True).where(-6<=test_xr.rlat, drop =True).where(test_xr.rlat<=8, drop =True).squeeze()


# In[36]:


a['tasmax'].sel(time=cftime.DatetimeProlepticGregorian(2005, 3, 16, 12, 0, 0, 0, has_year_zero=True)).plot(cmap = 'coolwarm', size=6)


# In[31]:


test_xr['tasmax'].sel(time=cftime.DatetimeProlepticGregorian(2005, 3, 16), method='nearest').plot(cmap = 'coolwarm', size=20)


# In[ ]:





# In[16]:


fig = plt.figure(1, figsize=[20,10])

# Fix extent
minval = 240
maxval = 300

# Plot 1 for Northern Hemisphere subplot argument (nrows, ncols, nplot)
# here 1 row, 2 columns and 1st plot
ax1 = plt.subplot(1, 2, 1, projection=ccrs.Orthographic(0, 90))

# Plot 2 for Southern Hemisphere
# 2nd plot 
ax2 = plt.subplot(1, 2, 2, projection=ccrs.Orthographic(180, -90))

tsel = 0
for ax,t in zip([ax1, ax2], ["Northern", "Southern"]):
    map = test_xr['tasmax'].isel(time=tsel).plot(ax=ax, vmin=minval, vmax=maxval, 
                                           transform=ccrs.PlateCarree(), 
                                           cmap='coolwarm', 
                                           add_colorbar=False)
    ax.set_title(t + " Hemisphere \n" , fontsize=15)
    ax.coastlines()
    ax.gridlines()

# Title for both plots
fig.suptitle('Near Surface Temperature\n' + test_xr.time.values[tsel].strftime("%B %Y"), fontsize=20)


cb_ax = fig.add_axes([0.325, 0.05, 0.4, 0.04])

cbar = plt.colorbar(map, cax=cb_ax, extend='both', orientation='horizontal', fraction=0.046, pad=0.04)
cbar.ax.tick_params(labelsize=25)
cbar.ax.set_ylabel('K', fontsize=25)


# In[17]:


print(test_xr.lat.sel())


# In[18]:


a = test_xr['tasmax'].sel(time=cftime.DatetimeProlepticGregorian(2000, 7, 1), method='nearest').values
a = a[~np.isnan(a)]
print(a)


# In[63]:


#Longitudes an denen der Wert der Termperatur ungleich 0 ist.
lons = test_xr.where(test_xr['tasmax']!=np.nan, drop =True).squeeze()


# In[67]:


np.max(lons)


# In[ ]:




