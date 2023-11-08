from Graphes import*
import copy
"""
def noeud_distance_mini(distances: dict,traites: list)->int:
    Renvoie un noeud non traité dont la valeur dans
    le dictionnaire des distances est minimale.

    Args:
        Distances (dict): le dictionnaires des distances
        traites (list): la liste des sommets déjà traités
    Returns:
        noeud_min(int): le noeud non traité dont la distance est la plus faible
    
    min=np.inf
    for noeud in distances:
        if noeud not in traites and distances[noeud]<=min:
            min=distances[noeud]
            noeud_min=noeud
            
    return noeud_min

def dijkstra(g: DiGraphe, source: int)->tuple[dict,dict]:
    Performe l'algorithme de Dijkstra sur un DiGraphe. A partir 
    d'un certain noeud source, détermine les plus courts chemins jusqu'à chaque noeud du graphe.

    Args:
        g (DiGraphe): DiGraphe à traiter
        source (int): noeud source

    Returns:
        tuple(dict,dict)]: le dictionnaire des distances des plus cours chemin, le dictionnaire des prédécésseurs
    
    traites={} #Dictionnaire dont les clés sont les sommets traités  
    distances={noeud:np.inf for noeud in g.noeuds} #Dictionnaire des distances (valeur) pour aller de la source à un noeud (clé)
    distances[source]=0
    pred={source:source} #Le dictionnaire des prédecésseurs
    
    for i in range(len(g.noeuds)):
        noeud_dis_min=noeud_distance_mini(distances,traites)
        traites[noeud_dis_min]=noeud_dis_min #On utilise un dict au lieu d'une list, car l'accès à un dict se fait en temps constant,contrairement aux listes.
        #Cela améliore grandement le temps de calcul lorsque le graphe possède beaucoup d'arretes.
        for voisin in g.dict_adj[noeud_dis_min]:
            
            distance_noeud_dis_min_puis_voisin= distances[noeud_dis_min] + g.mat_adj[noeud_dis_min,voisin] #Distance de la source au noeud_dis_min, puis au voisin
            if distances[voisin]>distance_noeud_dis_min_puis_voisin: #On vérifie si passer par le noeud_dis_min est une bonne idée (cela rend il la distance de source à voisin plus faible)
                distances[voisin]=distance_noeud_dis_min_puis_voisin
                pred[voisin]=noeud_dis_min
    return distances,pred
"""

def bellmanFord(g: DiGraphe, source:int)->tuple[dict,dict]:
    """Performe l'algortihme de Bellman-Ford sur un graphe pondéré. Parcours un graphe à partir 
    d'une source, et en détérmine les plus courts chemins vers chaque noeud.

    Args:
        g (DiGraphe): graphe à traiter
        source (int): noeud de départ

    Returns:
        tuple[dict,dict]: le dict des distances , le dict des prédécésseurs (pour reconstruire le chemin)
    """
    distances = {} 
    predecesseurs = {}
    for noeud in g.noeuds:
        distances[noeud] = np.inf
        predecesseurs[noeud] = None
    distances[source] = 0
    
    for i in range(len(g.noeuds)-1):
        for j in g.noeuds:
            for k in g.dict_adj[j]: 
                if distances[k] > distances[j] + g.mat_adj[j,k]:
                    distances[k]  = distances[j] + g.mat_adj[j,k]
                    predecesseurs[k] = j
    return distances, predecesseurs



def chemin_critique(g: DiGraphe,    source: int, arrivee: int)->tuple[list,float]:
    """Renvoie les arcs d'un des chemins critiques (le plus long) d'un DiGraphe d'une source à une arrivée,
    ainsi que sa durée. S'appuie sur la fonction bellmanFord
    

    Args:
        g (DiGraphe): graphe à traiter
        source (int): noeud source
        arrivee (int): noeud d'arrivée

    Returns:
        tuple[list,float]: Les arcs du chemin, et sa durée (distance)
    """
    etape_chemin=arrivee
    #On crée un graphe dont les poids sont les opposés des poids du graphe d'origine.
    #De cette manière, la recherche dU chemin le plus long (chemin critique) dans le graphe d'origine 
    #revient à la recherche du chemin le plus court dans ce nouveau graphe.
    g_oppose=copy.deepcopy(g)
    g_oppose.mat_adj=-g_oppose.mat_adj
    distances,pred=bellmanFord(g_oppose, source)
    chemin=[]
    while etape_chemin!=source: 
        pred_actuel=pred[etape_chemin] #On remonte le chemin à l'envers (à partir des prédécésseurs)
        chemin.append((pred_actuel,etape_chemin))
        etape_chemin=pred_actuel
    chemin=chemin[::-1]
    return chemin, -distances[arrivee]


def dates_tot_tard(g: DiGraphe,duree_finale:int)->dict[tuple[float,float,float]]:
    """Renvoie les dates de référence de chaque tâche d'un graphe.
    S'appuie sur la fonction bellmanFord. La durée de la tâche finale
    est un paramètre nécéssaire, car n'ayant pas de voisin, sa durée n'est pas encodée dans 
    les arcs menants à ses voisins, contrairement aux autres tâches.

    Args:
        g (DiGraphe): graphe à traiter
        duree_finale (int): durée de la tâche finale

    Returns:
        dict[tuple[float,float,float]]: dictionnaire des dates. 3 dates pour chaque tâche
    """

    dates=dict()
    
    #On crée un graphe dont les poids sont les opposés des poids du graphe d'origine.
    #De cette manière, la recherche des distances les plus longues revient à la recherche
    #des distances les plus courtes dans ce nouveau graphe.
    g_oppose=copy.deepcopy(g)
    g_oppose.mat_adj=-g_oppose.mat_adj
    
    distances_plus_courtes,pred=bellmanFord(g,0)

    distances_plus_longues,pred=bellmanFord(g_oppose,0)
    
    for i in range(len(g.noeuds)): #On ne prend pas la tache finale (pas de voisin)
        #car sa duree est en paramètre de la fonction.
        
        if i!=(len(g.noeuds)-1): 
            voisin=g.dict_adj[i][0]  
            duree=g.mat_adj[i,voisin]
        else:
            duree=duree_finale
        #On renvoie les 3 dates de références pour chaque tâche : début au plus tôt, fin au plus tôt, fin au plus tard.
        dates[i]=(distances_plus_courtes[i],distances_plus_courtes[i]+duree,-distances_plus_longues[i]+duree)
    return dates
    