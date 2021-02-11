# importation des librairies
import numpy as np
import csv
import sys
from matplotlib import pyplot as plt

# en argument
if len(sys.argv)==1 :
    print ("Vous devez spécifier le chemin du fichier en argument")
    quit()

lien_fichier = sys.argv[1]

barre = False
day_limit = 0
if len(sys.argv)==3 :
    barre = True
    day_limit = int(sys.argv[2])

#----------------- CALCUL DU NOMBRE DE TOURNOIS ---------
nbr_tournois = 0
nbr_mains_par_tournois = 0
liste_tournois = []
with open(lien_fichier,'r') as csv_file :
    csv_reader_tournois = csv.reader(csv_file, delimiter=',')
    for ligne in csv_reader_tournois :
        liste_tournois.append(ligne[7])
liste_tournois = list(set(liste_tournois))
nbr_tournois = len(liste_tournois)-1

#----------------- TOUTES LES POSITIONS -----------------

# initialisation variables
main_limite_tpositions = 0
nbr_mains_tpositions = 0
c = 0
k = 0
with open(lien_fichier,'r') as csv_file :
    csv_reader1 = csv.reader(csv_file, delimiter=',')
    for ligne in csv_reader1 :
        nbr_mains_tpositions += 1
        if k == 1 : 
            if float(ligne[15]) == day_limit and c == 0 :
                main_limite_tpositions = nbr_mains_tpositions
                c = 1
        k = 1
nbr_mains_tpositions -= 1

# calcul du nombre de mains par tournois
nbr_mains_par_tournois = nbr_mains_tpositions / nbr_tournois

courbe_cEV_tpositions = np.zeros(nbr_mains_tpositions)
courbe_cEV_espere_tpositions = np.zeros(nbr_mains_tpositions)
mains_tpositions = np.arange(nbr_mains_tpositions)

# création du tableau de cEV pour toutes les positions
i = 0
with open(lien_fichier,'r') as csv_file :
    csv_reader2 = csv.reader(csv_file, delimiter=',')
    for ligne in csv_reader2 :
        if i == 0 :
            i+=1
            continue
        elif i == 1 :
            courbe_cEV_tpositions[0] = float(ligne[24])/100+float(ligne[34])/100
        else :
            courbe_cEV_tpositions[i-1] = courbe_cEV_tpositions[i-2] + float(ligne[24])/100 + float(ligne[34])/100
        i+=1

cEV_tpositions = (courbe_cEV_tpositions[nbr_mains_tpositions-1] - courbe_cEV_tpositions[0])/(nbr_mains_tpositions/nbr_mains_par_tournois)
        
# création du tableau de cEV espéré pour toutes les positions
cEV_espere_tpositions = 90
for j in range(nbr_mains_tpositions) :
    if j == 0 :
        courbe_cEV_espere_tpositions[0] = cEV_espere_tpositions/nbr_mains_par_tournois
    else :
        courbe_cEV_espere_tpositions[j] = courbe_cEV_espere_tpositions[j-1] + cEV_espere_tpositions/nbr_mains_par_tournois
        

#----------------- THREE WAY SB -----------------

# initialisation variables
main_limite_tw = 0
c = 0
nbr_mains_tw_SB = 0
with open(lien_fichier,'r') as csv_file :
    csv_reader3 = csv.reader(csv_file, delimiter=',')
    for ligne in csv_reader3 :
        if (ligne[31] == '3') and (ligne[13] == '2') :
            nbr_mains_tw_SB += 1
            if float(ligne[15]) == day_limit and c == 0 :
                main_limite_tw = nbr_mains_tw_SB
                c = 1
    
courbe_cEV_tw_SB = np.zeros(nbr_mains_tw_SB)
courbe_cEV_espere_tw_SB = np.zeros(nbr_mains_tw_SB)
mains_tw_SB = np.arange(nbr_mains_tw_SB)

# création du tableau de cEV pour la SB en three way
i = 0
with open(lien_fichier,'r') as csv_file :
    csv_reader4 = csv.reader(csv_file, delimiter=',')
    for ligne in csv_reader4 :
        if i == 0 :
            i+=1
            continue
        elif i == 1 and ligne[31] == '3' and ligne[13] == '2' :
            courbe_cEV_tw_SB[0] = float(ligne[24])/100+float(ligne[34])/100
            i+=1
        elif ligne[31] == '3' and ligne[13] == '2' :
            courbe_cEV_tw_SB[i-1] = courbe_cEV_tw_SB[i-2] + float(ligne[24])/100 + float(ligne[34])/100
            i+=1
            
# calcul du cEV
pourcentage_mains_tw_SB = nbr_mains_tw_SB/nbr_mains_tpositions
        
cEV_tw_SB = (courbe_cEV_tw_SB[nbr_mains_tw_SB-1] - courbe_cEV_tw_SB[0])/(nbr_mains_tw_SB)*nbr_mains_par_tournois*pourcentage_mains_tw_SB

# création du tableau de cEV pour la SB en three way
cEV_espere_tw_SB = 0
for j in range(nbr_mains_tw_SB) :
    if j == 0 :
        courbe_cEV_espere_tw_SB[0] = cEV_espere_tw_SB/nbr_mains_par_tournois/pourcentage_mains_tw_SB
    else :
        courbe_cEV_espere_tw_SB[j] = courbe_cEV_espere_tw_SB[j-1] + cEV_espere_tw_SB/nbr_mains_par_tournois/pourcentage_mains_tw_SB


#----------------- THREE WAY BB -----------------

# initialisation variables
nbr_mains_tw_BB = 0
with open(lien_fichier,'r') as csv_file :
    csv_reader5 = csv.reader(csv_file, delimiter=',')
    for ligne in csv_reader5 :
        if (ligne[31] == '3') and (ligne[13] == '1') :
            nbr_mains_tw_BB += 1
    
courbe_cEV_tw_BB = np.zeros(nbr_mains_tw_BB)
courbe_cEV_espere_tw_BB = np.zeros(nbr_mains_tw_BB)
mains_tw_BB = np.arange(nbr_mains_tw_BB)

# création du tableau de cEV pour la BB en three way
i = 0
with open(lien_fichier,'r') as csv_file :
    csv_reader6 = csv.reader(csv_file, delimiter=',')
    for ligne in csv_reader6 :
        if i == 0 :
            i+=1
            continue
        elif i == 1 and ligne[31] == '3' and ligne[13] == '1' :
            courbe_cEV_tw_BB[0] = float(ligne[24])/100+float(ligne[34])/100
            i+=1
        elif ligne[31] == '3' and ligne[13] == '1' :
            courbe_cEV_tw_BB[i-1] = courbe_cEV_tw_BB[i-2] + float(ligne[24])/100 + float(ligne[34])/100
            i+=1
            
# calcul du cEV
pourcentage_mains_tw_BB = nbr_mains_tw_BB/nbr_mains_tpositions
        
cEV_tw_BB = (courbe_cEV_tw_BB[nbr_mains_tw_BB-1] - courbe_cEV_tw_BB[0])/(nbr_mains_tw_BB)*nbr_mains_par_tournois*pourcentage_mains_tw_BB

# création du tableau de cEV pour la BB en three way
cEV_espere_tw_BB = 0
for j in range(nbr_mains_tw_BB) :
    if j == 0 :
        courbe_cEV_espere_tw_BB[0] = cEV_espere_tw_BB/nbr_mains_par_tournois/pourcentage_mains_tw_BB
    else :
        courbe_cEV_espere_tw_BB[j] = courbe_cEV_espere_tw_BB[j-1] + cEV_espere_tw_BB/nbr_mains_par_tournois/pourcentage_mains_tw_BB



#----------------- THREE WAY BTN -----------------

# initialisation variables
nbr_mains_tw_BTN = 0
with open(lien_fichier,'r') as csv_file :
    csv_reader7 = csv.reader(csv_file, delimiter=',')
    for ligne in csv_reader7 :
        if (ligne[31] == '3') and (ligne[13] == '3') :
            nbr_mains_tw_BTN += 1
    
courbe_cEV_tw_BTN = np.zeros(nbr_mains_tw_BTN)
courbe_cEV_espere_tw_BTN = np.zeros(nbr_mains_tw_BTN)
mains_tw_BTN = np.arange(nbr_mains_tw_BTN)

# création du tableau de cEV pour le BTN en three way
i = 0
with open(lien_fichier,'r') as csv_file :
    csv_reader8 = csv.reader(csv_file, delimiter=',')
    for ligne in csv_reader8 :
        if i == 0 :
            i+=1
            continue
        elif i == 1 and ligne[31] == '3' and ligne[13] == '3' :
            courbe_cEV_tw_BTN[0] = float(ligne[24])/100+float(ligne[34])/100
            i+=1
        elif ligne[31] == '3' and ligne[13] == '3' :
            courbe_cEV_tw_BTN[i-1] = courbe_cEV_tw_BTN[i-2] + float(ligne[24])/100 + float(ligne[34])/100
            i+=1
            
# calcul du cEV
pourcentage_mains_tw_BTN = nbr_mains_tw_BTN/nbr_mains_tpositions
        
cEV_tw_BTN = (courbe_cEV_tw_BTN[nbr_mains_tw_BTN-1] - courbe_cEV_tw_BTN[0])/(nbr_mains_tw_BTN)*nbr_mains_par_tournois*pourcentage_mains_tw_BTN

# création du tableau de cEV pour le BTN en three way
cEV_espere_tw_BTN = 30
for j in range(nbr_mains_tw_BTN) :
    if j == 0 :
        courbe_cEV_espere_tw_BTN[0] = cEV_espere_tw_BTN/nbr_mains_par_tournois/pourcentage_mains_tw_BTN
    else :
        courbe_cEV_espere_tw_BTN[j] = courbe_cEV_espere_tw_BTN[j-1] + cEV_espere_tw_BTN/nbr_mains_par_tournois/pourcentage_mains_tw_BTN

#----------------- HU BTN -----------------

# initialisation variables
main_limite_hu = 0
nbr_mains_hu_BTN = 0
with open(lien_fichier,'r') as csv_file :
    csv_reader9 = csv.reader(csv_file, delimiter=',')
    for ligne in csv_reader9 :
        if (ligne[31] == '2') and (ligne[13] == '3') :
            nbr_mains_hu_BTN += 1
    
courbe_cEV_hu_BTN = np.zeros(nbr_mains_hu_BTN)
courbe_cEV_espere_hu_BTN = np.zeros(nbr_mains_hu_BTN)
mains_hu_BTN = np.arange(nbr_mains_hu_BTN)

# création du tableau de cEV pour le BTN en hu
i = 0
with open(lien_fichier,'r') as csv_file :
    csv_reader10 = csv.reader(csv_file, delimiter=',')
    for ligne in csv_reader10 :
        if i == 0 :
            i+=1
            continue
        elif i == 1 and ligne[31] == '2' and ligne[13] == '3' :
            courbe_cEV_hu_BTN[0] = float(ligne[24])/100+float(ligne[34])/100
            i+=1
        elif ligne[31] == '2' and ligne[13] == '3' :
            courbe_cEV_hu_BTN[i-1] = courbe_cEV_hu_BTN[i-2] + float(ligne[24])/100 + float(ligne[34])/100
            i+=1
            
# calcul du cEV
pourcentage_mains_hu_BTN = nbr_mains_hu_BTN/nbr_mains_tpositions
        
cEV_hu_BTN = (courbe_cEV_hu_BTN[nbr_mains_hu_BTN-1] - courbe_cEV_hu_BTN[0])/(nbr_mains_hu_BTN)*nbr_mains_par_tournois*pourcentage_mains_hu_BTN

# création du tableau de cEV pour le BTN en hu
cEV_espere_hu_BTN = 35
for j in range(nbr_mains_hu_BTN) :
    if j == 0 :
        courbe_cEV_espere_hu_BTN[0] = cEV_espere_hu_BTN/nbr_mains_par_tournois/pourcentage_mains_hu_BTN
    else :
        courbe_cEV_espere_hu_BTN[j] = courbe_cEV_espere_hu_BTN[j-1] + cEV_espere_hu_BTN/nbr_mains_par_tournois/pourcentage_mains_hu_BTN


#----------------- HU BB -----------------

# initialisation variables
nbr_mains_hu_BB = 0
c = 0
with open(lien_fichier,'r') as csv_file :
    csv_reader11 = csv.reader(csv_file, delimiter=',')
    for ligne in csv_reader11 :
        if (ligne[31] == '2') and (ligne[13] == '1') :
            nbr_mains_hu_BB += 1
            if float(ligne[15]) == day_limit and c == 0 :
                main_limite_hu = nbr_mains_hu_BB
                c = 1
    
courbe_cEV_hu_BB = np.zeros(nbr_mains_hu_BB)
courbe_cEV_espere_hu_BB = np.zeros(nbr_mains_hu_BB)
mains_hu_BB = np.arange(nbr_mains_hu_BB)

# création du tableau de cEV pour la BB en hu
i = 0
with open(lien_fichier,'r') as csv_file :
    csv_reader12 = csv.reader(csv_file, delimiter=',')
    for ligne in csv_reader12 :
        if i == 0 :
            i+=1
            continue
        elif i == 1 and ligne[31] == '2' and ligne[13] == '1' :
            courbe_cEV_hu_BB[0] = float(ligne[24])/100+float(ligne[34])/100
            i+=1
        elif ligne[31] == '2' and ligne[13] == '1' :
            courbe_cEV_hu_BB[i-1] = courbe_cEV_hu_BB[i-2] + float(ligne[24])/100 + float(ligne[34])/100
            i+=1
            
# calcul du cEV
pourcentage_mains_hu_BB = nbr_mains_hu_BB/nbr_mains_tpositions
        
cEV_hu_BB = (courbe_cEV_hu_BB[nbr_mains_hu_BB-1] - courbe_cEV_hu_BB[0])/(nbr_mains_hu_BB)*nbr_mains_par_tournois*pourcentage_mains_hu_BB

# création du tableau de cEV pour le BTN en hu
cEV_espere_hu_BB = 20
for j in range(nbr_mains_hu_BB) :
    if j == 0 :
        courbe_cEV_espere_hu_BB[0] = cEV_espere_hu_BB/nbr_mains_par_tournois/pourcentage_mains_hu_BB
    else :
        courbe_cEV_espere_hu_BB[j] = courbe_cEV_espere_hu_BB[j-1] + cEV_espere_hu_BB/nbr_mains_par_tournois/pourcentage_mains_hu_BB


#----------------- TRACÉ COURBES -----------------
        
plt.figure('toutes les positions', figsize=(13, 7))
plt.plot(mains_tpositions,courbe_cEV_espere_tpositions,'k--',label = 'cEV espéré = ' + str(cEV_espere_tpositions))
plt.plot(mains_tpositions,courbe_cEV_tpositions,'orange',label = 'cEV = ' + str(round(cEV_tpositions,1)))

if barre :
    abcisse_barre_tpositions = np.array([main_limite_tpositions,main_limite_tpositions])
    ordonnee_barre_tpositions = np.array([0,np.max(courbe_cEV_tpositions)])
    plt.plot(abcisse_barre_tpositions,ordonnee_barre_tpositions,'k')

plt.title('cEV toutes les positions')
plt.legend()

plt.figure('three way', figsize=(13, 7))

plt.plot(mains_tw_SB,courbe_cEV_espere_tw_SB,'b--',label = 'cEV espéré SB = ' + str(cEV_espere_tw_SB))
plt.plot(mains_tw_SB,courbe_cEV_tw_SB,'blue',label = 'cEV SB = ' + str(round(cEV_tw_SB,1)))

plt.plot(mains_tw_BB,courbe_cEV_espere_tw_BB,'g--',label = 'cEV espéré BB = ' + str(cEV_espere_tw_BB))
plt.plot(mains_tw_BB,courbe_cEV_tw_BB,'g',label = 'cEV BB = ' + str(round(cEV_tw_BB,1)))

plt.plot(mains_tw_BTN,courbe_cEV_espere_tw_BTN,'r--',label = 'cEV espéré BTN = ' + str(cEV_espere_tw_BTN))
plt.plot(mains_tw_BTN,courbe_cEV_tw_BTN,'r',label = 'cEV BTN = ' + str(round(cEV_tw_BTN,1)))

if barre :
    abcisse_barre_tw = np.array([main_limite_tw,main_limite_tw])
    ordonnee_barre_tw = np.array([np.min(courbe_cEV_tw_SB),np.max(courbe_cEV_tw_BTN)])
    plt.plot(abcisse_barre_tw,ordonnee_barre_tw,'k')

plt.legend()

plt.figure('HU', figsize=(13, 7))

plt.plot(mains_hu_BTN,courbe_cEV_espere_hu_BTN,'m--',label = 'cEV espéré BTN = ' + str(cEV_espere_hu_BTN))
plt.plot(mains_hu_BTN,courbe_cEV_hu_BTN,'m',label = 'cEV BTN = ' + str(round(cEV_hu_BTN,1)))

plt.plot(mains_hu_BB,courbe_cEV_espere_hu_BB,'y--',label = 'cEV espéré BB = ' + str(cEV_espere_hu_BB))
plt.plot(mains_hu_BB,courbe_cEV_hu_BB,'y',label = 'cEV BB = ' + str(round(cEV_hu_BB,1)))

if barre :
    abcisse_barre_hu = np.array([main_limite_hu,main_limite_hu])
    ordonnee_barre_hu = np.array([np.min(courbe_cEV_hu_BB),np.max(courbe_cEV_hu_BTN)])
    plt.plot(abcisse_barre_hu,ordonnee_barre_hu,'k')

plt.legend()
plt.show()















