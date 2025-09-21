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

#Questions 1, 2 et 3

#Kuala Lumpur
plt.figure()
precip_sel = precipitation.sel(lat=3.1, lon=101.6, method='nearest')
precip_sel.plot()
plt.title("Précipitations à Kuala Lumpur")
plt.ylabel("Précipitation")
plt.xlabel("Temps")
plt.grid(True)
#plt.show()
somme_precip = precip_sel.sum(dim='time')
print("Somme précipitations Kuala Lumpur:" , somme_precip.values)

precip_selSansValeursNulles = precip_sel.where(precip_sel != 0, drop=True)

print("Nombre mesures non nulles Kuala Lumpur : ", precip_selSansValeursNulles.size)

frequence_precip = precip_selSansValeursNulles.size / precip_sel.size

print("Fréquence précipitation Kuala Lumpur : " , frequence_precip)

precip_moyenne = somme_precip.values / precip_sel.size
intensite_precip = somme_precip.values / precip_selSansValeursNulles.size

print("Précipitation moyenne Kuala Lumpur : " , precip_moyenne , "Intensité de précicipitation moyenne : " , intensite_precip)

compte = 0
nbr_consec = 0
max_nbr_consec = 0
for x in precip_sel.values :
    if x != 0:
        compte +=1
    if x == 0:
        nbr_consec = compte
        compte = 0
    if max_nbr_consec < nbr_consec:
        max_nbr_consec = nbr_consec

print("Durée maximale des événements de précipitations Kuala Lumpur (h) : " , max_nbr_consec*3)

#Quibdo
plt.figure()
precip_sel=precipitation.sel(lat=5.7, lon=76.6, method='nearest')
precip_sel.plot()
plt.title("Précipitations à Quibdo")
plt.ylabel("Précipitation")
plt.xlabel("Temps")
plt.grid(True)
#plt.show()

somme_precip=precip_sel.sum(dim='time')
print("Somme précipitations Quibdo:" , somme_precip.values)

precip_selSansValeursNulles = precip_sel.where(precip_sel != 0, drop=True)

print("Nombre mesures non nulles Quibdo : ", precip_selSansValeursNulles.size)

frequence_precip = precip_selSansValeursNulles.size / precip_sel.size

print("Fréquence précipitation Quibdo : " , frequence_precip)

precip_moyenne = somme_precip.values / precip_sel.size
intensite_precip = somme_precip.values / precip_selSansValeursNulles.size

print("Précipitation moyenne Quibdo : " , precip_moyenne , "Intensité de précicipitation moyenne : " , intensite_precip)

compte = 0
nbr_consec = 0
max_nbr_consec = 0
for x in precip_sel.values :
    if x != 0:
        compte +=1
    if x == 0:
        nbr_consec = compte
        compte = 0
    if max_nbr_consec < nbr_consec:
        max_nbr_consec = nbr_consec

print("Durée maximale des événements de précipitations Quibdo (h) : " , max_nbr_consec*3)

#Montréal
plt.figure()
precip_sel=precipitation.sel(lat=45.5, lon=73.5, method='nearest')
precip_sel.plot()
plt.title("Précipitations à Montréal")
plt.ylabel("Précipitation")
plt.xlabel("Temps")
plt.grid(True)
#plt.show()

somme_precip=precip_sel.sum(dim='time')
print("Somme précipitations Montréal:" , somme_precip.values)

precip_selSansValeursNulles = precip_sel.where(precip_sel != 0, drop=True)

print("Nombre mesures non nulles Montréal : ", precip_selSansValeursNulles.size)

frequence_precip = precip_selSansValeursNulles.size / precip_sel.size

print("Fréquence précipitation Montréal : " , frequence_precip)

precip_moyenne = somme_precip.values / precip_sel.size
intensite_precip = somme_precip.values / precip_selSansValeursNulles.size

print("Précipitation moyenne Montréal : " , precip_moyenne , "Intensité de précicipitation moyenne : " , intensite_precip)

compte = 0
nbr_consec = 0
max_nbr_consec = 0
for x in precip_sel.values :
    if x != 0:
        compte +=1
    if x == 0:
        nbr_consec = compte
        compte = 0
    if max_nbr_consec < nbr_consec:
        max_nbr_consec = nbr_consec

print("Durée maximale des événements de précipitations Montréal (h): " , max_nbr_consec*3)
#Océan
plt.figure()
precip_sel=precipitation.sel(lat=5.0, lon=106.0, method='nearest')
precip_sel.plot()
plt.title("Précipitations océan")
plt.ylabel("Précipitation")
plt.xlabel("Temps")
plt.grid(True)


somme_precip=precip_sel.sum(dim='time')
print("Somme précipitations Océan:" , somme_precip.values)

precip_selSansValeursNulles = precip_sel.where(precip_sel != 0, drop=True)

print("Nombre mesures non nulles Océan : ", precip_selSansValeursNulles.size)

frequence_precip = precip_selSansValeursNulles.size / precip_sel.size

print("Fréquence précipitation Océan : " , frequence_precip)

precip_moyenne = somme_precip.values / precip_sel.size
intensite_precip = somme_precip.values / precip_selSansValeursNulles.size

print("Précipitation moyenne Océan : " , precip_moyenne , "Intensité de précicipitation moyenne : " , intensite_precip)

compte = 0
nbr_consec = 0
max_nbr_consec = 0
for x in precip_sel.values :
    if x != 0:
        compte +=1
    if x == 0:
        nbr_consec = compte
        compte = 0
    if max_nbr_consec < nbr_consec:
        max_nbr_consec = nbr_consec

print("Durée maximale des événements de précipitations Océan (h): " , max_nbr_consec*3)


plt.show() #Montre tous les graphiques
#mimitoo tamo
