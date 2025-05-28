# netcdf4
# Cartopy
# matplotlib
# numpy


import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt

fn = 'MERRA2_400.tavg1_2d_rad_Nx.20250501.nc4'
f = nc.Dataset(fn,'r')
lat = f.variables['lat'][:]
lon = f.variables['lon'][:]
data = f.variables['LWGEM'][:]

# Create plot
fig, ax = plt.subplots()  #Create a single subplot
contour = ax.contourf(lon, lat, data[0,:,:], cmap='viridis') #Assuming data is 3D (time, lat, lon)

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

