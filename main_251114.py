#Imports
import matplotlib.pyplot as plt
#Fonction pour calculer Ts et Ta

def Ts_Ta(a, Es, Ea):
    So = 1365 #W/m^2, constante solaire
    sigma = 5.67 * (10**(-8)) #W/m^2 K^4, constante de Stefan Boltzmann
    Ts=(((1-a)*So)/(4*sigma*(Es-(Ea/2))))**(1/4)
    Ta=(Es*(Ts**4)/2)**(1/4)
    return Ts, Ta

#x = Ts_Ta(0.3, 1, 0.77)
#print(x)

#Tests de sensibilité
#Variation de a
liste_Ts = []
liste_Ta = []
liste_a = []

for n in range (0, 101): #boucle pour avoir la valeur de Ts et Ta pour les valeurs de a de 0 à 1
    a = n / 100
    Ts, Ta = Ts_Ta(a, 1, 0.77)
    liste_a.append(a)
    liste_Ts.append(Ts)
    liste_Ta.append(Ta)

fig, axes = plt.subplots(1, 2)
#Graphique
axes[0].plot(liste_a, liste_Ts, label='Ts en fonction de a')
axes[0].plot(liste_a, liste_Ta, label='Ta en fonction de a')
axes[0].set_xlabel('Albédo (a)')
axes[0].set_ylabel('Température en K')
axes[0].set_title('Ts et Ta en fonction de a')
axes[0].legend()

#Variation de Ea
liste_Ts = []
liste_Ta = []
liste_Ea = []

for n in range (0, 101): #boucle pour avoir la valeur de Ts et Ta pour les valeurs de a de 0 à 1
    Ea = n / 100
    Ts, Ta = Ts_Ta(0.3, 1, Ea)
    liste_Ea.append(Ea)
    liste_Ts.append(Ts)
    liste_Ta.append(Ta)

#Graphique
axes[1].plot(liste_Ea, liste_Ts, label='Ts en fonction de Ea')
axes[1].plot(liste_Ea, liste_Ta, label='Ta en fonction de Ea')
axes[1].set_xlabel('Émissivité atmosphère (Ea)')
axes[1].set_ylabel('Température en K')
axes[1].set_title('Ts et Ta en fonction de Ea')
axes[1].legend()

plt.tight_layout()
plt.savefig("Figure 0.png")
plt.close()

#atmosphère en équilibre radiatif
#!/usr/bin/env python
# coding: utf-8
import os
import numpy as np
import matplotlib.pyplot as plt
import climlab
from climlab import constants as constants
import sys
import xarray as xr
import pdb
import copy as cp

# Pour fixer la taille de la police partout
import matplotlib as matplotlib
font = {'family' : 'monospace',
        'size'   : 15}
matplotlib.rc('font', **font)

outpath='./figures/' # repertoire pour les figures, il faut le creer dans votre repertoire

units=r'W m$^{-2}$' # Unités puisance
alb=.25 # Albedo surface
levels=np.arange(200,330,20)
levels=[298]
Tlims=[180,310]
Nz=30 # nombre de niveaux verticaux

# Load the reference vertical temperature profile from the NCEP reanalysis
ncep_lev=np.load('npy/ncep_lev.npy')
ncep_T=np.load('npy/ncep_T.npy')+273.15

#  State variables (Air and surface temperature)
state = climlab.column_state(num_lev=30)

#  Fixed relative humidity
h2o = climlab.radiation.ManabeWaterVapor(name='WaterVapor', state=state)

#  Couple water vapor to radiation
rad = climlab.radiation.RRTMG(name='Radiation', state=state, specific_humidity=h2o.q, albedo=alb)

# Creation d'un modele couplé avec rayonemment et vapour d'eau
rcm = climlab.couple([rad,h2o], name='Radiative-Equilibrium Model')
rcm2 = climlab.process_like(rcm) # creation d'un clone du modele rcm

print('\n','\n','********************************************')
print('Control simulation ')
print('********************************************')
# Make the initial state isothermal
rcm.state.Tatm[:] = rcm.state.Ts
T=[]
q=[]
tr=[]
print(state)
# Plot temperature
plt.figure()
for t in range(1000):
    T.append(cp.deepcopy(rcm.Tatm))
    q.append(cp.deepcopy(rcm.q))
    plt.plot(rcm.Tatm,rcm.lev[::-1])
    rcm.step_forward() #run the model forward one time step
    if abs(rcm.ASR - rcm.OLR)<1: # in W/m2
        tr.append(t)
plt.title('equilibrium reached at time t='+str(tr[0]))
plt.xlabel('temperature (K)')
plt.ylabel('pression (hPa)')
plt.gca().invert_yaxis()
fig_name=outpath+'fig1.png'
plt.savefig(fig_name,bbox_inches='tight')
plt.close()
print('output figure: ', fig_name)

#Plot humidity
for t in range(1000):
    plt.plot(q[t],rcm.lev[::-1])
plt.xlabel('specific humidity (kg/kg)')
plt.ylabel('pression (hPa)')
fig_name=outpath+'fig2.png'
plt.gca().invert_yaxis()
plt.savefig(fig_name,bbox_inches='tight')
plt.close()
print('output figure: ', fig_name)

# Quel est la sortie du modèle ?
print('diagnostics: ',rcm.diagnostics,'\n')
print('tendencies',rcm.tendencies,'\n')
print('Tair: ',rcm.Tatm,'\n')
print('albedo',rcm.SW_flux_up[-1]/rcm.SW_flux_down[-1],'\n')
print('co2',rad.absorber_vmr['CO2'],'\n') #volumetric mixing ratio
print('ch4',rad.absorber_vmr['CH4'],'\n') #volumetric mixing ratio
print('O3', rad.absorber_vmr['O3'],'\n') #volumetric mixing ratio)

print(rcm.lev)
print(rcm.Ts)


print('\n','\n','********************************************')
print('Sensitivity to the concentration of gases in the atmosphere')
print('********************************************')



#Pour les concentrations nulles de gaz
colors=['k','r','g','orange']
plt.plot(rcm.Tatm[::-1], rcm.lev[::-1], marker='s', color=colors[0],label='control')
plt.plot(rcm.Ts, 1000, marker='s',color=colors[0])
T_surface_ctrl = rcm.Ts

for gi,gg in enumerate(['O3','CO2','CH4']):
    state = climlab.column_state(num_lev=30)
    h2o = climlab.radiation.ManabeWaterVapor(name='WaterVapor', state=state)
    rad = climlab.radiation.RRTMG(name='Radiation', state=state, specific_humidity=h2o.q, albedo=alb)
    rcm = climlab.couple([rad,h2o], name='Radiative-Convective Model')
    rcm.absorber_vmr[gg] = 0
    rcm.integrate_years(2) # Run the model for two years
    plt.plot(rcm.Tatm[::-1], rcm.lev[::-1], marker='s', label='non-'+gg,color=colors[gi+1])
    plt.plot(rcm.Ts, 1000, marker='s',color=colors[gi+1])
plt.plot(ncep_T, ncep_lev, marker='x',color='k',label='NCEP reanalysis')
plt.gca().invert_yaxis()
plt.title('Sensitivity: gases')
plt.ylabel('Pression (hPa)')
plt.xlabel('Temperature (K)')
plt.gca().legend(loc='center left', bbox_to_anchor=(1, 0.5))
fig_name=outpath+'fig3.png'
print('output figure: ', fig_name)
plt.savefig(fig_name,bbox_inches='tight')
plt.close()

#Pour les concentrations doublées de gaz
colors=['k','r','g','orange']
plt.plot(rcm.Tatm[::-1], rcm.lev[::-1], marker='s', color=colors[0],label='control')
plt.plot(rcm.Ts, 1000, marker='s',color=colors[0])

for gi,gg in enumerate(['O3','CO2','CH4']):
    state = climlab.column_state(num_lev=30)
    h2o = climlab.radiation.ManabeWaterVapor(name='WaterVapor', state=state)
    rad = climlab.radiation.RRTMG(name='Radiation', state=state, specific_humidity=h2o.q, albedo=alb)
    rcm = climlab.couple([rad,h2o], name='Radiative-Convective Model')
    rcm.absorber_vmr[gg] *= 2
    rcm.integrate_years(2) # Run the model for two years
    plt.plot(rcm.Tatm[::-1], rcm.lev[::-1], marker='s', label='x2 '+gg,color=colors[gi+1])
    plt.plot(rcm.Ts, 1000, marker='s',color=colors[gi+1])
    if gg =='CO2':
        deuxCO2 = rcm.Ts

plt.plot(ncep_T, ncep_lev, marker='x',color='k',label='NCEP reanalysis')
plt.gca().invert_yaxis()
plt.title('Sensitivity: gases')
plt.ylabel('Pression (hPa)')
plt.xlabel('Temperature (K)')
plt.gca().legend(loc='center left', bbox_to_anchor=(1, 0.5))
fig_name=outpath+'fig3_1.png'
print('output figure: ', fig_name)
plt.savefig(fig_name,bbox_inches='tight')
plt.close()



#Pour les concentrations quadruplées de gaz
colors=['k','r','g','orange', 'b']
plt.plot(rcm.Tatm[::-1], rcm.lev[::-1], marker='s', color=colors[0],label='control')
plt.plot(rcm.Ts, 1000, marker='s',color=colors[0])

for gi,gg in enumerate(['O3','CO2','CH4']):
    state = climlab.column_state(num_lev=30)
    h2o = climlab.radiation.ManabeWaterVapor(name='WaterVapor', state=state)
    rad = climlab.radiation.RRTMG(name='Radiation', state=state, specific_humidity=h2o.q, albedo=alb)
    rcm = climlab.couple([rad,h2o], name='Radiative-Convective Model')
    rcm.absorber_vmr[gg] *= 4
    rcm.integrate_years(2) # Run the model for two years
    plt.plot(rcm.Tatm[::-1], rcm.lev[::-1], marker='s', label='x4 '+gg,color=colors[gi+1])
    plt.plot(rcm.Ts, 1000, marker='s',color=colors[gi+1])
plt.plot(ncep_T, ncep_lev, marker='x',color='k',label='NCEP reanalysis')
plt.gca().invert_yaxis()
plt.title('Sensitivity: gases')
plt.ylabel('Pression (hPa)')
plt.xlabel('Temperature (K)')
plt.gca().legend(loc='center left', bbox_to_anchor=(1, 0.5))
fig_name=outpath+'fig3_2.png'
print('output figure: ', fig_name)
plt.savefig(fig_name,bbox_inches='tight')
plt.close()

#Pour les concentrations préindustrielles vs aujourd'hui de gaz
#Aujourd'hui
state = climlab.column_state(num_lev=30)
h2o = climlab.radiation.ManabeWaterVapor(name='WaterVapor', state=state)
rad = climlab.radiation.RRTMG(name='Radiation', state=state, specific_humidity=h2o.q, albedo=alb)
rcm = climlab.couple([rad,h2o], name='Radiative-Convective Model')
rcm.absorber_vmr['CO2'] = 0.000422
rcm.absorber_vmr['CH4'] = 0.00000192
rcm.integrate_years(2) # Run the model for two years
plt.plot(rcm.Tatm[::-1], rcm.lev[::-1], marker='s', label='Concentrations présentement ',color=colors[2])
plt.plot(rcm.Ts, 1000, marker='s',color=colors[2])
#print(rcm.absorber_vmr['O3'])

#Préindustriel
state = climlab.column_state(num_lev=30)
h2o = climlab.radiation.ManabeWaterVapor(name='WaterVapor', state=state)
rad = climlab.radiation.RRTMG(name='Radiation', state=state, specific_humidity=h2o.q, albedo=alb)
rcm = climlab.couple([rad,h2o], name='Radiative-Convective Model')
rcm.absorber_vmr['O3'][np.arange(7, 30)] = rcm.absorber_vmr['O3'][np.arange(7, 30)]/1.5 #modification de la concentration d'ozone uniquement dans le troposphère
rcm.absorber_vmr['CO2'] = 0.000284
rcm.absorber_vmr['CH4'] = 0.00000073
rcm.integrate_years(2) # Run the model for two years
plt.plot(rcm.Tatm[::-1], rcm.lev[::-1], marker='s', label='Concentrations préindustrielles ',color=colors[1])
plt.plot(rcm.Ts, 1000, marker='s',color=colors[1])
plt.gca().invert_yaxis()
plt.title('Sensitivity: gases')
plt.ylabel('Pression (hPa)')
plt.xlabel('Temperature (K)')
plt.gca().legend(loc='center left', bbox_to_anchor=(1, 0.5))
fig_name=outpath+'fig3_3.png'
print('output figure: ', fig_name)
plt.savefig(fig_name,bbox_inches='tight')
plt.close()


print('\n','\n','********************************************')
print('Sensitivity to albedo')
print('********************************************')
albedos=np.arange(.1,.4,.1)
rcms={}
for alb in albedos:
    state = climlab.column_state(num_lev=30)
    h2o = climlab.radiation.ManabeWaterVapor(name='WaterVapor', state=state)
    rad = climlab.radiation.RRTMG(name='Radiation', state=state, specific_humidity=h2o.q, albedo=alb)
    rcm = climlab.couple([rad,h2o], name='Radiative-Convective Model')
    rcms['rcm'+str(alb)]=rcm

for ai,alb in enumerate(albedos):
    rcms['rcm'+str(alb)].integrate_years(2)
    plt.plot(rcms['rcm'+str(alb)].Tatm[::-1], rcm.lev[::-1], marker='s', label=r'$\alpha$='+str(np.round(alb,1)),color=colors[ai])
    plt.plot(rcms['rcm'+str(alb)].Ts, 1000, marker='s',color=colors[ai])
#rcm.absorber_vmr['CO2'] *= 2
#plt.plot(rcm.Tatm[::-1], rcm.lev[::-1], marker='s', label='x2 CO2 ',color='b')
#plt.plot(rcm.Ts, 1000, marker='s',color='b')
plt.plot(ncep_T, ncep_lev, marker='x',color='k',label='NCEP reanalysis')
plt.gca().invert_yaxis()
plt.title('Sensitivity: albedo')
plt.ylabel('Pression (hPa)')
plt.xlabel('Temperature (K)')
plt.gca().legend(loc='center left', bbox_to_anchor=(1, 0.5))
fig_name=outpath+'fig4.png'
print('output figure: ', fig_name)
plt.savefig(fig_name,bbox_inches='tight')
plt.close()

#Calcul changement de température de surface associé à un doublement de la concentration de CO₂
changement_T = deuxCO2 - T_surface_ctrl

print(deuxCO2, T_surface_ctrl, changement_T)

#variation d’albédo qui permettrait de compenser ce réchauffement
albedos=np.arange(.25,.27,.001)
rcms={}
for alb in albedos:
    state = climlab.column_state(num_lev=30)
    h2o = climlab.radiation.ManabeWaterVapor(name='WaterVapor', state=state)
    rad = climlab.radiation.RRTMG(name='Radiation', state=state, specific_humidity=h2o.q, albedo=alb)
    rcm = climlab.couple([rad,h2o], name='Radiative-Convective Model')
    rcms['rcm'+str(alb)]=rcm

for ai,alb in enumerate(albedos):
    rcms['rcm'+str(alb)].integrate_years(2)
    #plt.plot(rcms['rcm'+str(alb)].Tatm[::-1], rcm.lev[::-1], marker='s', label=r'$\alpha$='+str(np.round(alb,1)),color=colors[ai])
    #plt.plot(rcms['rcm'+str(alb)].Ts, 1000, marker='s',color=colors[ai])
    #print(T_surface_ctrl - rcms['rcm'+str(alb)].Ts)
    if (T_surface_ctrl - rcms['rcm'+str(alb)].Ts) < 1.64 and (T_surface_ctrl - rcms['rcm'+str(alb)].Ts) > 1.62:
        break
print(alb)

print('\n','\n','********************************************')
print('Sensitivity to convection')
print('********************************************')
alb=.25
state = climlab.column_state(num_lev=30)
h2o = climlab.radiation.ManabeWaterVapor(name='WaterVapor', state=state)
rad = climlab.radiation.RRTMG(name='Radiation', state=state, specific_humidity=h2o.q, albedo=alb)
rcms={}
rcms['rcm0'] = climlab.couple([rad,h2o], name='Radiative-Convective Model')
conv = climlab.convection.ConvectiveAdjustment(name='Convection', state=state, adj_lapse_rate=6.5)
rcms['rcm1'] = climlab.couple([rad,conv,h2o], name='Radiative-Convective Model')
conv = climlab.convection.ConvectiveAdjustment(name='Convection', state=state, adj_lapse_rate=9.8) #lapse rate in degC per km
rcms['rcm2'] = climlab.couple([rad,conv,h2o], name='Radiative-Convective Model')
conv = climlab.convection.ConvectiveAdjustment(name='Convection', state=state, adj_lapse_rate=0) #lapse rate in degC per km
rcms['rcm3'] = climlab.couple([rad,conv,h2o], name='Radiative-Convective Model')
conv = climlab.convection.ConvectiveAdjustment(name='Convection', state=state, adj_lapse_rate=-2) #lapse rate in degC per km
rcms['rcm4'] = climlab.couple([rad,conv,h2o], name='Radiative-Convective Model')

mod_name=['control','conv-6.5','conv-9.8', 'conv-0', 'conv--2']
for ai in range(5):
    rcms['rcm'+str(ai)].integrate_years(2)
    plt.plot(rcms['rcm'+str(ai)].Tatm[::-1], rcm.lev[::-1], marker='s', label=mod_name[ai],color=colors[ai])
    plt.plot(rcms['rcm'+str(ai)].Ts, 1000, marker='s',color=colors[ai])
plt.plot(ncep_T, ncep_lev, marker='x',color='k',label='NCEP reanalysis')
plt.gca().invert_yaxis()
plt.title('Sensitivity: convection')
plt.ylabel('Pression (hPa)')
plt.xlabel('Temperature (K)')
plt.gca().legend(loc='center left', bbox_to_anchor=(1, 0.5))
fig_name=outpath+'fig5.png'
print('output figure: ', fig_name)
plt.savefig(fig_name,bbox_inches='tight')
plt.close()

#Figures bonus

#1. Variation T surface selon la variation de la concentration des gaz
liste_TsCO2 = []
liste_TsCH4 = []
liste_TsO3 = []

for concentration in range(1,5):
    state = climlab.column_state(num_lev=30)
    h2o = climlab.radiation.ManabeWaterVapor(name='WaterVapor', state=state)
    rad = climlab.radiation.RRTMG(name='Radiation', state=state, specific_humidity=h2o.q, albedo=alb)
    rcm = climlab.couple([rad,h2o], name='Radiative-Convective Model')
    rcm.absorber_vmr['CO2'] = rcm.absorber_vmr['CO2']*concentration
    rcm.integrate_years(2) # Run the model for two years
    liste_TsCO2.append(rcm.Ts - T_surface_ctrl)

for concentration in range(1,5):
    state = climlab.column_state(num_lev=30)
    h2o = climlab.radiation.ManabeWaterVapor(name='WaterVapor', state=state)
    rad = climlab.radiation.RRTMG(name='Radiation', state=state, specific_humidity=h2o.q, albedo=alb)
    rcm = climlab.couple([rad,h2o], name='Radiative-Convective Model')
    rcm.absorber_vmr['CH4'] = rcm.absorber_vmr['CH4']*concentration
    rcm.integrate_years(2) # Run the model for two years
    liste_TsCH4.append(rcm.Ts - T_surface_ctrl)

for concentration in range(1,5):
    state = climlab.column_state(num_lev=30)
    h2o = climlab.radiation.ManabeWaterVapor(name='WaterVapor', state=state)
    rad = climlab.radiation.RRTMG(name='Radiation', state=state, specific_humidity=h2o.q, albedo=alb)
    rcm = climlab.couple([rad,h2o], name='Radiative-Convective Model')
    rcm.absorber_vmr['O3'] = rcm.absorber_vmr['O3']*concentration
    rcm.integrate_years(2) # Run the model for two years
    liste_TsO3.append(rcm.Ts - T_surface_ctrl)

liste_Ts = []

for concentration in range(1,5):
    state = climlab.column_state(num_lev=30)
    h2o = climlab.radiation.ManabeWaterVapor(name='WaterVapor', state=state)
    rad = climlab.radiation.RRTMG(name='Radiation', state=state, specific_humidity=h2o.q, albedo=alb)
    rcm = climlab.couple([rad,h2o], name='Radiative-Convective Model')
    rcm.absorber_vmr['CO2'] = rcm.absorber_vmr['CO2']*concentration
    rcm.absorber_vmr['CH4'] = rcm.absorber_vmr['CH4'] * concentration
    rcm.absorber_vmr['O3'] = rcm.absorber_vmr['O3'] * concentration
    #rcm.absorber_vmr['O3'][np.arange(7, 30)] = rcm.absorber_vmr['O3'][np.arange(7, 30)] * concentration  # modification de la concentration d'ozone uniquement dans le troposphère
    rcm.integrate_years(2) # Run the model for two years
    liste_Ts.append(rcm.Ts - T_surface_ctrl)

plt.plot([1,2,3,4], liste_TsCO2, label='CO2')
plt.plot([1,2,3,4], liste_TsCH4, label='CH4')
plt.plot([1,2,3,4], liste_TsO3, label='O3')
plt.plot([1,2,3,4], np.array(liste_TsCO2) + np.array(liste_TsCH4) + np.array(liste_TsO3), label = 'Augmentation T additionée de CO2, CH4, O3')
plt.plot([1,2,3,4], liste_Ts, label='CO2, CH4 et O3 combinés')
plt.title('Augmentation T surface en fonction du facteur de concentration')
plt.ylabel('Augmentation T surface (°C)')
plt.xlabel('Facteur de concentration')
plt.xticks([1,2,3,4])
plt.gca().legend(loc='center left', bbox_to_anchor=(1, 0.5))
fig_name=outpath+'fig6.png'
print('output figure: ', fig_name)
plt.savefig(fig_name,bbox_inches='tight')
plt.close()

print(liste_TsCO2, liste_TsCH4, liste_TsO3, liste_Ts)

