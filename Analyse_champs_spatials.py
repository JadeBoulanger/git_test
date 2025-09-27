# Packages a importer
import os
import cartopy.crs as ccrs
import sys
import glob
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import xarray as xr

# Repertoire ou le fichier se trouve
path_file = 'imerg_pr_201911_3h.nc4'

# Nom de la variable
var_name = 'precipitationCal'

# Pour lire le fichier
print('Reading file: ', path_file)
ds_i = xr.open_dataset(path_file)
ds_i.close()
print('Reading file: DONE')
precipitation = ds_i[var_name]
lons = ds_i['lon']
lats = ds_i['lat']

precip_sel = precipitation.sel(time="2019-11-01T12:00:00.000000000", method='nearest')
precip_selValeurSous20mm = precip_sel.where((precip_sel <= 20) & (precip_sel > 0))

#1
plt.figure()
ax = plt.axes(projection=ccrs.LambertCylindrical())
ax.coastlines()
plt.pcolormesh(lons, lats, precip_selValeurSous20mm)
plt.title("Distribution spatiale du taux de précipitation")
ax.set_xticks(range(-180, 180, 60), crs=ccrs.LambertCylindrical())
ax.set_yticks(range(-90, 90, 30), crs=ccrs.LambertCylindrical())
ax.set_ylabel("Latitude")
ax.set_xlabel("Longitude")
plt.colorbar(ax=ax, orientation="horizontal", label="Taux de précipitation (mm/3h)")

#2
plt.figure()
precip = precip_sel.values[~np.isnan(precip_sel.values)].flatten()
plt.hist(precip, bins=20)
plt.yscale('log')
plt.title("Histograme pour différentes intensités de précipitation")
plt.xlabel("Intensité de précipitation (mm/3h)")
plt.ylabel("Nombre de mesures")

#3
precip_moyenne = precipitation.mean(dim="time")
precip_selValeurSous5mm = precip_moyenne.where((precip_moyenne <= 5) & (precip_sel > 0))

plt.figure()
ax = plt.axes(projection=ccrs.LambertCylindrical())
ax.coastlines()
plt.pcolormesh(lons, lats, precip_selValeurSous5mm)
plt.title("Distribution spatiale du taux de précipitation moyen")
ax.set_xticks(range(-180, 180, 60), crs=ccrs.LambertCylindrical())
ax.set_yticks(range(-90, 90, 30), crs=ccrs.LambertCylindrical())
ax.set_ylabel("Latitude")
ax.set_xlabel("Longitude")
plt.colorbar(ax=ax, orientation="horizontal", label="Taux de précipitation (mm/3h)")


#4
plt.figure()
precip = precip_moyenne.values[~np.isnan(precip_sel.values)].flatten()
plt.hist(precip, bins=20)
plt.yscale('log')
plt.title("Histograme du taux de précipitation moyen")
plt.xlabel("Taux de précipitation moyen (mm/3h)")
plt.ylabel("Nombre de mesures")

#5
precip_sel = precipitation.sel(lat=slice(44.5, 46.5), lon=slice(-74.5, -72.5))
precip_moyenne = precip_sel.mean(dim="time")

plt.figure()
ax = plt.axes(projection=ccrs.Mercator())
plt.pcolormesh(precip_moyenne.lon, precip_moyenne.lat, precip_moyenne)
plt.title("Distribution spatiale du taux de précipitation moyen autour de Montréal")
ax.set_xticks(np.arange(-74.5, -72.5), crs=ccrs.Mercator())
ax.set_yticks(np.arange(44.5, 46.5), crs=ccrs.Mercator())
ax.set_ylabel("Latitude")
ax.set_xlabel("Longitude")
plt.colorbar(ax=ax, orientation="horizontal", label="Taux de précipitation (mm/3h)")

#6
precip_sel = precipitation.sel(lat=slice(44.5, 46.5), lon=slice(-74.5, -72.5))
precip_moyenne = precip_sel.mean(dim="time")

plt.figure()
ax = plt.axes(projection=ccrs.Mercator())
plt.contourf(precip_moyenne.lon, precip_moyenne.lat, precip_moyenne.values)
plt.title("Distribution spatiale du taux de précipitation moyen autour de Montréal")
ax.set_xticks(np.arange(-74.5, -72.5,), crs=ccrs.Mercator())
ax.set_yticks(np.arange(44.5, 46.5, 0.5), crs=ccrs.Mercator())
ax.set_ylabel("Latitude")
ax.set_xlabel("Longitude")
plt.colorbar(ax=ax, orientation="horizontal", label="Taux de précipitation (mm/3h)")

#Bonus
#precip_somme = precipitation.sum(dim="time")

#plt.figure()
#ax = plt.axes(projection=ccrs.LambertCylindrical())
#ax.coastlines()
#plt.pcolormesh(lons, lats, precip_somme)
#plt.title("Distribution spatiale de la somme des précipitations pour le mois")
#ax.set_xticks(range(-180, 180, 60), crs=ccrs.LambertCylindrical())
#ax.set_yticks(range(-90, 90, 30), crs=ccrs.LambertCylindrical())
#ax.set_ylabel("Latitude")
#ax.set_xlabel("Longitude")
#plt.colorbar(ax=ax, orientation="horizontal", label="Somme des précipitations (mm)")

precip_intensitemax = precipitation.max(dim="time")
#precip_max = precip_intensitemax.where(precip_intensitemax > 50)


plt.figure()
ax = plt.axes(projection=ccrs.LambertCylindrical())
ax.coastlines()
plt.pcolormesh(lons, lats, precip_intensitemax)
plt.title("Distribution spatiale de l'intensité maximale des précipitations")
ax.set_xticks(range(-180, 180), crs=ccrs.LambertCylindrical())
ax.set_yticks(range(-90, 90), crs=ccrs.LambertCylindrical())
ax.set_ylabel("Latitude")
ax.set_xlabel("Longitude")
plt.colorbar(ax=ax, orientation="horizontal", label="Intensité des précipitations (mm/3h)")
plt.show()