import pytest
import coverage
from csv_to_graphe import*

def test_conversion_unite():
    
    assert conversion_unite('3 jours')==3
    assert conversion_unite('1 jour')==1
    assert conversion_unite('3 semaines')==21
    assert conversion_unite('2 mois')==60
    assert conversion_unite('1 annee')==365
    try:
        valeur=conversion_unite("1 banane")
    except UniteError:
        assert 0==0
    else:
        assert 1==0

def test_ponderation_branche():
    assert ponderation_branches({(0,1)},[(0,30)])=={(0,1,30)}
    assert ponderation_branches({(0,1),(0,2),(2,3)},[(0,2),(1,3),(2,5),(3,1)])=={(0,1,2),(0,2,2),(2,3,5)}
    
def test_traitement_information():
    l=[['D','1er tache','2 mois','','1 mois','2 semaines','1 semaine'],['F','tache finale','1 mois','D','3 semaines','2 semaines','1 semaines']]
    assert traitement_information(l)==(['D','F'],{('D','F')},[('D',60),('F',30)],30)
    assert traitement_information(l,0)==(['D','F'],{('D','F')},[('D',30),('F',21)],21)
    assert traitement_information(l,1)==(['D','F'],{('D','F')},[('D',14),('F',14)],14)
    assert traitement_information(l,2)==(['D','F'],{('D','F')},[('D',7),('F',7)],7)
    l=[['D', 'Tache de debut', '2 mois', '', '', '', ''], ['I1', 'Tache intermediaire 1', '1 mois', 'D', '', '', ''], ['I2', 'Tache intermediaire 2', '3 mois', 'D', '', '', ''], ['I3', 'Tache intermediaire 3', '2 mois', 'D', '', '', ''], ['F', 'Tache de fin', '2 mois', 'I1 I2 I3', '', '', '']]
    assert traitement_information(l)==(['D','I1','I2','I3','F'],{('D','I1'),('D','I2'),('D','I3'),('I1','F'),('I2','F'),('I3','F')},[('D',60),('I1',30),('I2',90),('I3',60),('F',60)],60)
    
def test_csv_to_graph():
    nom_test="test_csv_to_graph"
    output=[(['D', 'I1', 'I2', 'F'], {('D', 'I1', 30.0), ('D', 'I2', 30.0), ('I1', 'F', 14.0), ('I2', 'F', 1.0)}, 1.0),#Sans suivi
(['D', 'I1', 'I2', 'F'], {('D', 'I1', 60.0), ('D', 'I2', 60.0), ('I1', 'F', 21.0), ('I2', 'F', 2.0)}, 1.0),#S0
(['D', 'I1', 'I2', 'F'], {('D', 'I1', 90.0), ('D', 'I2', 90.0), ('I1', 'F', 21.0), ('I2', 'F', 3.0)}, 3.0),#S1
(['D', 'I1', 'I2', 'F'], {('D', 'I1', 90.0), ('D', 'I2', 90.0), ('I1', 'F', 35.0), ('I2', 'F', 3.0)}, 4.0)]#S2
    assert csv_to_graph(f"Projets\\{nom_test}")==output