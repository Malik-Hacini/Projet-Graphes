from Graphes import*

#Traduction d'un graphe en LaTeX
def graphe_to_tex(g: DiGraphe,chemin_critique: list)->str:
    """Donne l'écriture en langage dot d'un graphe de la classe DiGraphe.
    Colore aussi les chemins critiques donnés.
    L'écrit ensuite dans un fichier dot externe.

    Args:
        g (DiGraphe): graphe orienté à traiter

    Returns:
        str: Le code dot du graphe, directement utilisable en LaTeX
    """
    arcs_chemin_critique=[(chemin_critique[i],chemin_critique[i+1]) for i in range(len(chemin_critique)-1)]
    adj=g.dict_adj
    print(adj)
    dot="\\begin{dot2tex}[autosize, options=-tmath,scale=0.8]"
    
    dot+= """
    digraph G{ \n""" + " "*3 + "rankdir=LR \n" + " "*3
    
    for noeud, voisins in adj.items():
        for voisin in voisins:
            dot+=f"{g.noeuds[noeud]}"
            dot+=f' -> {g.noeuds[voisin]} [label="{int(g.mat_adj[noeud,voisin])}"'
            if (noeud,voisin) in arcs_chemin_critique:
                dot+=' color="red"'
            dot+="]; \n" +"   "
    dot+="} \n"
    dot+="\\end{dot2tex}"
    with open("Tests\\graph.dot","w") as f:
        f.write(dot)
    return dot

