from Graphes import*
import copy
def noeud_distance_mini(distances: dict,traites: list)->int:
    """Renvoie un noeud non traité dont la valeur dans
    le dictionnaire des distances est minimale.

    Args:
        Distances (dict): le dictionnaires des distances
        traites (list): la liste des sommets déjà traités
    Returns:
        noeud_min(int): le noeud non traité dont la distance est la plus faible
    """
    min=np.inf
    for noeud in distances:
        if noeud not in traites and distances[noeud]<=min:
            min=distances[noeud]
            noeud_min=noeud
            
    return noeud_min

def dijkstra(g: DiGraphe, source: int)->tuple[dict,dict]:
    """Performe l'algorithme de Dijkstra sur un DiGraphe. A partir 
    d'un certain noeud source, détermine les plus courts chemins jusqu'à chaque noeud du graphe.

    Args:
        g (DiGraphe): DiGraphe à traiter
        source (int): noeud source

    Returns:
        tuple(dict,dict)]: le dictionnaire des distances des plus cours chemin, le dictionnaire des prédécésseurs
    """
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
            
def chemin_critique(g: DiGraphe, source: int, arrivee: int)->tuple[list,float]:
    """Renvoie un des chemins critiques (le plus court) d'un DiGraphe d'une source à une arrivée,
    ainsi que sa durée.
    

    Args:
        g (DiGraphe): Graphe à traiter
        source (int): Noeud (tache) source
        arrivee (int): Noeud (tache) d'arrivée

    Returns:
        tuple[list,float]: Le chemin, et sa durée (distance)
    """
    etape_chemin=arrivee
    distances,pred=dijkstra(g, source)
    chemin=[etape_chemin]
    while etape_chemin!=source: 
        etape_chemin=pred[etape_chemin] #On remonte le chemin à l'envers (à partir des prédécésseurs)
        chemin.append(etape_chemin)
    chemin=chemin[::-1] #On remet le chemin dans le bon sens
    
    return chemin,distances[arrivee]


def dates_tot_tard(g: DiGraphe)->tuple[float,float]:


    dates=dict()
    g_oppose=copy.deepcopy(g)
    
    for i in range(len(g.noeuds)):
        for j in range(len(g.noeuds)):
            if (i,j)==(3,4) :
                print(i,j , g_oppose.mat_adj[i,j])
            g_oppose.mat_adj[i,j]= -g_oppose.mat_adj[i,j]
    
    distances_plus_courtes,pred=dijkstra(g,0)
    
    
    distances_plus_longues,pred=dijkstra(g_oppose,0)
    print("longues",distances_plus_longues)

    for i in range(1,len(g.noeuds)-1):
        dates[i]=(distances_plus_courtes[i],-distances_plus_longues[i])
        print(i,dates[i])
    
    return dates
    