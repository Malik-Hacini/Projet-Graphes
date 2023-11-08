import pytest
from Graphes import*
from csv_to_graphe import*
from cycle_detector import*
from chemins_critiques import*
from graphe_to_latex import*

#Ce test est validé.
def test_chemin_critique():
    g_def=csv_to_graph("test_chemin_critique_1")[0]
    noeuds, arcs_ponderes,duree_finale= g_def
    g=DiGraphe(noeuds,arcs_ponderes)
    assert ([(0,2), (2,3)],4)==chemin_critique(g, 0 ,len(g.noeuds)-1)
    g_def=csv_to_graph("test_chemin_critique_2")[0]
    noeuds, arcs_ponderes,duree_finale= g_def
    g=DiGraphe(noeuds,arcs_ponderes)
    assert ([(0,1),(1,3),(3,5)],12)==chemin_critique(g, 0 ,len(g.noeuds)-1)