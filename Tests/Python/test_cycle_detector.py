import pytest
import networkx as nx
import random
from cycle_detector import*

#Ce test est validé.

def test_cycle_detector():
    for i in range(100):
        g_nx=nx.DiGraph()
        g_nx.add_nodes_from(range(10))
        arcs=[tuple(random.randint(0,9) for x in range(2)) for i in range(random.randint(1,15))]
        arcs=list(set(arcs))
        arcs_ponderes=[(i[0],i[1], random.randint(0,20)) for i in arcs]
        g_nx.add_edges_from(arcs)
        g_test=DiGraphe(list(range(10)),set(arcs_ponderes))
        
        
        assert cycle_detector(g_test) == (not nx.is_directed_acyclic_graph(g_nx))
            
            

