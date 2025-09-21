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

x = precipitation.sel(lat=3.1, lon=101.6, method='nearest')
print(x.values)
print(x.size)
#xSansValeursNulles = x.where(x != 0, drop=True)

#nombreValeursNonNulles = xSansValeursNulles.size

#print("Nombre mesures non nulles Kuala Lumpur : ", nombreValeursNonNulles)

plt.figure()
x = precipitation.sel(lat=3.1, lon=101.6, method='nearest') #.sel est ok, nearest est ok, à vérifier pour pouvoir mettre la et lon en même temps et vérifier si ok de faire avec précipitation et non ds_i
x.plot() #à vérifier que tout soit ok et changer les titres par les miens
plt.title("Précipitations à Kuala Lumpur")
plt.ylabel("Précipitation")
plt.xlabel("Temps")
plt.grid(True)
plt.show()