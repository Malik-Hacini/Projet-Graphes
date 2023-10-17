import pytest
from csv_to_graphe import*

def test_conversion_unite():
    assert conversion_unite('3 jours')==3
    assert conversion_unite('1 jour')==1
    assert conversion_unite('3 semaines')==21
    assert conversion_unite('2 mois')==60
    assert conversion_unite('1 annee')==365

def test_ponderation_branche():
    assert ponderation_branches({(0,1)},[(0,30)])=={(0,1,30)}
    assert ponderation_branches({(0,1),(0,2),(2,3)},[(0,2),(1,3),(2,5),(3,1)])=={(0,1,2),(0,2,2),(2,3,5)}
    
def test_traitement_information():
    l=[['D','1er tache','2 mois','','1 mois','2 semaines','1 semaine'],['F','tache finale','1 mois','D','3 semaines','2 semaines','1 semaines']]
    assert traitement_information(l)==(['D','F'],{('D','F')},[('D',60),('F',30)])
    assert traitement_information(l,0)==(['D','F'],{('D','F')},[('D',30),('F',21)])
    assert traitement_information(l,1)==(['D','F'],{('D','F')},[('D',14),('F',14)])
    assert traitement_information(l,2)==(['D','F'],{('D','F')},[('D',7),('F',7)])
    l=[['D', 'Tache de debut', '2 mois', '', '', '', ''], ['I1', 'Tache intermediaire 1', '1 mois', 'D', '', '', ''], ['I2', 'Tache intermediaire 2', '3 mois', 'D', '', '', ''], ['I3', 'Tache intermediaire 3', '2 mois', 'D', '', '', ''], ['F', 'Tache de fin', '2 mois', 'I1 I2 I3', '', '', '']]
    assert traitement_information(l)==(['D','I1','I2','I3','F'],{('D','I1'),('D','I2'),('D','I3'),('I1','F'),('I2','F'),('I3','F')},[('D',60),('I1',30),('I2',90),('I3',60),('F',60)])