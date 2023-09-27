import networkx as nx
import random


class DiGraphe:
    def __init__(self,noeuds: set[int],arcs : set[tuple[int,int]])->None:
        """Construit un graphe orienté à partir des deux ensembles le définissant :
        noeuds et arcs.

        Args:
            noeuds (set[int]): noeuds du graphe orienté
            arcs (set[tuple[int,int]]): arcs du graphe orienté
        """
        self.noeuds=noeuds
        #Dictionnaire des listes d'adjacence. On trie les listes pour que les parcours
        #du graphe orienté ne dépendent pas de l'ordre de définition des arcs 
        # (on priorise toujours le noeud le plus grand)
        self.adj={ n: sorted([ a[1] for a in arcs if a[0]==n ]) for n in noeuds}
    
        

def parcours_largeur(g: DiGraphe, noeud: int)->list:
    """Réalise le parcours en largeur d'un graphe orienté 
    à partir d'un noeud donné. Utilise une file
    (structure de donnée linéaire de type FIFO "premier arrivé, premier sorti)

    Args:
        g (graphe orienté): graphe orienté à parcourir
        n (int): Noeud de départ

    Returns:
        list: parcours du graphe orienté, dans l'ordre de réalisation (correspond aussi
        au parcours hiérarchique de l'arborescence du noeud)
    """
    try:
        assert noeud in g.noeuds
    except:
        return None
    parcours=[noeud]
    file=[noeud]
    while len(file) != 0:
        noeud = file.pop(0)
        for voisin in g.adj[noeud]:
            if voisin not in parcours:
                file.append(voisin)
                parcours.append(voisin)
    return parcours
        
def parcours_profondeur(g: DiGraphe, noeud: int)->list:
    """Réalise le parcours en profondeur d'un graphe orienté 
    à partir d'un noeud donné. Utilise une pile
    (structure de donnée linéaire de type LIFO "dernier arrivé, premier sorti)

    Args:
        g (graphe orienté): graphe orienté à parcourir
        n (int): Noeud de départ

    Returns:
        list: parcours du graphe orienté, dans l'ordre de réalisation (correspond aussi
        au parcours préfixe de l'arborescence du noeud)
    """
 
    try:
        assert noeud in g.noeuds
    except:
        return None
    
    parcours=[]
    pile=[noeud]
    while len(pile) != 0:
        noeud = pile.pop(-1)
        parcours.append(noeud)
        for voisin in g.adj[noeud]:
            if voisin not in parcours and voisin not in pile:
                pile.append(voisin)
    return parcours

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

    for voisin in g.adj[noeud]:
        
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


def graphe_to_tex(g: DiGraphe)->str:
    """Donne l'écriture en langage dot d'un graphe de la classe DiGraphe.
    L'écrit ensuite dans un fichier texte séparé.

    Args:
        g (DiGraphe): graphe orienté à traiter

    Returns:
        str: Le code dot du graphe, directement utilisable en LaTeX
    """
    
    adj=g.adj
    dot="\\begin{dot2tex}[autosize, options=-tmath,scale=0.8]"
    
    dot+= """
    digraph G{ \n""" + " "*3 + "rankdir=LR \n" + " "*3
    
    for noeud, voisins in adj.items():
        for voisin in voisins:
            dot+=f"{noeud}"
            dot+=f" -> {voisin}"
            dot+="; \n" +"   "
    dot+="} \n"
    dot+="\\end{dot2tex}"
    with open("C:\\Users\\juioi\\Desktop\\Majeure Info\\Graphes et Arbres\\TPs\\3\\graph.dot","w") as f:
        f.write(dot)
    return dot


            

graphe_test=DiGraphe(set(range(10)),
    {(5,8),(8,2),(2,9),(4,8),(4,0),(0,7),(7,6),(2,4),(8,1),(1,3),(1,6)})

graphe_to_tex(graphe_test)