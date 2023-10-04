from csv_to_graphe import*

noeuds, arcs_ponderes= csv_to_graph("Tests\\test_boucle")

g=DiGraphe(noeuds,arcs_ponderes)
graphe_to_tex(g)