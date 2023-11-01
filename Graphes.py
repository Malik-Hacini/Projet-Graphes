
import random
import numpy as np

class DiGraphe:
    def __init__(self,noeuds: list[str],arcs_ponderes : set[tuple[str, str, int]])->None:
        """Construit un graphe orienté à partir des deux ensembles le définissant :
        noeuds et arcs (pondérés). On suppose que le graphe est connexe. On le représentera
        En utilisant sa matrice d'adjacence (array numpy), et un dictionnaire des listes d'adjacence.

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
        
