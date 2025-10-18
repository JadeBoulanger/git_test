#imports
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

#1.0

def eq_discretisée(B, rho, sigma, N): #fonction pour discrétiser l'équation qui prend comme paramètres d'entrée B, rho, sigma et N

    # Valeurs des variables initiales
    n = math.sqrt(B * (rho-1))
    xt0 = n
    yt0 = n + 3
    zt0 = rho - 1

    # initialisation des variables pour la discrétisation
    yt = yt0
    xt = xt0
    zt = zt0
    x_t_plus_un = 0
    y_t_plus_un = 0

    delta_t = 0.001

    #initialisation des listes
    liste_xt = [xt0]
    liste_yt = [yt0]
    liste_zt = [zt0]
    liste_t = [0]

    #Boucle pour la discrétisation
    for pas_de_temps in range(0, N + 1): #crée une boucle partant de 0 avec un pas de temps de 1, allant jusqu'à N

        x_t_plus_un = ((sigma * (yt - xt)) * (delta_t)) + xt
        y_t_plus_un = (((xt * (rho - zt)) - yt) * (delta_t)) + yt
        z_t_plus_un = (((yt * xt) - (B * zt)) * (delta_t)) + zt

        #les valeurs au temps t + 1 deviennent les valeurs au temps t
        xt = x_t_plus_un
        yt = y_t_plus_un
        zt = z_t_plus_un

        #les valeurs pour le temps t sont ajoutées à leur liste respective
        liste_xt.append(xt)
        liste_yt.append(yt)
        liste_zt.append(zt)
        liste_t.append(delta_t * (pas_de_temps + 1)) #On ajoute 1 à la valeur du pas de temps, puisqu'on prend les valeurs de x, y et z +1, et on multiplie par le delta_t pour obtenir le vrai temps

    return liste_t, liste_xt, liste_yt, liste_zt #la fonction retourne les listes de t, xt, yt et zt comme paramètre (sous forme de liste)

#1.1

donnees = eq_discretisée(2.667, 1.0, 10, 20000) #on vient chercher la liste des variables rtournées par la fonction

#Graphique x, y et z en fonction du temps
fig1, solution_num = plt.subplots(3, 1, figsize=(5, 10))
solution_num[0].plot(donnees[0], donnees[1], label="x en fonction du temps") #on fait une série de x (liste à la position 1 dans la liste retournée par la fonction) en fonction du temps (position 0)
solution_num[0].plot(donnees[0], donnees[2], label="y en fonction du temps") #série de y en fonction de t
solution_num[0].plot(donnees[0], donnees[3], label="z en fonction du temps") #série de z en fonction de t
solution_num[0].set_title("x, y et z en fonction du temps")
solution_num[0].legend()
solution_num[0].set_xlabel("Temps (s)")

#Graphique x en fonction de y
solution_num[1].plot(donnees[2], donnees[1])
solution_num[1].set_title("x en fonction de y")
solution_num[1].set_xlabel("y")
solution_num[1].set_ylabel("x")

#Graphique x en fonction de z
solution_num[2].plot(donnees[3], donnees[1])
solution_num[2].set_title("x en fonction de z")
solution_num[2].set_xlabel("z")
solution_num[2].set_ylabel("x")

plt.tight_layout()
plt.savefig("fig1.png")

#1.2
donnees = eq_discretisée(2.667, 350.0, 10, 20000) #on va chercher les listes t, xt, yt, zt avec les paramètres désirés

#Graphique x, y et z en fonction du temps
fig2, solution_num = plt.subplots(3, 1, figsize=(5, 10))
solution_num[0].plot(donnees[0], donnees[1], label="x en fonction du temps")
solution_num[0].plot(donnees[0], donnees[2], label="y en fonction du temps")
solution_num[0].plot(donnees[0], donnees[3], label="z en fonction du temps")
solution_num[0].set_title("x, y et z en fonction du temps")
solution_num[0].legend()
solution_num[0].set_xlabel("Temps (s)")
solution_num[0].set_ylabel("x")

#Graphique x en fonction de y
solution_num[1].plot(donnees[2], donnees[1])
solution_num[1].set_title("x en fonction de y")
solution_num[1].set_xlabel("y")
solution_num[1].set_ylabel("x")

#Graphique x en fonction de z
solution_num[2].plot(donnees[3], donnees[1])
solution_num[2].set_title("x en fonction de z")
solution_num[0].set_xlabel("z")
solution_num[0].set_ylabel("x")

plt.tight_layout()
plt.savefig("fig2.png")

#1.3
donnees = eq_discretisée(2.667, 28.0, 10, 20000) #on va chercher les listes t, xt, yt, zt avec les paramètres désirés

#Graphique x, y et z en fonction du temps
fig3, solution_num = plt.subplots(3, 1, figsize=(5, 10))
solution_num[0].plot(donnees[0], donnees[1], label="x en fonction du temps")
solution_num[0].plot(donnees[0], donnees[2], label="y en fonction du temps")
solution_num[0].plot(donnees[0], donnees[3], label="z en fonction du temps")
solution_num[0].set_title("x, y et z en fonction du temps")
solution_num[0].legend()
solution_num[0].set_xlabel("Temps (s)")
solution_num[0].set_ylabel("x")

#Graphique x en fonction de y
solution_num[1].plot(donnees[2], donnees[1])
solution_num[1].set_title("x en fonction de y")
solution_num[1].set_xlabel("y")
solution_num[1].set_ylabel("x")

#Graphique x en fonction de z
solution_num[2].plot(donnees[3], donnees[1])
solution_num[2].set_title("x en fonction de z")
solution_num[2].set_xlabel("z")
solution_num[2].set_ylabel("x")

plt.tight_layout()
plt.savefig("fig3.png")

#2.0

def eq_discretisée2(B, rho, sigma, N, e): #Fonction pour discrétiser l'équation qui prend comme paramètres d'entrée B, rho, sigma, N et e, qui est la perturbation

    n = math.sqrt(B * (rho-1))
    xt0 = n + e
    yt0 = n + 3
    zt0 = rho - 1




    yt = yt0
    xt = xt0
    zt = zt0
    x_t_plus_un = 0
    y_t_plus_un = 0

    liste_xt = [xt0]
    liste_yt = [yt0]
    liste_zt = [zt0]
    liste_t = [0]
    delta_t = 0.001

    for pas_de_temps in range(0, N + 1): #crée une boucle partant de 0 avec un pas de temps de 1, allant jusqu'à N
        x_t_plus_un = ((sigma * (yt - xt)) * (delta_t)) + xt
        y_t_plus_un = (((xt * (rho - zt)) - yt) * (delta_t)) + yt
        z_t_plus_un = (((yt * xt) - (B * zt)) * (delta_t)) + zt

        xt = x_t_plus_un
        yt = y_t_plus_un
        zt = z_t_plus_un

        liste_xt.append(xt)
        liste_yt.append(yt)
        liste_zt.append(zt)
        liste_t.append(delta_t * (pas_de_temps + 1))

    return liste_t, liste_xt, liste_yt, liste_zt

#2.1

donnees1 = eq_discretisée(2.667, 28.0, 10, 40000) #pour obtenir la solution contrôle (sans perturbation)
donnees2 = eq_discretisée2(2.667, 28.0, 10, 40000, 0.01) #pour obtenir la solution perturbée avec e = 0,01

#graphique de x en fonction du temps pour la solution contrôle et perturbée
plt.figure()
plt.plot(donnees1[0], donnees1[1], label="x en fonction du temps CI contrôle")
plt.plot(donnees2[0], donnees2[1], label="x en fonction du temps CI perturbée")
plt.title("x en fonction du temps pour CI contrôle et CI perturbée")
plt.legend()
plt.xlabel("Temps (s)")
plt.ylabel("x")
plt.savefig("fig4.png")

#graphique de y en fonction du temps pour la solution contrôle et perturbée
plt.figure()
plt.plot(donnees1[0], donnees1[2], label="y en fonction du temps CI contrôle")
plt.plot(donnees2[0], donnees2[2], label="y en fonction du temps CI perturbée")
plt.title("y en fonction du temps pour CI contrôle et CI perturbée")
plt.legend()
plt.xlabel("Temps (s)")
plt.ylabel("y")
plt.savefig("fig5.png")

#graphique de z en fonction du temps pour la solution contrôle et perturbée
plt.figure()
plt.plot(donnees1[0], donnees1[3], label="z en fonction du temps CI contrôle")
plt.plot(donnees2[0], donnees2[3], label="z en fonction du temps CI perturbée")
plt.title("z en fonction du temps pour CI contrôle et CI perturbée")
plt.legend()
plt.xlabel("Temps (s)")
plt.ylabel("z")
plt.savefig("fig6.png")

#écarts-type de x, y et z pour la solution contrôle
ecart_type_CI_controle_x =  np.std(donnees1[1])
ecart_type_CI_controle_y =  np.std(donnees1[2])
ecart_type_CI_controle_z =  np.std(donnees1[3])

print("Écart type de la solution chaotique contrôle pour x : ", ecart_type_CI_controle_x)
print("Écart type de la solution chaotique contrôle pour y : ", ecart_type_CI_controle_y)
print("Écart type de la solution chaotique contrôle pour z : ", ecart_type_CI_controle_z)

#Calcul du premier pas de temps pour lequel la différence absolue entre la solution perturbée et la solution contrôlenest plus grande que l'écart type de la variable de la solution contrôle
for x in range(0, 40001) : #boucle de 0 à 40000 (le nombre de pas de temps)
    diff = abs(donnees2[1][x] - donnees1[1][x]) #différence absolue entre la solution perturbée et contrôle au temps x
    if diff > ecart_type_CI_controle_x: #si la différence est plus élevée que l'écart type, on sort de la boucle
        break

print("Prévisibilité de x pour la solution chaotique avec perturbation à x de + 0,01 : ", donnees2[0][x]) # premier pas de temps 𝒕 pour lequel la différence absolue entre la solution perturbée et la solution contrôle est plus grande que l’écart type de la variable

#2.2

#Prévisibilité selon la perturbation

#e = 0,000001
donnees2 = eq_discretisée2(2.667, 28.0, 10, 40000, 0.000001)

ecart_type_CI_controle_x =  np.std(donnees1[1])

for x in range(0, 40001) :
    diff = abs(donnees2[1][x] - donnees1[1][x])
    if diff > ecart_type_CI_controle_x:
        break
print(donnees2[0][x]) # premier pas de temps 𝒕 pour lequel la différence absolue entre la solution perturbée et la solution contrôle est plus grande que l’écart type de la variable

liste_previsibilite = [donnees2[0][x]] #La prévisibilité est ajoutée à la liste (Créée ici)

#e = 0,00001
donnees2 = eq_discretisée2(2.667, 28.0, 10, 40000, 0.00001)

ecart_type_CI_controle_x =  np.std(donnees1[1])

for x in range(0, 40001) :
    diff = abs(donnees2[1][x] - donnees1[1][x])
    if diff > ecart_type_CI_controle_x:
        break
print(donnees2[0][x])

liste_previsibilite.append(donnees2[0][x]) #La prévisibilité est ajoutée à la liste

#e = 0,0001
donnees2 = eq_discretisée2(2.667, 28.0, 10, 40000, 0.0001)

ecart_type_CI_controle_x =  np.std(donnees1[1])

for x in range(0, 40001) :
    diff = abs(donnees2[1][x] - donnees1[1][x])
    if diff > ecart_type_CI_controle_x:
        break
print(donnees2[0][x])

liste_previsibilite.append(donnees2[0][x]) #La prévisibilité est ajoutée à la liste

#e = 0,001
donnees2 = eq_discretisée2(2.667, 28.0, 10, 40000, 0.001)

ecart_type_CI_controle_x =  np.std(donnees1[1])

for x in range(0, 40001) :
    diff = abs(donnees2[1][x] - donnees1[1][x])
    if diff > ecart_type_CI_controle_x:
        break
print(donnees2[0][x])

liste_previsibilite.append(donnees2[0][x]) #La prévisibilité est ajoutée à la liste

#e = 0,01
donnees2 = eq_discretisée2(2.667, 28.0, 10, 40000, 0.01)

ecart_type_CI_controle_x =  np.std(donnees1[1])

for x in range(0, 40001) :
    diff = abs(donnees2[1][x] - donnees1[1][x])
    if diff > ecart_type_CI_controle_x:
        break
print(donnees2[0][x])

liste_previsibilite.append(donnees2[0][x]) #La prévisibilité est ajoutée à la liste

#e = 0,1
donnees2 = eq_discretisée2(2.667, 28.0, 10, 40000, 0.1)

ecart_type_CI_controle_x =  np.std(donnees1[1])

for x in range(0, 40001):
    diff = abs(donnees2[1][x] - donnees1[1][x])
    if diff > ecart_type_CI_controle_x:
        break
print(donnees2[0][x])

liste_previsibilite.append(donnees2[0][x]) #La prévisibilité est ajoutée à la liste


#Graphique
magnitude = [0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1] #Liste avec les valeurs des perturbations

#Graphique de la prévisibilité en fonction de la magnitude de la perturbation
plt.figure()
plt.plot(magnitude, liste_previsibilite)
plt.title("Prévisibilité en fonction de la magnitude de la perturbation")
plt.xscale('log') #Échelle logarithmique
plt.xlabel("Magnitude de la perturbation")
plt.ylabel("Prévisibilité (s)")
plt.savefig("fig7.png")

#2.3

def eq_discretisée2pars(B, rho, sigma, N, e, parx, pary): #fonction qui permet de changer les conditions initiales en x et y

    n = math.sqrt(B * (rho-1))
    xt0 = n + parx + e
    yt0 = n + pary
    zt0 = rho - 1




    yt = yt0
    xt = xt0
    zt = zt0
    x_t_plus_un = 0
    y_t_plus_un = 0

    liste_xt = [xt0]
    liste_yt = [yt0]
    liste_zt = [zt0]
    liste_t = [0]
    delta_t = 0.001

    for pas_de_temps in range(0, N + 1): #crée une boucle partant de 0 avec un pas de temps de 1, allant jusqu'à N
        x_t_plus_un = ((sigma * (yt - xt)) * (delta_t)) + xt
        y_t_plus_un = (((xt * (rho - zt)) - yt) * (delta_t)) + yt
        z_t_plus_un = (((yt * xt) - (B * zt)) * (delta_t)) + zt

        xt = x_t_plus_un
        yt = y_t_plus_un
        zt = z_t_plus_un

        liste_xt.append(xt)
        liste_yt.append(yt)
        liste_zt.append(zt)
        liste_t.append(delta_t * (pas_de_temps + 1))

    return liste_t, liste_xt, liste_yt, liste_zt


#xt0 = n - 2, yt0 = n + 1
donnees2 = eq_discretisée2pars(2.667, 28.0, 10, 40000, 0.01, (-2), 1)
donnees2_contrl = eq_discretisée2pars(2.667, 28.0, 10, 40000, 0, (-2), 1)

ecart_type_CI_controle_x =  np.std(donnees2_contrl[1])

for x in range(0, 40001):
    diff = abs(donnees2[1][x] - donnees1[1][x])
    if diff > ecart_type_CI_controle_x:
        break
print(donnees2[0][x])

liste_prev = [donnees2[0][x]]

#xt0 = n - 4, yt0 = n - 1
donnees2 = eq_discretisée2pars(2.667, 28.0, 10, 40000, 0.01, (-4), (-1))
donnees2_contrl = eq_discretisée2pars(2.667, 28.0, 10, 40000, 0, (-4), (-1))

ecart_type_CI_controle_x =  np.std(donnees2_contrl[1])

for x in range(0, 40001):
    diff = abs(donnees2[1][x] - donnees1[1][x])
    if diff > ecart_type_CI_controle_x:
        break
print(donnees2[0][x])

liste_prev.append(donnees2[0][x])

#xt0 = n - 6, yt0 = n - 3
donnees2 = eq_discretisée2pars(2.667, 28.0, 10, 40000, 0.01, (-6), (-3))
donnees2_contrl = eq_discretisée2pars(2.667, 28.0, 10, 40000, 0, (-6), (--3))

ecart_type_CI_controle_x =  np.std(donnees2_contrl[1])

for x in range(0, 40001):
    diff = abs(donnees2[1][x] - donnees1[1][x])
    if diff > ecart_type_CI_controle_x:
        break
print(donnees2[0][x])

liste_prev.append(donnees2[0][x])

#xt0 = n - 8, yt0 = n - 5
donnees2 = eq_discretisée2pars(2.667, 28.0, 10, 40000, 0.01, (-8), (-5))
donnees2_contrl = eq_discretisée2pars(2.667, 28.0, 10, 40000, 0, (-8), (-5))

ecart_type_CI_controle_x =  np.std(donnees2_contrl[1])

for x in range(0, 40001):
    diff = abs(donnees2[1][x] - donnees1[1][x])
    if diff > ecart_type_CI_controle_x:
        break
print(donnees2[0][x])

liste_prev.append(donnees2[0][x])

#Graphique prévisibilité en fonction de la condition initiale selon x
cond_init = ["xt0 = n - 2, yt0 = n + 1", "xt0 = n - 4, yt0 = n - 1", "xt0 = n - 6, yt0 = n - 3", "xt0 = n - 8, yt0 = n - 5"]

plt.figure()
plt.plot(cond_init, liste_prev)
plt.title("Prévisibilité en fonction de la valeur de la condition initiale selon x")
plt.xlabel("Conditions initiales")
plt.ylabel("Prévisibilité de x (s)")
plt.savefig("fig8.png")

#3
donnees3_crl = eq_discretisée2(2.667, 28.0, 10, 100000, 0) #solution contrôle
donnees3 = eq_discretisée2(2.667, 28.0, 10, 100000, 0.01) #solution perturbée

#Graphique quantité de variable x par bins
min_e = (min((min(donnees3_crl[1])), (min(donnees3[1])))) #min entre les deux mins de l'équation contrôle et perturbée
max_e = max((max(donnees3_crl[1])), (max(donnees3[1]))) #max entre les deux maxs de l'équation contrôle et perturbée
diff_max_min_sur_50 = (max_e - min_e)/50 #différence netre le max et le min divisé pas 50
bins = [min_e] #création de la liste de bins avec la valeur min en 0

#Boucle pour ajouter la valeur des bins à la liste jusqu'à 50 puisqu'il y a 50 bins
for lim in range(1, 51):
    val_bin = min_e + (lim * diff_max_min_sur_50)
    bins.append(val_bin)

#Graphique avec les histogrammes
fig9, solution_num = plt.subplots(3, 1, figsize=(5, 10))
solution_num[0].hist(donnees3_crl[1], bins=bins, alpha=0.5, label='Solution contrôle')
solution_num[0].hist(donnees3[1], bins=bins, alpha=0.5, label='Solution perturbée')
solution_num[0].set_title("Nombre de valeurs de x")
solution_num[0].set_xlabel("Valeurs de x réparties sur 50 intervalles")
solution_num[0].set_ylabel("Nombre de valeurs")
solution_num[0].legend()

#Graphique quantité de variable y par bins
min_e = (min((min(donnees3_crl[2])), (min(donnees3[2])))) #min entre les deux mins de l'équation contrôle et perturbée
max_e = max((max(donnees3_crl[2])), (max(donnees3[2]))) #max entre les deux maxs de l'équation contrôle et perturbée
diff_max_min_sur_50 = (max_e - min_e)/50
bins = [min_e]

for lim in range(1, 51):
    val_bin = min_e + (lim * diff_max_min_sur_50)
    bins.append(val_bin)

solution_num[1].hist(donnees3_crl[2], bins=bins, alpha=0.5, label='Solution contrôle')
solution_num[1].hist(donnees3[2], bins=bins, alpha=0.5, label='Solution perturbée')
solution_num[1].set_title("Nombre de valeurs de y")
solution_num[1].set_xlabel("Valeurs de y réparties sur 50 intervalles")
solution_num[1].set_ylabel("Nombre de valeurs")
solution_num[1].legend()

#Graphique quantité de variable z par bins
min_e = (min((min(donnees3_crl[3])), (min(donnees3[3])))) #min entre les deux mins de l'équation contrôle et perturbée
max_e = max((max(donnees3_crl[3])), (max(donnees3[3]))) #max entre les deux maxs de l'équation contrôle et perturbée
diff_max_min_sur_50 = (max_e - min_e)/50
bins = [min_e]

for lim in range(1, 51):
    val_bin = min_e + (lim * diff_max_min_sur_50)
    bins.append(val_bin)

solution_num[2].hist(donnees3_crl[3], bins=bins, alpha=0.5, label='Solution contrôle')
solution_num[2].hist(donnees3[3], bins=bins, alpha=0.5, label='Solution perturbée')
solution_num[2].set_title("Nombre de valeurs de z")
solution_num[2].set_xlabel("Valeurs de z réparties sur 50 intervalles")
solution_num[2].set_ylabel("Nombre de valeurs")
solution_num[2].legend()

plt.tight_layout()
plt.savefig("fig9.png")

#Tests statistique
test_statx = stats.ks_2samp(donnees3_crl[1], donnees3[1])
test_staty = stats.ks_2samp(donnees3_crl[2], donnees3[2])
test_statz = stats.ks_2samp(donnees3_crl[3], donnees3[3])

print(test_statx)
print(test_staty)
print(test_statz)

#Figure bonus
donnees_ctrl = eq_discretisée2(2.667, 28.0, 10, 40000, 0)
donnees_e1 = eq_discretisée2(2.667, 28.0, 10, 40000, 0.000001)
donnees_e2 = eq_discretisée2(2.667, 28.0, 10, 40000, 0.00001)
donnees_e3 = eq_discretisée2(2.667, 28.0, 10, 40000, 0.0001)
donnees_e4 = eq_discretisée2(2.667, 28.0, 10, 40000, 0.001)
donnees_e5 = eq_discretisée2(2.667, 28.0, 10, 40000, 0.01)
donnees_e6 = eq_discretisée2(2.667, 28.0, 10, 40000, 0.1)

#perturbation : 0,00001
diff = abs(donnees_e1[1][0] - donnees_ctrl[1][0])
liste_diff = [diff]

for x in range(1, 40002):
    diff = abs(donnees_e1[1][x] - donnees_ctrl[1][x])
    liste_diff.append(diff)

#perturbation : 0,0001
diff = abs(donnees_e2[1][0] - donnees_ctrl[1][0])
liste_diff2 = [diff]

for x in range(1, 40002):
    diff = abs(donnees_e2[1][x] - donnees_ctrl[1][x])
    liste_diff2.append(diff)


#plt.figure()
#plt.plot(donnees_e1[0], liste_diff, label="perturbation : 0,00001")

#perturbation : 0,001
diff = abs(donnees_e3[1][0] - donnees_ctrl[1][0])
liste_diff3 = [diff]

for x in range(1, 40002):
    diff = abs(donnees_e3[1][x] - donnees_ctrl[1][x])
    liste_diff3.append(diff)


#plt.figure()
#plt.plot(donnees_e1[0], liste_diff, label="perturbation : 0,00001")

#perturbation : 0,01
diff = abs(donnees_e4[1][0] - donnees_ctrl[1][0])
liste_diff4 = [diff]

for x in range(1, 40002):
    diff = abs(donnees_e4[1][x] - donnees_ctrl[1][x])
    liste_diff4.append(diff)


#plt.figure()
#plt.plot(donnees_e1[0], liste_diff, label="perturbation : 0,00001")

#perturbation : 0,1
diff = abs(donnees_e5[1][0] - donnees_ctrl[1][0])
liste_diff5 = [diff]

for x in range(1, 40002):
    diff = abs(donnees_e5[1][x] - donnees_ctrl[1][x])
    liste_diff5.append(diff)

plt.figure()
plt.plot(donnees_e1[0], liste_diff, label="perturbation : 0,00001")
#plt.plot(donnees_e2[0], liste_diff2, label="perturbation : 0,0001")
#plt.plot(donnees_e3[0], liste_diff3, label="perturbation : 0,001")
#plt.plot(donnees_e4[0], liste_diff4, label="perturbation : 0,01")
plt.plot(donnees_e5[0], liste_diff5, label="perturbation : 0,1")
plt.title("Différence absolue entre la solution de x perturbée et la solution contrôle")
plt.xlabel("Temps (s)")
plt.ylabel("x")
plt.legend()

plt.savefig("fig10.png")

plt.show()