import csv
from Graphes import*


class UniteError(Exception):
    pass

def from_csv(nom_fichier_csv: str)->list:
    """Ouvre un fichier csv et le traduit en liste imbriquée.
    Le fichier est découpé en lignes, et chaque ligne est une liste, contenants ses mots."

    Args:
        nom_fichier_csv (str): nom du fichier à utiliser

    Returns:
        list
    """
    with open(nom_fichier_csv + ".csv" , 'r', encoding="utf−8" ) as fichier_csv:
        lecture_fichier_csv =csv.reader(fichier_csv, delimiter= "," ,quoting=csv.QUOTE_ALL)
        l=[]
        for r in lecture_fichier_csv:
            l.append(r)
        return l

def conversion_unite(duree_tache):
    """Convertit toutes les unités de temps en jours. On suppose 1 mois=30 jours.

    Args:
        duree_tache (str): la duree avec les unités (jours/mois/annee/semaine)

    Returns:
        int: la durée en jours.
    """
    valeur=float(duree_tache.split()[0]) #La valeur est le premier terme de la duree 
    unite=duree_tache.split()[1] #L'unité est le second terme de la duree 
    if unite=='mois': #Si l'unité est en mois
        valeur*=30 #Alors on multiplie par 30 la valeur car il y a 30 jour dans un mois 
    elif unite=='annees' or unite=='annee':  #Si l'unité est en annee
        valeur*=365 #Alors on multiplie par 365 la valeur car il y a 365 jours dans un mois 
    elif unite=='semaines' or unite=='semaine': #Si l'unité est en semaine
        valeur*=7  #Alors on multiplie par 7 la valeur car il y a 7 jours dans un mois 
    elif unite=='jours' or unite=='jour': #Si l'unite est en jour
        valeur=valeur #Alors on ne change rien
    else: #Sinon 
        raise UniteError #On soulève une erreur d'unite
    return valeur

def traitement_information(liste_informations, n_suivi)->tuple[list,set,list]:
    """Traite l'information d'une liste (output de from_csv). Renvoie les noeuds,arcs et poids des noeuds

    Args:
        liste_informations (list): la liste des lignes d'un fichier csv

    Returns:
        tuple: 
            list: la liste des différents noeuds du graphes 
            set: l'ensemble des arcs du graphe
            list: la liste des poids de chaque noeud
                tuple: 
                    str: le nom du noeud
                    int: son poids
    """
    noeuds=[] #La liste des noeuds
    poids=[] #La liste des poids
    arcs=set() #L'ensemble des arcs
    #Vérifions tout d'abord si le suivi est vide.
    if len([1 for ligne in liste_informations if ligne[3+n_suivi]!=''])==0:
        #Si tel est le cas, on renvoie None pour touts les éléments du graphe (on ne traite pas le suivi)
        return None, None, None, None
    for ligne in liste_informations: #Pour chaque ligne, donc chaque tâche, donc chaque noeud
        noeud=ligne[0] #On rajoute le noeud à la liste
        noeuds.append(noeud)
        
        #On extrait la durée de la tâche
        if ligne[3+n_suivi]=='': #Si la tâche est terminée
            duree_tache="0 jours"
        else: #Si la tâche n'est pas terminée
            duree_tache=ligne[3+n_suivi]
            
        duree_tache=conversion_unite(duree_tache) #On convertit la duree qui était une valeur suivi d'une unité temporelle en nombre de jour
        poids.append((noeud,duree_tache)) #On associe le noeud à son poids et on le rajoute dans la liste des poids
        if ligne[3]!='': #Si la tache à un prérequis
            pre_noeuds=ligne[3] #La liste des prerequis
            for pre_noeud in pre_noeuds.split(): #Pour chaque prérequis
                arcs.add((pre_noeud, noeud)) #On ajoute l'arc prerequis -> noeud
    poids_final=poids[-1][1]
        
    return noeuds, arcs, poids, poids_final



def ponderation_branches(arcs, poids)->set:
    """Pour réaliser un graphe à partir de l'output de traitement_information, associe chaque
    voisin d'un noeud donné par un arc du poids du noeud donné. 

    Args:
        arcs (set): l'ensemble des branches
        poids (_type_): l'ensemble des poids
    
    Returns:
        set: l'ensemble des arcs ponderés
    """
    arcs_ponderes=set() #L'ensemble des arcs ponderees
    for arc in arcs: #Pour chaque arcs
        pre_noeud=arc[0] #Le noeud iitial de l'arc
        for p in poids: #Pour chaque poids
            if pre_noeud==p[0]: #Si le noeud initial de l'arc est le meme que ce noeud ponderee
                poids_arc=p[1] #Alors le poids de de cet arc est egal au poids du noeud initial
        arcs_ponderes.add((arc[0], arc[1], poids_arc)) #On rajoute au set des arcs ponderés l'arc avec son poids 
    return arcs_ponderes

def csv_to_graph(nom_fichier_csv:str):
    """A partir d'un nom de fichier csv, renvoie les ensembles de définitions des graphes de tâches
    associés à l'analyse initiale, et chaque compte rendu d'éxécution du fichier.

    Args:
        nom_fichier_csv (str): Nom du fichier csv à convertir

    Returns:
        list: Liste imbriquées des ensembles de définitions des graphes de chaque compte rendu d'éxécution du fichier.
            tuple:
                list: la liste des noeuds
                set: l'ensemble des arcs pondérés
                int: le poids final de la tâche qui n'est donc sur aucun arc
    """
    graphs=[] #La liste des graphes
    liste_csv=from_csv(nom_fichier_csv) #On convertit le fichier en liste
    liste_csv.pop(0) #On enlève le premier terme de la liste qui correspond au indication sur le fichier
    
    #Les colonnes suivis sont les colonnes 3, puis 5,6,...
    indices_colonnes_suivis=list(range(len(liste_csv[0])-3))
    indices_colonnes_suivis[0]=-1
    
    for n_suivi in indices_colonnes_suivis: #On extrait les informations de tout les suivis disponibles.
        noeuds, arcs, poids, poids_final= traitement_information(liste_csv,n_suivi) #On récupère les différentes informations
        if noeuds==None:
            continue
        arcs_ponderee=ponderation_branches(arcs, poids) #On crée les arcs ponderes à partir des arcs et des poids
        graphs.append((noeuds,arcs_ponderee, poids_final))  #On crée un tuple aves toutes les informations necessaires à créer un graphe ponderé. 
    return graphs