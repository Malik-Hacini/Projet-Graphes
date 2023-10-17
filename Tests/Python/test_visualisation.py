import pytest
from Graphes import*
from chemins_critiques import*
from graphe_visualisation_latex import*
gr1=DiGraphe(["D","I1","I2","I3","F"],{("D","I1",5),("D","I2",2),("D","I3",8),("I1","I2",4),("I2","F",1),("I3","F",2)}) 
gr_2_crit=DiGraphe(["D","I1","I2","F"],{("D","I1",2),("D","I2",2),("I1","F",1),("I2","F",1)})

print(chemin_critique(gr_2_crit,0,len(gr_2_crit.noeuds)-1))

#graphe_to_tex(gr1,chemin)

