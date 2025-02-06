import xarray as xr
import glob
import os
import numpy as np
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature


cities = {}
cities['Denver'] = [39.739,-104.985]
cities['Colorado Springs'] = [38.834,-104.821]
# cities['Aurora'] = [39.729,-104.832]
cities['Fort Collins'] = [40.585,-105.084]
# cities['Lakewood'] = [39.705,-105.081]
# cities['Thornton'] = [39.868,-104.972]
# cities['Westminster'] = [39.837,-105.037]
# cities['Arvada'] = [39.803,-105.087]
cities['Centennial'] = [39.579,-104.877]
cities['Boulder'] = [40.015,-105.271]
cities['Greeley'] = [40.423,-104.709]


def plot_var(var_to_plot, cmap='viridis', contour=True):
    
    # proj = ccrs.LambertConformal(central_longitude=(xmin+xmax)/2, central_latitude=(ymin+ymax)/2)
    proj = ccrs.PlateCarree()

    fig = plt.figure()    
    ax = fig.add_subplot(111, facecolor='None', projection=proj)

    ax.coastlines()
    ax.add_feature(cfeature.STATES, ls=':')
    ax.add_feature(cfeature.RIVERS)
    ax.set_title(var_to_plot.description, fontsize=10)
    plt.suptitle(var_to_plot.name, fontsize=16)
    
    if contour:
        im = ax.contourf(var_to_plot.lon, var_to_plot.lat, var_to_plot.data[0,:,:], transform=ccrs.PlateCarree(), cmap=cmap)
    else:
        im = ax.pcolormesh(var_to_plot.lon, var_to_plot.lat, var_to_plot.data[0,:,:], transform=ccrs.PlateCarree(), cmap=cmap)
    for city in cities.keys():
        ax.scatter(cities[city][1], cities[city][0], transform=ccrs.PlateCarree(), s=30, c='k', marker='*')
        ax.text(cities[city][1]+0.03, cities[city][0]+0.04, city, fontsize=8)
    ax.set_extent([np.min(var_to_plot.lon)-0.5, np.max(var_to_plot.lon)+0.5,
                   np.min(var_to_plot.lat)-0.5, np.max(var_to_plot.lat)+0.5], crs=ccrs.PlateCarree())
    cax = fig.add_axes([ax.get_position().x1+0.01, ax.get_position().y0, 0.05, ax.get_position().height])
    cbar = plt.colorbar(im, cax=cax)
    cbar.set_label(var_to_plot.units, rotation=90, fontsize=14)

def plot_var_numpy(var_to_plot, ds, cmap='viridis', contour=True):
    
    # proj = ccrs.LambertConformal(central_longitude=(xmin+xmax)/2, central_latitude=(ymin+ymax)/2)
    proj = ccrs.PlateCarree()

    fig = plt.figure()    
    ax = fig.add_subplot(111, facecolor='None', projection=proj)

    ax.coastlines()
    ax.add_feature(cfeature.STATES, ls=':')
    ax.add_feature(cfeature.RIVERS)
    
    if contour:
        im = ax.contourf(ds.lon, ds.lat, var_to_plot, transform=ccrs.PlateCarree(), cmap=cmap)
    else:
        im = ax.pcolormesh(ds.lon, ds.lat, var_to_plot, transform=ccrs.PlateCarree(), cmap=cmap)
    for city in cities.keys():
        ax.scatter(cities[city][1], cities[city][0], transform=ccrs.PlateCarree(), s=30, c='k', marker='*')
        ax.text(cities[city][1]+0.03, cities[city][0]+0.04, city, fontsize=8)
    ax.set_extent([np.min(ds.lon)-0.5, np.max(ds.lon)+0.5,
                   np.min(ds.lat)-0.5, np.max(ds.lat)+0.5], crs=ccrs.PlateCarree())
    cax = fig.add_axes([ax.get_position().x1+0.01, ax.get_position().y0, 0.05, ax.get_position().height])
    cbar = plt.colorbar(im, cax=cax)