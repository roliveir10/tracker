# importation des librairies
import numpy as np
import csv
import sys
from matplotlib import pyplot as plt
from numpy.core.fromnumeric import size

# entrées utilisateur
if len(sys.argv)==1 :
    print ("Vous devez spécifier le chemin du fichier en argument")
    quit()

lien_fichier=sys.argv[1]

# définition clés
def tournamentID (M) :
    return int(M[2])

# coefficient multiplicateur blindes

def coefmultiplicateur (level) :
    if level==1 :
        return 1
    elif level==2 :
        return 2/3
    elif level==3 :
        return 3/4
    elif level==4 :
        return 4/6
    elif level==5 :
        return 6/8
    elif level==6 :
        return 8/10
    elif level==64 :
        return 8/10
    elif level==38 :
        return 8/10
    elif level==7 :
        return 10/12
    else :
        print('niveau de blindes inconnu')
        quit()

# calcul stack vilain

def stackVilain (main) :
    if int(main[1])==1 : nbr_total_blindes=75
    elif int(main[1])==2 : nbr_total_blindes=50
    elif int(main[1])==3 : nbr_total_blindes=37.5
    elif int(main[1])==4 : nbr_total_blindes=25
    elif int(main[1])==5 : nbr_total_blindes=18.75
    elif int(main[1])==6 or int(main[1])==64 or int(main[1])==38 : nbr_total_blindes=15
    elif int(main[1])==7 : nbr_total_blindes=12.5
    else : 
        print('niveau de blindes inconnu')
        quit()
    return nbr_total_blindes-main[-1]

# premier parcours du fichier csv

liste_dayID=[]
liste_date=[]

except_line1 = True
with open(lien_fichier,'r') as csv_file :
    csv_reader = csv.reader(csv_file, delimiter=',')
    for ligne in csv_reader :
        if except_line1 :
            except_line1=False
            continue
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


# deuxième parcours fichier csv
parser=[]
except_line1 = True

with open(lien_fichier,'r') as csv_file :
    csv_reader2 = csv.reader(csv_file, delimiter=',')
    for ligne in csv_reader2 :
        if except_line1 :
            except_line1=False
            continue
        parser.append([ligne[0],ligne[6],ligne[7],ligne[13],ligne[24],ligne[27],ligne[31],ligne[34],ligne[15]])

parser_tri_tournois=sorted(parser,key=tournamentID)
nbr_mains=len(parser_tri_tournois)


# on classe les mains par tournois
liste_tournois_mains=[]
liste_tournois_temporaire=[]
premiere_main=True

for i in range(len(parser_tri_tournois)) :
    if premiere_main :
        liste_tournois_temporaire.append(parser_tri_tournois[0])
        premiere_main=False
    else :
        if parser_tri_tournois[i][2]==parser_tri_tournois[i-1][2] :
            liste_tournois_temporaire.append(parser_tri_tournois[i])
        else :
            liste_tournois_mains.append(liste_tournois_temporaire)
            liste_tournois_temporaire=[]
            liste_tournois_temporaire.append(parser_tri_tournois[i])

liste_tournois_mains.append(liste_tournois_temporaire)

stack = 25
premiere_main_tournois=True
for numerotournois in range(len(liste_tournois_mains)) :
    for numeromain in range (len(liste_tournois_mains[numerotournois])) :
        if premiere_main_tournois :
            liste_tournois_mains[numerotournois][numeromain].append(stack)
            premiere_main_tournois=False
        else :
            stack+=float(liste_tournois_mains[numerotournois][numeromain-1][5])
            if liste_tournois_mains[numerotournois][numeromain][1]!=liste_tournois_mains[numerotournois][numeromain-1][1] :
                stack*=coefmultiplicateur(int(liste_tournois_mains[numerotournois][numeromain][1]))
            liste_tournois_mains[numerotournois][numeromain].append(stack)
    stack=25
    premiere_main_tournois=True


# catégorisation des mains
def stackEffectif (main) :
    return (min(main[-1],stackVilain(main)))

def domination (main) :
    if int(main[1])==1 : 
        if main[-1] > 45 :
            return('HD')
        elif main[-1] <= 45 and main[-1] >= 30 :
            return('EQ')
        else :
            return('VD')
    elif int(main[1])==2 :
        if main[-1] > 30 :
            return('HD')
        elif main[-1] <= 30 and main[-1] >= 20 :
            return('EQ')
        else :
            return('VD')
    elif int(main[1])==3 : 
        if main[-1] > 22.5 :
            return('HD')
        elif main[-1] <= 22.5 and main[-1] >= 15 :
            return('EQ')
        else :
            return('VD')
    elif int(main[1])==4 :
        if main[-1] > 14 :
            return('HD')
        elif main[-1] <= 14 and main[-1] >= 11 :
            return('EQ')
        else :
            return('VD')
    elif int(main[1])==5 :
        if main[-1] > 10.3 :
            return('HD')
        elif main[-1] <= 10.3 and main[-1] >= 8.45 :
            return('EQ')
        else :
            return('VD')
    elif int(main[1])==6 or int(main[1])==64 or int(main[1])==38:
        if main[-1] > 8.25 :
            return('HD')
        elif main[-1] <= 8.25 and main[-1] >= 6.75 :
            return('EQ')
        else :
            return('VD')
    elif int(main[1])==7 :
        if main[-1] > 6.75 :
            return('HD')
        elif main[-1] <= 6.75 and main[-1] >= 5.75 :
            return('EQ')
        else :
            return('VD')
    else : 
        print('niveau de blindes inconnu')
        quit()

def categorie (main) :
    if stackEffectif(main)<10 :
        if int(main[1]) in [1,2,3] and domination(main)=='HD' :
            return (1)
        elif int(main[1]) in [4,5,6,64,7] and domination(main)=='HD' :
            return (2) 
        elif int(main[1]) in [5,6,64,7] and domination(main)=='EQ' :
            return (3)
        elif int(main[1]) in [1,2,3] and domination(main)=='VD' :
            return (4)
        else :
            return(5)
    if stackEffectif(main)<=20 and stackEffectif(main)>=10 :
        if int(main[1]) in [1,2] and domination(main)=='HD' :
            return (6)
        elif int(main[1]) in [3,4] and domination(main)=='HD' :
            return (7) 
        elif int(main[1]) in [3,4] and domination(main)=='EQ' :
            return (8)
        elif int(main[1])==5 and domination(main)=='EQ' :
            return (3)
        elif int(main[1]) in [1,2] and domination(main)=='VD' :
            return (9)
        else :
            return(10)
    if stackEffectif(main)>20 :
        if int(main[1])==1 and domination(main)=='HD' :
            return (11)
        elif int(main[1]) in [1,2,3] and domination(main)=='EQ' :
            return (12) 
        else :
            return(13)

'''
Test de catégorisation :

for tournois in liste_tournois_mains :
    for main in tournois :
        if int(main[0]) in [32235,32234,32233,32231,32222,32216,32193,32171,32174,32055,31965,31944,31827,31700,31673,31449,31440] :
            print(main[0]+'  '+str(categorie(main)))

doit renvoyer :

31440  11
31449  1
31700  7
31673  9
31827  12
31944  6
31965  13
32055  4
32174  10
32216  2
32171  8
32193  10
32222  5
32231  2
32233  5
32234  5
32235  3

'''
# on cherche ou placer la barre
if barre :
    position_barre_10_HD=0
    position_barre_10_HD_trouve=False
    compteur_barre_10_HD=0

    position_barre_10_EQ=0
    position_barre_10_EQ_trouve=False
    compteur_barre_10_EQ=0

    position_barre_10_VD=0
    position_barre_10_VD_trouve=False
    compteur_barre_10_VD=0

    position_barre_1020_HD=0
    position_barre_1020_HD_trouve=False
    compteur_barre_1020_HD=0

    position_barre_1020_EQ=0
    position_barre_1020_EQ_trouve=False
    compteur_barre_1020_EQ=0

    position_barre_1020_VD=0
    position_barre_1020_VD_trouve=False
    compteur_barre_1020_VD=0

    position_barre_20_HD=0
    position_barre_20_HD_trouve=False
    compteur_barre_20_HD=0

    position_barre_20_EQ=0
    position_barre_20_EQ_trouve=False
    compteur_barre_20_EQ=0

    position_barre_20_VD=0
    position_barre_20_VD_trouve=False
    compteur_barre_20_VD=0

    for tournois in liste_tournois_mains :
        for main in tournois :
            if int(main[6])==3 :
                continue
            if categorie(main) in [1,2] : 
                compteur_barre_10_HD+=1
            elif categorie(main)==3 :
                compteur_barre_10_EQ+=1
            elif categorie(main) in [4,5] :
                compteur_barre_10_VD+=1
            elif categorie(main) in [6,7] :
                compteur_barre_1020_HD+=1
            elif categorie(main)==8 :
                compteur_barre_1020_EQ+=1
            elif categorie(main) in [9,10] :
                compteur_barre_1020_VD+=1
            elif categorie(main)==11 :
                compteur_barre_20_HD+=1
            elif categorie(main)==12 :
                compteur_barre_20_EQ+=1
            elif categorie(main)==13 :
                compteur_barre_20_VD+=1

            if int(main[-2])==dayID_barre :
                if categorie(main) in [1,2] and not position_barre_10_HD_trouve : 
                    position_barre_10_HD=compteur_barre_10_HD
                    position_barre_10_HD_trouve=True
                elif categorie(main)==3 and not position_barre_10_EQ_trouve :
                    position_barre_10_EQ=compteur_barre_10_EQ
                    position_barre_10_EQ_trouve=True
                elif categorie(main) in [4,5] and not position_barre_10_VD_trouve :
                    position_barre_10_VD=compteur_barre_10_VD
                    position_barre_10_VD_trouve=True
                elif categorie(main) in [6,7] and not position_barre_1020_HD_trouve :
                    position_barre_1020_HD=compteur_barre_1020_HD
                    position_barre_1020_HD_trouve=True
                elif categorie(main)==8 and not position_barre_1020_EQ_trouve :
                    position_barre_1020_EQ=compteur_barre_1020_EQ
                    position_barre_1020_EQ_trouve=True
                elif categorie(main) in [9,10] and not position_barre_1020_VD_trouve :
                    position_barre_1020_VD=compteur_barre_1020_VD
                    position_barre_1020_VD_trouve=True
                elif categorie(main)==11 and not position_barre_20_HD_trouve :
                    position_barre_20_HD=compteur_barre_20_HD
                    position_barre_20_HD_trouve=True
                elif categorie(main)==12 and not position_barre_20_EQ_trouve :
                    position_barre_20_EQ=compteur_barre_20_EQ
                    position_barre_20_EQ_trouve=True
                elif categorie(main)==13 and not position_barre_20_VD_trouve :
                    position_barre_20_VD=compteur_barre_20_VD
                    position_barre_20_VD_trouve=True


# création du tableau d’EV pour les mains d’une certaine catégorie

def tableaux_EV_categorie (L_tournois_mains,L_categories) :
    premier_passage = True
    liste_EV = []
    for tournois in L_tournois_mains :
        for main in tournois :
            if categorie(main) in L_categories and int(main[6])==2 :
                if premier_passage :
                    liste_EV.append(int(main[4])/100+int(main[7])/100)
                    premier_passage=False
                else :
                    liste_EV.append(liste_EV[-1]+int(main[4])/100+int(main[7])/100)
    return(np.asarray(liste_EV))

# calcul des tableaux d’EV
tab_EV_10_HD = tableaux_EV_categorie(liste_tournois_mains,[1,2])
tab_EV_10_EQ = tableaux_EV_categorie(liste_tournois_mains,[3])
tab_EV_10_VD = tableaux_EV_categorie(liste_tournois_mains,[4,5])

tab_EV_1020_HD = tableaux_EV_categorie(liste_tournois_mains,[6,7])
tab_EV_1020_EQ = tableaux_EV_categorie(liste_tournois_mains,[8])
tab_EV_1020_VD = tableaux_EV_categorie(liste_tournois_mains,[9,10])

tab_EV_20_HD = tableaux_EV_categorie(liste_tournois_mains,[11])
tab_EV_20_EQ = tableaux_EV_categorie(liste_tournois_mains,[12])
tab_EV_20_VD = tableaux_EV_categorie(liste_tournois_mains,[13])

# calcul du cEV d’un tableau 
def cEV_tab (L_tournois_mains,tab) :
    return ((tab[-1]-tab[0])/len(L_tournois_mains))

# fonction affichage courbe
def affichage(tab_EV,L_tournois_mains,debut_legende,couleur) :
    taby=tab_EV
    tabx = np.arange(np.size(taby))
    plt.plot(tabx,taby,label=debut_legende+str(round(cEV_tab(L_tournois_mains,taby),1)),color=couleur)

# fonction tracé barre 
def trace_barre (position,couleur,graph) :
    abcisse_barre = np.array([position,position])
    if graph==1 :
        ordonnee_barre = ordonnee_barre = np.array([min([np.min(tab_EV_10_HD),np.min(tab_EV_10_EQ),np.min(tab_EV_10_VD)]),
        max([np.max(tab_EV_10_HD),np.max(tab_EV_10_EQ),np.max(tab_EV_10_VD)])])
    if graph==2 :
        ordonnee_barre = np.array([min([np.min(tab_EV_1020_HD),np.min(tab_EV_1020_EQ),np.min(tab_EV_1020_VD)]),
        max([np.max(tab_EV_1020_HD),np.max(tab_EV_1020_EQ),np.max(tab_EV_1020_VD)])])
    if graph==3 :
        ordonnee_barre = np.array([min([np.min(tab_EV_20_HD),np.min(tab_EV_20_EQ),np.min(tab_EV_20_VD)]),
        max([np.max(tab_EV_20_HD),np.max(tab_EV_20_EQ),np.max(tab_EV_20_VD)])])
    plt.plot(abcisse_barre,ordonnee_barre,color=couleur)


# tracé courbes

plt.figure('stack effectif < 10 BB', figsize=(13, 7))
affichage(tab_EV_10_HD,liste_tournois_mains,'le cEV quand hero domine vilain est de ','b')
affichage(tab_EV_10_EQ,liste_tournois_mains,'le cEV quand les stacks sont équilibrés ','g')
affichage(tab_EV_10_VD,liste_tournois_mains,'le cEV quand vilain domine hero est de ','r')

if barre :
    trace_barre(position_barre_10_HD,'b',1)
    trace_barre(position_barre_10_EQ,'g',1)
    trace_barre(position_barre_10_VD,'r',1)

plt.legend()

plt.figure('stack effectif entre 10 et 20 BB', figsize=(13, 7))
affichage(tab_EV_1020_HD,liste_tournois_mains,'le cEV quand hero domine vilain est de ','b')
affichage(tab_EV_1020_EQ,liste_tournois_mains,'le cEV quand les stacks sont équilibrés ','g')
affichage(tab_EV_1020_VD,liste_tournois_mains,'le cEV quand vilain domine hero est de ','r')

if barre :
    trace_barre(position_barre_1020_HD,'b',2)
    trace_barre(position_barre_1020_EQ,'g',2)
    trace_barre(position_barre_1020_VD,'r',2)

plt.legend()

plt.figure('stack effectif > 20 BB', figsize=(13, 7))
affichage(tab_EV_20_HD,liste_tournois_mains,'le cEV quand hero domine vilain est de ','b')
affichage(tab_EV_20_EQ,liste_tournois_mains,'le cEV quand les stacks sont équilibrés ','g')
affichage(tab_EV_20_VD,liste_tournois_mains,'le cEV quand vilain domine hero est de ','r')

if barre :
    trace_barre(position_barre_20_HD,'b',3)
    trace_barre(position_barre_20_EQ,'g',3)
    trace_barre(position_barre_20_VD,'r',3)
 
plt.legend()

plt.show()




