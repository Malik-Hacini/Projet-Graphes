from Graphes import*

#Traduction d'un graphe en LaTeX
def graphe_to_latex(g: DiGraphe,chemin_critique: list=[])->str:
    """Donne l'écriture en langage dot d'un graphe de tâches de la classe DiGraphe.
    Colore aussi en rouge les chemins critiques donnés.

    Args:
        g (DiGraphe): graphe orienté à traiter

    Returns:
        str: code dot du graphe, directement utilisable en LaTeX
    """
    adj=g.dict_adj
    dot="""\\begin{center}
\\begin{tikzpicture}[scale=0.6, every node/.style={scale=0.6}]
\\begin{dot2tex}[codeonly]\n"""
    
    dot+= """
    digraph G{ \n""" + " "*3 + "rankdir=LR \n" + " "*3
    
    for noeud, voisins in adj.items():
        for voisin in voisins:
            dot+=f"{g.noeuds[noeud]}"
            dot+=f' -> {g.noeuds[voisin]} [label="{int(g.mat_adj[noeud,voisin])}"'
            if (noeud,voisin) in chemin_critique: #on colore en rouge les arcs du chemin critique
                dot+=' color="red"'
            dot+="]; \n" +"   "
    dot+="} \n"
    dot+="""\\end{dot2tex}
\\end{tikzpicture}
\\end{center}\n"""

    return dot

