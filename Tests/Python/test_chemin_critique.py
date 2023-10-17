import pytest
from Graphes import*
from chemins_critiques import*

gr1=DiGraphe(["D","I1","I2","I3","F"],{("D","I1",5),("D","I2",2),("D","I3",8),("I1","I2",4),("I2","F",1),("I3","F",2)})
gr_2_crit=DiGraphe(["D","I1","I2","F"],{("D","I1",2),("D","I2",2),("I1","F",1),("I2","F",1)})

assert chemin_critique(gr1,0,len(gr1.noeuds)-1) == ([0,2,4],3.0)
assert chemin_critique(gr_2_crit,0,len(gr_2_crit.noeuds)-1) == ([0,2,3],3.0)