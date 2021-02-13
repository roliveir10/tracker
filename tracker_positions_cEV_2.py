# importation des librairies
import numpy as np
import csv
import sys
from matplotlib import pyplot as plt

# entrées utilisateur
if len(sys.argv)==1 :
    print ("Vous devez spécifier le chemin du fichier en argument")
    quit()

lien_fichier=sys.argv[1]

# données par défaut
cEV_esp_tpositions=85
cEV_esp_tway_SB=0
cEV_esp_tway_BB=0
cEV_esp_tway_BTN=30
cEV_esp_HU_BB=20
cEV_esp_HU_BTN=35

# premier parcours du fichier csv
liste_dayID=[]
date=[]
liste_date=[]
liste_ID_tournois=[]
liste_EVdiff_tpositions=[]
liste_EVdiff_tway_SB=[]
liste_EVdiff_tway_BB=[]
liste_EVdiff_tway_BTN=[]
liste_EVdiff_HU_BB=[]
liste_EVdiff_HU_BTN=[]
dayID_barre=0
main_limite_tpositions=0
main_limite_tway=0
main_limite_HU=0

except_line1 = 1
with open(lien_fichier,'r') as csv_file :
    csv_reader = csv.reader(csv_file, delimiter=',')
    for ligne in csv_reader :
        if except_line1==1 :
            except_line1=0
            continue
        liste_ID_tournois.append(ligne[7])
        date=ligne[22]
        liste_date.append(date[0:10])
        liste_dayID.append(int(ligne[15]))

# entrées utilisateur suite
givedate=False
givedate_entered=False
dayID_entered=0
barre=False
if len(sys.argv)>2 :
    if len(sys.argv)==3 and sys.argv[2]=='givedate' :
        givedate=True
    elif len(sys.argv)==4 and sys.argv[2]=='givedate' :
        if int(sys.argv[3]) not in liste_dayID :
            print("Le dayID entré ne correspond à aucune date")
            quit()
        else :
            dayID_entered=int(sys.argv[3])
            givedate_entered=True
    else :
        if int(sys.argv[2]) not in liste_dayID :
            print("Le dayID entré ne correspond à aucune date")
            quit()
        else :
            dayID_barre=int(sys.argv[2])
            barre=True
            day_trouve=False

if givedate :
    print('La première main à été faite le '+str(liste_date[0])+' et correspond au DayID '+str(liste_dayID[0])
    +' et la dernière main a été faite le '+str(liste_date[-1])+' et correspond au DayID '+str(liste_dayID[-1]))
    quit()
if givedate_entered :
    dateposition=0
    for i in range(len(liste_dayID)) :
        if int(liste_dayID[i])==dayID_entered :
            dateposition=i
    print('Le DayID spécifié correspond à jour suivant : '+liste_date[dateposition])
    quit()

# second parcours du fichier csv
except_line1 = 1
with open(lien_fichier,'r') as csv_file :
    csv_reader2 = csv.reader(csv_file, delimiter=',')
    for ligne in csv_reader2 :
        if except_line1==1 :
            except_line1=0
            continue
        liste_EVdiff_tpositions.append(float(ligne[24])/100+float(ligne[34])/100)
        if ligne[31] == '3' and ligne[13] == '2' :
            liste_EVdiff_tway_SB.append(float(ligne[24])/100+float(ligne[34])/100)
        elif ligne[31] == '3' and ligne[13] == '1' :
            liste_EVdiff_tway_BB.append(float(ligne[24])/100+float(ligne[34])/100)
        elif ligne[31] == '3' and ligne[13] == '3' :
            liste_EVdiff_tway_BTN.append(float(ligne[24])/100+float(ligne[34])/100)
        elif ligne[31] == '2' and ligne[13] == '1' :
            liste_EVdiff_HU_BB.append(float(ligne[24])/100+float(ligne[34])/100)
        elif ligne[31] == '2' and ligne[13] == '3' :
            liste_EVdiff_HU_BTN.append(float(ligne[24])/100+float(ligne[34])/100)
        if barre and not day_trouve:
            if dayID_barre==int(ligne[15]) :
                main_limite_tpositions=len(liste_EVdiff_tpositions)
                main_limite_tway=len(liste_EVdiff_tway_SB)
                main_limite_HU=len(liste_EVdiff_HU_BB)
                day_trouve=True

# création des tableaux de cEV
nbr_mains_tpositions=len(liste_EVdiff_tpositions)
nbr_mains_tway_SB=len(liste_EVdiff_tway_SB)
nbr_mains_tway_BB=len(liste_EVdiff_tway_BB)
nbr_mains_tway_BTN=len(liste_EVdiff_tway_BTN)
nbr_mains_HU_BB=len(liste_EVdiff_HU_BB)
nbr_mains_HU_BTN=len(liste_EVdiff_HU_BTN)

tab_mains_tpositions=np.arange(nbr_mains_tpositions)
tab_mains_tway_SB=np.arange(nbr_mains_tway_SB)
tab_mains_tway_BB=np.arange(nbr_mains_tway_BB)
tab_mains_tway_BTN=np.arange(nbr_mains_tway_BTN)
tab_mains_HU_BB=np.arange(nbr_mains_HU_BB)
tab_mains_HU_BTN=np.arange(nbr_mains_HU_BTN)   

tab_cEV_tpositions=np.zeros(nbr_mains_tpositions)
tab_cEV_tway_SB=np.zeros(nbr_mains_tway_SB)
tab_cEV_tway_BB=np.zeros(nbr_mains_tway_BB)
tab_cEV_tway_BTN=np.zeros(nbr_mains_tway_BTN)
tab_cEV_HU_BB=np.zeros(nbr_mains_HU_BB)
tab_cEV_HU_BTN=np.zeros(nbr_mains_HU_BTN)

c=0
for EVdiff in liste_EVdiff_tpositions :
    if c==0 :
        tab_cEV_tpositions[0]=EVdiff
    else :
        tab_cEV_tpositions[c]=tab_cEV_tpositions[c-1]+EVdiff
    c+=1

c=0
for EVdiff in liste_EVdiff_tway_SB :
    if c==0 :
        tab_cEV_tway_SB[0]=EVdiff
    else :
        tab_cEV_tway_SB[c]=tab_cEV_tway_SB[c-1]+EVdiff
    c+=1

c=0
for EVdiff in liste_EVdiff_tway_BB :
    if c==0 :
        tab_cEV_tway_BB[0]=EVdiff
    else :
        tab_cEV_tway_BB[c]=tab_cEV_tway_BB[c-1]+EVdiff
    c+=1

c=0
for EVdiff in liste_EVdiff_tway_BTN :
    if c==0 :
        tab_cEV_tway_BTN[0]=EVdiff
    else :
        tab_cEV_tway_BTN[c]=tab_cEV_tway_BTN[c-1]+EVdiff
    c+=1

c=0
for EVdiff in liste_EVdiff_HU_BB :
    if c==0 :
        tab_cEV_HU_BB[0]=EVdiff
    else :
        tab_cEV_HU_BB[c]=tab_cEV_HU_BB[c-1]+EVdiff
    c+=1

c=0
for EVdiff in liste_EVdiff_HU_BTN :
    if c==0 :
        tab_cEV_HU_BTN[0]=EVdiff
    else :
        tab_cEV_HU_BTN[c]=tab_cEV_HU_BTN[c-1]+EVdiff
    c+=1

# calcul des cEV
# avant : calcul du nombre de mains par tournois
nbr_tournois=len(list(set(liste_ID_tournois)))
nbr_mains_par_tournois=nbr_mains_tpositions/nbr_tournois
pourcentage_mains_tway_SB=nbr_mains_tway_SB/nbr_mains_tpositions
pourcentage_mains_tway_BB=nbr_mains_tway_BB/nbr_mains_tpositions
pourcentage_mains_tway_BTN=nbr_mains_tway_BTN/nbr_mains_tpositions
pourcentage_mains_HU_BB=nbr_mains_HU_BB/nbr_mains_tpositions
pourcentage_mains_HU_BTN=nbr_mains_HU_BTN/nbr_mains_tpositions

cEV_tpositions=(tab_cEV_tpositions[-1]-tab_cEV_tpositions[0])/(nbr_mains_tpositions/nbr_mains_par_tournois)
cEV_tway_SB=(tab_cEV_tway_SB[-1]-tab_cEV_tway_SB[0])/nbr_mains_tway_SB*nbr_mains_par_tournois*pourcentage_mains_tway_SB
cEV_tway_BB=(tab_cEV_tway_BB[-1]-tab_cEV_tway_BB[0])/nbr_mains_tway_BB*nbr_mains_par_tournois*pourcentage_mains_tway_BB
cEV_tway_BTN=(tab_cEV_tway_BTN[-1]-tab_cEV_tway_BTN[0])/nbr_mains_tway_BTN*nbr_mains_par_tournois*pourcentage_mains_tway_BTN
cEV_HU_BB=(tab_cEV_HU_BB[-1]-tab_cEV_HU_BB[0])/nbr_mains_HU_BB*nbr_mains_par_tournois*pourcentage_mains_HU_BB
cEV_HU_BTN=(tab_cEV_HU_BTN[-1]-tab_cEV_HU_BTN[0])/nbr_mains_HU_BTN*nbr_mains_par_tournois*pourcentage_mains_HU_BTN

# création des tableaux de cEV espérés
tab_cEV_esp_tpositions=np.zeros(nbr_mains_tpositions)
tab_cEV_esp_tway_SB=np.zeros(nbr_mains_tway_SB)
tab_cEV_esp_tway_BB=np.zeros(nbr_mains_tway_BB)
tab_cEV_esp_tway_BTN=np.zeros(nbr_mains_tway_BTN)
tab_cEV_esp_HU_BB=np.zeros(nbr_mains_HU_BB)
tab_cEV_esp_HU_BTN=np.zeros(nbr_mains_HU_BTN)

for i in range(nbr_mains_tpositions) :
    if i==0 :
        tab_cEV_esp_tpositions[0]=cEV_esp_tpositions/nbr_mains_par_tournois
    else :
        tab_cEV_esp_tpositions[i]=tab_cEV_esp_tpositions[i-1]+cEV_esp_tpositions/nbr_mains_par_tournois

for i in range(nbr_mains_tway_SB) :
    if i==0 :
        tab_cEV_esp_tway_SB[0]=cEV_esp_tway_SB/nbr_mains_par_tournois/pourcentage_mains_tway_SB
    else :
        tab_cEV_esp_tway_SB[i]=tab_cEV_esp_tway_SB[i-1]+cEV_esp_tway_SB/nbr_mains_par_tournois/pourcentage_mains_tway_SB

for i in range(nbr_mains_tway_BB) :
    if i==0 :
        tab_cEV_esp_tway_BB[0]=cEV_esp_tway_BB/nbr_mains_par_tournois/pourcentage_mains_tway_BB
    else :
        tab_cEV_esp_tway_BB[i]=tab_cEV_esp_tway_BB[i-1]+cEV_esp_tway_BB/nbr_mains_par_tournois/pourcentage_mains_tway_BB

for i in range(nbr_mains_tway_BTN) :
    if i==0 :
        tab_cEV_esp_tway_BTN[0]=cEV_esp_tway_BTN/nbr_mains_par_tournois/pourcentage_mains_tway_BTN
    else :
        tab_cEV_esp_tway_BTN[i]=tab_cEV_esp_tway_BTN[i-1]+cEV_esp_tway_BTN/nbr_mains_par_tournois/pourcentage_mains_tway_BTN

for i in range(nbr_mains_HU_BB) :
    if i==0 :
        tab_cEV_esp_HU_BB[0]=cEV_esp_HU_BB/nbr_mains_par_tournois/pourcentage_mains_HU_BB
    else :
        tab_cEV_esp_HU_BB[i]=tab_cEV_esp_HU_BB[i-1]+cEV_esp_HU_BB/nbr_mains_par_tournois/pourcentage_mains_HU_BB

for i in range(nbr_mains_HU_BTN) :
    if i==0 :
        tab_cEV_esp_HU_BTN[0]=cEV_esp_HU_BTN/nbr_mains_par_tournois/pourcentage_mains_HU_BTN
    else :
        tab_cEV_esp_HU_BTN[i]=tab_cEV_esp_HU_BTN[i-1]+cEV_esp_HU_BTN/nbr_mains_par_tournois/pourcentage_mains_HU_BTN

# tracé barre




# tracé des courbes
plt.figure('Toutes les positions', figsize=(13, 7))
plt.plot(tab_mains_tpositions,tab_cEV_esp_tpositions,'--',color='orange',label='cEV espéré = '+str(cEV_esp_tpositions))
plt.plot(tab_mains_tpositions,tab_cEV_tpositions,'orange',label='cEV = '+str(round(cEV_tpositions)))

if barre :
    abcisse_barre_tpositions = np.array([main_limite_tpositions,main_limite_tpositions])
    ordonnee_barre_tpositions = np.array([np.min(tab_cEV_tpositions),max(np.max(tab_cEV_tpositions),np.max(tab_cEV_esp_tpositions))])
    plt.plot(abcisse_barre_tpositions,ordonnee_barre_tpositions,'k')

plt.legend()

plt.figure('Three way', figsize=(13, 7))
plt.plot(tab_mains_tway_BTN,tab_cEV_esp_tway_BTN,'r--',label='cEV espéré BTN = '+str(cEV_esp_tway_BTN))
plt.plot(tab_mains_tway_BTN,tab_cEV_tway_BTN,'r',label='cEV BTN = '+str(round(cEV_tway_BTN)))

plt.plot(tab_mains_tway_BB,tab_cEV_esp_tway_BB,'g--',label='cEV espéré BB = '+str(cEV_esp_tway_BB))
plt.plot(tab_mains_tway_BB,tab_cEV_tway_BB,'g',label='cEV BB = '+str(round(cEV_tway_BB)))

plt.plot(tab_mains_tway_SB,tab_cEV_esp_tway_SB,'b--',label='cEV espéré SB = '+str(cEV_esp_tway_SB))
plt.plot(tab_mains_tway_SB,tab_cEV_tway_SB,'blue',label='cEV SB = '+str(round(cEV_tway_SB)))

if barre :
    abcisse_barre_tway = np.array([main_limite_tway,main_limite_tway])
    ordonnee_barre_tway = np.array([min(np.min(tab_cEV_tway_SB),np.min(tab_cEV_tway_BB)),max(np.max(tab_cEV_tway_BTN),np.max(tab_cEV_esp_tway_BTN))])
    plt.plot(abcisse_barre_tway,ordonnee_barre_tway,'k')

plt.legend()

plt.figure('Heads Up', figsize=(13, 7))
plt.plot(tab_mains_HU_BTN,tab_cEV_esp_HU_BTN,'m--',label='cEV espéré BTN = '+str(cEV_esp_HU_BTN))
plt.plot(tab_mains_HU_BTN,tab_cEV_HU_BTN,'m',label='cEV BTN = '+str(round(cEV_HU_BTN)))

plt.plot(tab_mains_HU_BB,tab_cEV_esp_HU_BB,'y--',label='cEV espéré BB = '+str(cEV_esp_HU_BB))
plt.plot(tab_mains_HU_BB,tab_cEV_HU_BB,'y',label='cEV SB = '+str(round(cEV_HU_BB)))

if barre :
    abcisse_barre_HU = np.array([main_limite_HU,main_limite_HU])
    ordonnee_barre_HU = np.array([min(np.min(tab_cEV_HU_BB),np.min(tab_cEV_HU_BTN)),max(max(np.max(tab_cEV_HU_BTN),np.max(tab_cEV_HU_BB)),
    max(np.max(tab_cEV_esp_HU_BB),np.max(tab_cEV_esp_HU_BTN)))])
    plt.plot(abcisse_barre_HU,ordonnee_barre_HU,'k')

plt.legend()

plt.show()
