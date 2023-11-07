import pytest
from Graphes import*
from csv_to_graphe import*
from cycle_detector import*
from chemins_critiques import*
from graphe_to_latex import*

def test_chemin_critique():
    g=csv_to_graph("test_chemin_critique_1")
    assert ([0, 2, 3],4)==chemin_critique(g, 0 ,len(g.noeuds)-1)
    g=csv_to_graph("test_chemin_critique_2")
    assert ([0, 1, 3, 5],12)==chemin_critique(g, 0 ,len(g.noeuds)-1)