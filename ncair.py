#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs 
import cartopy.feature as cfeat
# from cartopy.mpl.ticker import LONGITUDE_FORMATTER,LATITUDE_FORMATTER
from cartopy.mpl.gridliner  import LONGITUDE_FORMATTER,LATITUDE_FORMATTER
#读nc数据
import xarray as xr

#读nc数据
ds = xr.open_dataset('D:\\syt\\air.2m.mon.mean.nc')

lon_name = 'lon'  # whatever name is in the data
#从0至360转换为-180-180，方便画图
# Adjust lon values to make sure they are within (-180, 180)
ds['_longitude_adjusted'] = xr.where(
    ds[lon_name] > 180,
    ds[lon_name] - 360,
    ds[lon_name])

# reassign the new coords to as the main lon coords
# and sort DataArray using new coordinate values
ds = (
    ds
    .swap_dims({lon_name: '_longitude_adjusted'})
    .sel(**{'_longitude_adjusted': sorted(ds._longitude_adjusted)})
    .drop(lon_name))

ds = ds.rename({'_longitude_adjusted': lon_name})

temp = (ds['air'] - 273.15).mean(dim='time')
temp.attrs['units'] = 'deg C'
temp=temp[0,0:25,0:25]




# In[10]:


# 创建画图空间
proj = ccrs.PlateCarree() #创建投影
fig = plt.figure(figsize=(16,9)) #创建页面
ax = fig.subplots(1, 1, subplot_kw={'projection': proj}) #子图
# 设置地图属性:加载国界、海岸线、河流、湖泊
ax.add_feature(cfeat.BORDERS.with_scale('50m'), linewidth=0.8, zorder=1)
ax.add_feature(cfeat.COASTLINE.with_scale('50m'), linewidth=0.6, zorder=1)
ax.add_feature(cfeat.RIVERS.with_scale('50m'), zorder=1)
ax.add_feature(cfeat.LAKES.with_scale('50m'), zorder=1)

gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
linewidth=1.2, color='k', alpha=0.5, linestyle='--')
gl.xlabels_top = False #关闭顶端标签
gl.ylabels_right = False #关闭右侧标签
gl.xformatter = LONGITUDE_FORMATTER #x轴设为经度格式
gl.yformatter = LATITUDE_FORMATTER #y轴设为纬度格式

# 设置colorbar
cbar_kwargs = {
'orientation': 'horizontal',
'label': '2m temperature (℃)',
'shrink': 0.8,
}
levels = np.arange(-30, 30, 1)

temp.plot.contourf(ax=ax, levels=levels, cmap='Spectral_r',
cbar_kwargs=cbar_kwargs, transform=ccrs.PlateCarree())
ax.set_title('2m Temperature',color='black',fontsize= 20)

plt.show()


# In[ ]:





# In[ ]:




