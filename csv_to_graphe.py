import csv
from Graphes import*

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

def traitement_information(liste_informations, n_suivi=None)->tuple[list,set,list]:
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
    noeuds=[]
    arcs=set()
    poids=[]
    for ligne in liste_informations:
        noeud=ligne[0]
        noeuds.append(noeud)
        duree_tache=ligne[2]
        if n_suivi!=None:
            for i in range(4,5+n_suivi):
                if ligne[i]!='':
                    duree_tache=ligne[i]
        duree_tache=conversion_unite(duree_tache)
        poids.append((noeud,duree_tache))
        if ligne[3]!='':
            pre_noeuds=ligne[3]
            for pre_noeud in pre_noeuds.split():
                arcs.add((pre_noeud, noeud))
        if noeud=='F':
            poids_final=duree_tache       
        
    return noeuds, arcs, poids, poids_final

def conversion_unite(duree_tache):
    """Convertit toutes les unités de temps en jours. On suppose 1 mois=30 jours.

    Args:
        duree_tache (str): la duree avec les unités (jours/mois/annee/semaine)

    Returns:
        int: la durée en jours.
    """
    valeur=float(duree_tache.split()[0])
    unite=duree_tache.split()[1]
    if unite=='mois':
        valeur*=30
    elif unite=='annees' or unite=='annee':
        valeur*=365
    elif unite=='semaines' or unite=='semaine':
        valeur*=7
    elif unite=='jours' or unite=='jour':
        valeur=valeur
    return valeur


def ponderation_branches(arcs, poids)->set:
    """Pour réaliser un graphe à partir de l'output de traitement_information, associe chaque
    voisin d'un noeud donné par un arc du poids du noeud donné. 

    Args:
        arcs (set): l'ensemble des branches
        poids (_type_): l'ensemble des poids
    
    Returns:
        set: l'ensemble des arcs ponderés
    """
    arcs_ponderee=set()
    for arc in arcs:
        pre_noeud=arc[0]
        for p in poids:
            if pre_noeud==p[0]:
                poids_branche=p[1]
        arcs_ponderee.add((arc[0], arc[1], poids_branche))
    return arcs_ponderee 

def csv_to_graph(nom_fichier_csv:str):
    """A partir d'un nom de fichier csv, renvoie les ensembles de définitions des graphes de tâches
    associés à l'analyse initiale, et chaque compte rendu d'éxécution du fichier.

    Args:
        nom_fichier_csv (str): nom du fichier à convertir

    Returns:
        graphs (list): Liste imbriquée d'ensembles de définition de graphes associés au fichier
    """
    graphs=[]
    for n_suivi in [None,0,1,2]: #On répète l'opération pour chaque compte rendu d'éxécution
        liste_csv=from_csv(nom_fichier_csv)
        liste_csv.pop(0)
        noeuds, arcs, poids, poids_final= traitement_information(liste_csv,n_suivi)
        arcs_ponderee=ponderation_branches(arcs, poids)
        graphs.append((noeuds,arcs_ponderee, poids_final))
    return graphs 
