import csv
from Graphes import*


class UniteError(Exception):
    pass

def from_csv(nom_fichier_csv: str)->list:
    """Programme qui ouvre un fichier csv et qui le tranforme en liste de liste de mot

    Args:
        nom_fichier_csv (str): Nom du fichier à utiliser

    Returns:
        list: Liste ou chaque terme est une liste qui correspond à une ligne et chaque terme de cette liste est un mot de la ligne
    """
    with open(nom_fichier_csv + ".csv" , 'r', encoding="utf−8" ) as fichier_csv:
        lecture_fichier_csv =csv.reader(fichier_csv, delimiter= "," ,quoting=csv.QUOTE_ALL)
        l=[]
        for r in lecture_fichier_csv:
            l.append(r)
        return l

def traitement_information(liste_informations, n_suivi=None)->tuple[list,set,list]:
    """Fonction qui prend la listes des lignes du fichier csv et qui ressort la liste des noeuds du graphe 
    et ses différentes arrêtes ainsi que leur pondéraation

    Args:
        liste_informations (list): la liste des lignes d'un fichier
        n_suivi: (int or None): Le numéro du suivi auquels on s'interresse. (None si on s'interesse qu'a la duree initiale)

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
    arcs=set() #L'ensemble des arcs
    poids=[] #La liste des poids
    for ligne in liste_informations: #Pour chaque ligne, donc chaque noeud
        noeud=ligne[0] #On rajoute le noeud à la liste
        noeuds.append(noeud)
        duree_tache=ligne[2] #La duree de la tache est initialement la colonne duree
        if n_suivi!=None: #Si on s'interesse à un suivi
            for i in range(4,5+n_suivi): #Pour chaque colonne de suivi auxquelles on s'interresse
                if ligne[i]!='': #Si le suivi existe
                    duree_tache=ligne[i] #La duree de la tache est celle du suivi
        duree_tache=conversion_unite(duree_tache) #On convertit la duree qui était une valeur suivi d'une unité temporelle en nombre de jour
        poids.append((noeud,duree_tache)) #On associe le noeud à son poids et on le rajoute dans la liste des poids
        if ligne[3]!='': #Si la tache à un prérequis
            pre_noeuds=ligne[3] #La liste des prerequis
            for pre_noeud in pre_noeuds.split(): #Pour chaque prérequis
                arcs.add((pre_noeud, noeud)) #On ajoute l'arc prerequis -> noeud
        if noeud=='F': #Si la tache est la tache finale
            poids_final=duree_tache #Alors on met en évidence le poids final
        
    return noeuds, arcs, poids, poids_final

def conversion_unite(duree_tache):
    """Fonction qui convertie un str d'une duree temporelle et qui le convertir en int qui correspond au nombre de jour 
    que représente cette duree
    La fonction peut raise une UniteError si l'unite de la duree n'est pas connue
    Args:
        duree_tache (str): la duree temporelle avec les unités (mois/annee/semaine)

    Returns:
        int: le nombre de jour qui correspond a la duree
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


def ponderation_branches(arcs, poids)->set:
    """Fonction qui associe les branches et les poids de ces branches

    Args:
        arcs (set): l'ensemble des branches
        poids (list): la liste des poids
            tuples:
                str: Le nom du noeud
                int: Le poid du noeud
    
    Returns:
        set: l'ensemble des arcs ponderees
    """
    arcs_ponderes=set() #L'ensemble des arcs ponderees
    for arc in arcs: #Pour chaque arcs
        pre_noeud=arc[0] #Le noeud iitial de l'arc
        for p in poids: #Pour chaque poids
            if pre_noeud==p[0]: #Si le noeud initial de l'arc est le meme que ce noeud ponderee
                poids_arc=p[1] #Alors le poids de de cet arc est egal au poids du noeud initial
        arcs_ponderes.add((arc[0], arc[1], poids_arc)) #On rajoute au set des arcs ponderres l'arc avec son poids 
    return arcs_ponderes

def csv_to_graph(nom_fichier_csv:str):
    """Fonction qui convertie un fichier CSV en graphe pondérée

    Args:
        nom_fichier_csv (str): Nom du fichier à convertir

    Returns:
        list: les graphes pour chaque suivi
            tuple:
                list: la liste des noeuds
                set: l'ensemble des arcs ponderres
                int: le poids final de la tache qui n'est donc sur aucun arc
    """
    graphs=[] #La liste des graphes
    for n_suivi in [None,0,1,2]: #Pour chaque suivi
        liste_csv=from_csv(nom_fichier_csv) #On converit le fichier en liste
        liste_csv.pop(0) #On en lève le premier terme de la liste qui correspond au indication sur le fichier
        noeuds, arcs, poids, poids_final= traitement_information(liste_csv,n_suivi) #On reccupère les différentes information
        arcs_ponderee=ponderation_branches(arcs, poids) #On créer les arcs ponderes à partir des arcs et des poids
        graphs.append((noeuds,arcs_ponderee, poids_final))  #On créer un tuple aves toutes les informations necessaires à créer un graphes ponderee 
    return graphs