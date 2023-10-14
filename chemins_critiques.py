from Graphes import*

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
    print(distances)
    distances[source]=0
    pred={source:source} #Le dictionnaire des prédecésseurs
    
    for i in range(len(g.noeuds)):
        noeud_dis_min=noeud_distance_mini(distances,traites)
        traites[noeud_dis_min]=noeud_dis_min
        
        for voisin in g.dict_adj[noeud_dis_min]:
            print("noeud_min",noeud_dis_min,"voisin", voisin)
            distance_noeud_dis_min_puis_voisin= distances[noeud_dis_min] + g.mat_adj[noeud_dis_min,voisin] #Distance de la source au noeud_dis_min, puis au voisin
            if distances[voisin]>distance_noeud_dis_min_puis_voisin: #On vérifie si passer par le noeud_dis_min est une bonne idée (cela rend il la distance de source à voisin plus faible)
                distances[voisin]=distance_noeud_dis_min_puis_voisin
                pred[voisin]=noeud_dis_min
    
    return distances,pred
            
def chemin_critique(g: DiGraphe, source: int, arrivee: int)->tuple[list,float]:
    """Renvoie un des chemins critiques d'un DiGraphe d'une source à une arrivée,
    ainsi que sa distance. 
    

    Args:
        g (DiGraphe): _description_
        source (int): _description_
        arrivee (int): _description_

    Returns:
        _type_: _description_
    """
    etape_chemin=arrivee
    distances,pred=dijkstra(g, source)
    print("pred",pred)
    print("distances",distances)
    chemin=[etape_chemin]
    while etape_chemin!=source: 
        etape_chemin=pred[etape_chemin] #On remonte le chemin à l'envers (à partir des prédécésseurs)
        chemin.append(etape_chemin)
    chemin=chemin[::-1] #On remet le chemin dans le bon sens
    
    return chemin,distances[arrivee]