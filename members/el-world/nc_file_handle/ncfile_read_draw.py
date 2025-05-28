# netcdf4
# Cartopy
# matplotlib
# numpy


import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt

fn = 'MERRA2_400.tavg1_2d_rad_Nx.20250501.nc4'
fn_land = 'lsmask.oisst.nc'

f = nc.Dataset(fn, 'r')
land_data = nc.Dataset(fn_land, 'r')

lon = land_data.variables['lon'][:]
lat = land_data.variables['lat'][:]
land = land_data.variables['lsmask'][:]
fig=plt.figure(figsize=(16,9))
ax = fig.add_subplot(111)

cont=ax.contourf(lon-180,lat,land[0,:,:],colors='#F8ECD2')
conline=ax.contour(lon-180, lat, land[0,:,:], colors='k',linewidths=0.2,alpha=0.8)


lat_2 = f.variables['lat'][:]
lon_2 = f.variables['lon'][:]
data_2 = f.variables['LWGEM'][:]


# Create plot
# fig, ax = plt.subplots(111)  #Create a single subplot
contour = ax.contourf(lon_2, lat_2, data_2[0,:,:], cmap='viridis') #Assuming data is 3D (time, lat, lon)

# Add labels and title
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
cbar = fig.colorbar(contour)
cbar.set_label('Temperature')
ax.set_title('Temperature Distribution')

# Show or save the plot
plt.show()
#plt.savefig('temperature_plot.png')

# Close the NetCDF file
f.close()

