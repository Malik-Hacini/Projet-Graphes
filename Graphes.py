import networkx as nx
import random
import numpy as np

class DiGraphe:
    def __init__(self,noeuds: list[str],arcs_ponderes : set[tuple[str, str, int]])->None:
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
        for noeud in noeuds:
            noeuds_dict[i]= noeud
            i+=1
        
        
        mat_adj=np.full((len(noeuds),len(noeuds)), np.inf)
        
        keys=list(range(len(noeuds)))
        vals=list(noeuds_dict.values())
        for arc in arcs_ponderes:
            ligne=keys[vals.index(arc[0])]
            col=keys[vals.index(arc[1])]
            mat_adj[ligne,col]=arc[2]

        for i in range(len(noeuds)):
            mat_adj[i,i]=0
            
        
        self.dict_adj={key: [keys[vals.index(a[1])] for a in arcs_ponderes if a[0]==value] for key,value in noeuds_dict.items()}
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



            