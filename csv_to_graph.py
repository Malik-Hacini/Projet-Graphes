import csv
import graphe

def from_csv(nom_fichier_csv: str)->list:
    """Programme qui ouvre un fichier csv et qui le tranforme en liste de liste mot

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

def traitement_information(liste_informations)->tuple:
    """Fonction qui prend la listes des lignes du fichier csv et qui ressort la liste des noeuds du graphe 
    et ses différentes arrêtes ainsi que leur pondéraatio n

    Args:
        liste_informations (list): la liste des lignes d'un fichier

    Returns:
        tuple: 
    """
    noeuds=set()
    arcs=set()
    poids=set()
    for ligne in liste_informations:
        noeud=ligne[0]
        noeuds.add(noeud)
        duree_tache=ligne[2]
        for i in range(4,7):
            if ligne[i]!='':
                duree_tache=ligne[i]
        duree_tache=conversion_unite(duree_tache)
        if ligne[3]!='':
            pre_noeuds=ligne[3]
            for pre_noeud in pre_noeuds.split():
                arcs.add((pre_noeud, noeud))
        poids.add((noeud,duree_tache))
    return noeuds, arcs, poids

def conversion_unite(duree_tache):
    """Fonction qui convertie un str d'une duree temporelle et qui le convertir en int qui correspond au nombre de jour 
    que représente cette duree

    Args:
        duree_tache (str): la duree temporelle avec les unités (mois/annee/semaine)

    Returns:
        int: le nombre de jour qui correspond a la duree
    """
    valeur=int(duree_tache.split()[0])
    unite=duree_tache.split()[1]
    if unite=='mois':
        valeur*=30
    elif unite=='annees':
        valeur*=365
    elif unite=='semaines':
        valeur*=7
    return valeur

def ponderation_branches(arcs, poids):
    """Fonction qui associe les branches et les poids de ces branches

    Args:
        arcs (set): l'ensemble des branches
        poids (_type_): l'ensembles des poids
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
    """Fonction qui convertie un fichier CSV en graphe pondérée

    Args:
        nom_fichier_csv (str): Nom du fichier à convertir

    Returns:
        DiGraphe: Graphe pondérée
    """
    liste_csv=from_csv(nom_fichier_csv)
    liste_csv.pop(0)
    noeuds, arcs, poids= traitement_information(liste_csv)
    arcs_ponderee=ponderation_branches(arcs, poids)
    return noeuds, arcs_ponderee