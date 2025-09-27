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
fig, Taux_Precip = plt.subplots(2,2)
precip_sel = precipitation.sel(lat=3.1, lon=101.6, method='nearest')
Taux_Precip[0,0].plot(precip_sel)
Taux_Precip[0,0].set_title("Précipitations à Kuala Lumpur")
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
taux_precip_max = 0
for x in precip_sel.values :
    if x != 0:
        compte +=1
    if x == 0:
        nbr_consec = compte
        compte = 0
    if max_nbr_consec < nbr_consec:
        max_nbr_consec = nbr_consec
    if x > taux_precip_max:
        taux_precip_max = x


print("Durée maximale des événements de précipitations Kuala Lumpur (h) : " , max_nbr_consec*3)
print("Taux maximal de précipitation Kuala Lumpur (mm/h) : " , taux_precip_max/3)

#111km = 1° de latitude et 111km * cos(lat) = 1° de longitude
#plus_50km_Nord = 50/111
#plus_50km_Sud = -(50/111)
#plus_50km_Est = 50/(111*cos(3.1))
#plus_50km_Ouest = - (50/(111*cos(3.1)))

precip_sel_nord = precipitation.sel(lat=3.6, lon=101.6, method='nearest')
precip_sel_sud = precipitation.sel(lat=2.6, lon=101.6, method='nearest')
precip_sel_est = precipitation.sel(lat=3.1, lon=102.1, method='nearest')
precip_sel_ouest = precipitation.sel(lat=3.1, lon=101.1, method='nearest')

arr = np.array([precip_sel.values, precip_sel_nord.values, precip_sel_sud.values, precip_sel_est.values, precip_sel_ouest.values])
coef = np.corrcoef(arr, rowvar=True)
print("Coefficient à Kuala Lumpur : " , coef)

#plt.figure()
fig, Variab_Points_Proches = plt.subplots(2,2)
ax = Variab_Points_Proches[0, 0]
ax.scatter(precip_sel_nord.values, precip_sel.values, color='blue', label='50km au Nord')
ax.scatter(precip_sel_sud.values, precip_sel.values, color='red', label='50km au Sud')
ax.scatter(precip_sel_est.values, precip_sel.values, color='green', label='50km Est')
ax.scatter(precip_sel_ouest.values, precip_sel.values, color='yellow', label='50km Ouest')
ax.set_title("Kuala Lumpur")
ax.set_ylabel("Kuala Lumpur (mm/3h)")
ax.legend()

groupes_jours = precip_sel.groupby('time.dayofyear')
for date, donnee in groupes_jours:
    total =+ donnee

precip_moyenne_journee = (total/30).values
heure_de_la_journee = ["8h", "11h", "14h", "17h", "20h", "23h", "2h", "5h"] #UTC+8 pour Kuala Lumpur

fig, Cycle_Precip = plt.subplots(2,2)
Cycle_Precip[0, 0].plot(heure_de_la_journee, precip_moyenne_journee)
Cycle_Precip[0, 0].set_title("Kuala Lumpur")
Cycle_Precip[0, 0].set_ylim(0, 0.03)
Cycle_Precip[0, 0].set_ylabel("Précip. moy. (mm)")
Cycle_Precip[0, 0].grid(True)

#Quibdo
precip_sel=precipitation.sel(lat=5.7, lon=-76.6, method='nearest')
Taux_Precip[0,1].plot(precip_sel,'tab:orange')
Taux_Precip[0,1].set_title("Précipitations à Quibdo")

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
taux_precip_max = 0
for x in precip_sel.values :
    if x != 0:
        compte +=1
    if x == 0:
        nbr_consec = compte
        compte = 0
    if max_nbr_consec < nbr_consec:
        max_nbr_consec = nbr_consec
    if x > taux_precip_max:
        taux_precip_max = x

print("Durée maximale des événements de précipitations Quibdo (h) : " , max_nbr_consec*3)
print("Taux maximal de précipitation Quibdo (mm/h) : " , taux_precip_max/3)

precip_sel_nord = precipitation.sel(lat=6.2, lon=-76.6, method='nearest')
precip_sel_sud = precipitation.sel(lat=5.2, lon=-76.6, method='nearest')
precip_sel_est = precipitation.sel(lat=5.7, lon=-76.2, method='nearest')
precip_sel_ouest = precipitation.sel(lat=5.7, lon=-77.1, method='nearest')

arr = np.array([precip_sel.values, precip_sel_nord.values, precip_sel_sud.values, precip_sel_est.values, precip_sel_ouest.values])
coef = np.corrcoef(arr, rowvar=True)
print("Coefficient à Quibdo : " , coef)

ax = Variab_Points_Proches[0, 1]
ax.scatter(precip_sel_nord.values, precip_sel.values, color='blue', label='50km au Nord')
ax.scatter(precip_sel_sud.values, precip_sel.values, color='red', label='50km au Sud')
ax.scatter(precip_sel_est.values, precip_sel.values, color='green', label='50km Est')
ax.scatter(precip_sel_ouest.values, precip_sel.values, color='yellow', label='50km Ouest')
ax.set_title("Quibdo")
ax.set_ylabel("Quibdo (mm/3h)")
ax.legend()

groupes_jours = precip_sel.groupby('time.dayofyear')
for date, donnee in groupes_jours:
    total =+ donnee

precip_moyenne_journee = (total/30).values
heure_de_la_journee = ["19h", "22h", "1h", "4h", "7h", "10h", "13h", "16h"] #UTC-5 pour Quibdo

Cycle_Precip[0, 1].plot(heure_de_la_journee, precip_moyenne_journee)
Cycle_Precip[0, 1].set_title("Quibdó")
Cycle_Precip[0, 1].set_ylim(0, 0.03)
Cycle_Precip[0, 1].set_ylabel("Précip. moy. (mm)")
Cycle_Precip[0, 1].grid(True)

#Montréal
precip_sel=precipitation.sel(lat=45.5, lon=-73.5, method='nearest')
Taux_Precip[1,0].plot(precip_sel,'tab:green')
Taux_Precip[1,0].set_title("Précipitations à Montréal")

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
taux_precip_max = 0
for x in precip_sel.values :
    if x != 0:
        compte +=1
    if x == 0:
        nbr_consec = compte
        compte = 0
    if max_nbr_consec < nbr_consec:
        max_nbr_consec = nbr_consec
    if x > taux_precip_max:
        taux_precip_max = x

print("Durée maximale des événements de précipitations Montréal (h): " , max_nbr_consec*3)
print("Taux maximal de précipitation Montréal (mm/h) : " , taux_precip_max/3)

precip_sel_nord = precipitation.sel(lat=46.0, lon=-73.5, method='nearest')
precip_sel_sud = precipitation.sel(lat=45.0, lon=-73.5, method='nearest')
precip_sel_est = precipitation.sel(lat=45.5, lon=-72.9, method='nearest')
precip_sel_ouest = precipitation.sel(lat=45.5, lon=-74.1, method='nearest')

arr = np.array([precip_sel.values, precip_sel_nord.values, precip_sel_sud.values, precip_sel_est.values, precip_sel_ouest.values])
coef = np.corrcoef(arr, rowvar=True)
print("Coefficient à Montréal : " , coef)

ax = Variab_Points_Proches[1, 0]
ax.scatter(precip_sel_nord.values, precip_sel.values, color='blue', label='50km au Nord')
ax.scatter(precip_sel_sud.values, precip_sel.values, color='red', label='50km au Sud')
ax.scatter(precip_sel_est.values, precip_sel.values, color='green', label='50km Est')
ax.scatter(precip_sel_ouest.values, precip_sel.values, color='yellow', label='50km Ouest')
ax.set_title("Montréal")
ax.set_xlabel("Voisins (mm/3h)")
ax.set_ylabel("Montréal (mm/3h)")
ax.legend()

groupes_jours = precip_sel.groupby('time.dayofyear')
for date, donnee in groupes_jours:
    total =+ donnee

precip_moyenne_journee = (total/30).values
heure_de_la_journee = ["19h", "22h", "1h", "4h", "7h", "10h", "13h", "16h"] #UTC-5 pour Montréal

Cycle_Precip[1, 0].plot(heure_de_la_journee, precip_moyenne_journee)
Cycle_Precip[1, 0].set_title("Montréal")
Cycle_Precip[1, 0].set_ylim(0, 0.03)
Cycle_Precip[1, 0].set_ylabel("Précip. moy. (mm)")
Cycle_Precip[1, 0].set_xlabel("Heure de la journée")
Cycle_Precip[1, 0].grid(True)

#Océan
precip_sel=precipitation.sel(lat=5.0, lon=106.0, method='nearest')
Taux_Precip[1,1].plot(precip_sel,'tab:red')
Taux_Precip[1,1].set_title("Précipitations Océan")

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
taux_precip_max = 0
for x in precip_sel.values :
    if x != 0:
        compte +=1
    if x == 0:
        nbr_consec = compte
        compte = 0
    if max_nbr_consec < nbr_consec:
        max_nbr_consec = nbr_consec
    if x > taux_precip_max:
        taux_precip_max = x

print("Durée maximale des événements de précipitations Océan (h): " , max_nbr_consec*3)
print("Taux maximal de précipitation Océan (mm/h) : " , taux_precip_max/3)

precip_sel_nord = precipitation.sel(lat=5.5, lon=106.0, method='nearest')
precip_sel_sud = precipitation.sel(lat=4.5, lon=106.0, method='nearest')
precip_sel_est = precipitation.sel(lat=5.0, lon=106.5, method='nearest')
precip_sel_ouest = precipitation.sel(lat=5.0, lon=105.6, method='nearest')

arr = np.array([precip_sel.values, precip_sel_nord.values, precip_sel_sud.values, precip_sel_est.values, precip_sel_ouest.values])
coef = np.corrcoef(arr, rowvar=True)
print("Coefficient Océan : " , coef)

ax = Variab_Points_Proches[1, 1]
ax.scatter(precip_sel_nord.values, precip_sel.values, color='blue', label='50km au Nord')
ax.scatter(precip_sel_sud.values, precip_sel.values, color='red', label='50km au Sud')
ax.scatter(precip_sel_est.values, precip_sel.values, color='green', label='50km Est')
ax.scatter(precip_sel_ouest.values, precip_sel.values, color='yellow', label='50km Ouest')
ax.set_title("Océan")
ax.set_xlabel("Voisins (mm/3h)")
ax.set_ylabel("Océan (mm/3h)")
ax.legend()

groupes_jours = precip_sel.groupby('time.dayofyear')
for date, donnee in groupes_jours:
    total =+ donnee

precip_moyenne_journee = (total/30).values
heure_de_la_journee = ["8h", "11h", "14h", "17h", "20h", "23h", "2h", "5h"] #UTC+8 pour Océan

Cycle_Precip[1, 1].plot(heure_de_la_journee, precip_moyenne_journee)
Cycle_Precip[1, 1].set_title("Océan")
Cycle_Precip[1, 1].set_ylim(0, 0.03)
Cycle_Precip[1, 1].set_ylabel("Précip. moy. (mm)")
Cycle_Precip[1, 1].set_xlabel("Heure de la journée")
Cycle_Precip[1, 1].grid(True)

for ax in Taux_Precip.flat:
    ax.set(xlabel="Temps",ylabel="Précipitation")
for ax in Taux_Precip.flat:
    ax.label_outer()
plt.show() #Montre tous les graphiques

