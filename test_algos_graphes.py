import pytest
from Algo_graphes import*


noeuds=['wsh',"la","zone","gang","niska"]
arcs_ponderes={('wsh','la',4),("wsh","gang",6),("gang", "niska",1),('la','zone',3),('zone','niska',10)}
g=DiGraphe(noeuds,arcs_ponderes)

result=dijkstra(g,0,len(g.noeuds) )
print(result)