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
            dot+=f' -> {voisin[0]} [label="{int(voisin[1])}"]'
            dot+="; \n" +"   "
    dot+="} \n"
    dot+="\\end{dot2tex}"
    with open("Tests\\graph.dot","w") as f:
        f.write(dot)
    return dot


def dijkstra(g: DiGraphe, depart : int, arrivee: int)->list:

    visites={depart}
    chemin=[depart] + [None] * (len(g.noeuds)-1)
    dijkstra_tableau=[float('inf')] * len(g.noeuds)
    for noeud in g.noeuds: 
        dijkstra_tableau[noeud]=g.mat_adj[depart,noeud]
    i=0

    while visites!=g.noeuds:
        if i==30:
            break
        print(visites)
        print(dijkstra_tableau)
        tableau_int=[value for index,value in enumerate(dijkstra_tableau) if index not in visites]
        print("int",tableau_int)
        voisin_plus_proche=[dijkstra_tableau.index(i) for i in tableau_int if  i==min(tableau_int)][0]
        # PROBLEME ICI : Si le poids du voisin le plus proche est présent 2 fois dans dijkstra_tableau
        #, alors on ajoute toujours le premier rencontré, ce qui peut mener a une boucle infinie.
        print("voisin_plus_proche", voisin_plus_proche)
        visites.add(voisin_plus_proche)
        
        for noeud in g.noeuds :
            
            if noeud not in visites:
                print("noued",noeud)
                comparaison= (dijkstra_tableau[noeud],
                    dijkstra_tableau[voisin_plus_proche]+g.mat_adj[voisin_plus_proche,noeud])
                print(comparaison)
                if min(comparaison)==comparaison[1]:
                    dijkstra_tableau[noeud]=comparaison[1]
                    chemin[noeud]=voisin_plus_proche
        
        i+=1    
    return (sum(dijkstra_tableau), chemin)        
            
    


