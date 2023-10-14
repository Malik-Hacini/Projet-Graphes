from Graphes import*

def cycle_detector_recursive_part(g:DiGraphe, noeud, visites: set, pile_recursive: list)->bool:
    """Partie récursive du détécteur de cycle. Se base sur le DFS

    Args:
        g (DiGraphe): Graphe orienté à traiter
        noeud (_type_): Noeud de départ du parcours
        visites (set): La liste des noeuds visités
        pile_recursive (list): La pile des noeuds du parcours en cours.

    Returns:
        bool: True si le graphe a un cycle à partir du noeud de départ, False sinon.
    """
        
    visites.add(noeud)
    pile_recursive.append(noeud)

    for voisin in g.dict_adj[noeud]:
        
        if voisin not in visites:
            if cycle_detector_recursive_part(g, voisin, visites, pile_recursive):
                return True
        elif voisin in pile_recursive:
            return True

    pile_recursive.remove(noeud)
    return False


def cycle_detector(g: DiGraphe)->bool:
    """Détécteur de cycle dans un graphe orienté

    Args:
        g (DiGraphe): Graphe à traiter
    Returns:
        bool: True si le graphe a un cycle à partir du noeud de départ, False sinon.
    """
    visites=set()
    pile_recursive=[]
    for noeud in list(g.noeuds):
        if noeud not in visites:
            if cycle_detector_recursive_part(g, noeud, visites, pile_recursive):
                return True
            
    return False