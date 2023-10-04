import networkx as nx
import random
import numpy as np

class DiGraphe:
    def __init__(self,noeuds: set[str],arcs_ponderes : set[tuple[str, str, int]])->None:
        """Construit un graphe orienté à partir des deux ensembles le définissant :
        noeuds et arcs (pondérés). On suppose que le graphe est connexe. On le représentera
        En utilisant sa matrice d'adjacence (array numpy)

        Args:
            noeuds (dict[int,str])): noeuds du graphe orienté. La clé est un entier (pour ordonner les noeuds)
            et la valeur une chaine de caractères (l'information que porte le noeud)
            arcs_ponderes (set[tuple[int,int,int]): arcs du graphe orienté. 
            L'entier représente la pondération de l'arc.
        """
        noeuds_dict=dict()
        
        i=0
        for noeud  in noeuds:
            noeuds_dict[i]= noeud
            i+=1
        
        
        mat_adj=np.full((len(noeuds),len(noeuds)), float('inf'))
        
        for arc in arcs_ponderes:
            
            mat_adj[arc[0],arc[1]]=arc[2]

        for i in range(len(noeuds)):
            mat_adj[i,i]=0
            
        keys=list(noeuds_dict.keys())
        vals=list(noeuds_dict.values())
        
        self.dict_adj={n:[ (noeuds_dict[a[1]],a[2]) for a in arcs_ponderes if a[0]==keys[vals.index(n)]] for n in noeuds}
        self.noeuds=noeuds_dict
        self.mat_adj=mat_adj
        
        

        
        
    
        

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
        for voisin in g.dict_adj[noeud]:
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
        for voisin in g.dict_adj[noeud]:
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


def graphe_to_tex(g: DiGraphe)->str:
    """Donne l'écriture en langage dot d'un graphe de la classe DiGraphe.
    L'écrit ensuite dans un fichier texte séparé.

    Args:
        g (DiGraphe): graphe orienté à traiter

    Returns:
        str: Le code dot du graphe, directement utilisable en LaTeX
    """
    
    adj=g.dict_adj
    print(adj)
    dot="\\begin{dot2tex}[autosize, options=-tmath,scale=0.8]"
    
    dot+= """
    digraph G{ \n""" + " "*3 + "rankdir=LR \n" + " "*3
    
    for noeud, voisins in adj.items():
        for voisin in voisins:
            dot+=f"{noeud}"
            dot+=f' -> {voisin[0]} [label="{voisin[1]}"]'
            dot+="; \n" +"   "
    dot+="} \n"
    dot+="\\end{dot2tex}"
    with open("C:\\Users\\juioi\\Desktop\\Majeure Info\\Graphes et Arbres\\Projet-Graphes\\graph.dot","w") as f:
        f.write(dot)
    return dot


            

graphe_test=DiGraphe({"test0","test1","test2"},((0, 2, 2), (0, 1, 4),(2, 1, 6)))

print(graphe_test.mat_adj)
graphe_to_tex(graphe_test)