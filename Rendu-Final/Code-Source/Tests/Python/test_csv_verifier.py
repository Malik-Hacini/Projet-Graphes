import pytest
from csv_verifier import*

def test_fichier_correct():
    assert verification_format_fichier("test_cool")==True,"Fichier valide"
    assert verification_format_fichier("test_cool")==True,"Fichier valide"
    
    
def test_fichier_incorrect():
    assert verification_format_fichier("test_4_suivi")==False,"Le fichier ne comporte pas les colonnes nécéssaires"
    assert verification_format_fichier("test_2taches_2")==False,'Il y a 2 fois la même tâche 2 aux lignes 4 et 5'
    assert verification_format_fichier("test_pas_de_durée")==False,"La tâche D Tache de début n'a pas de durée indiquée à la ligne 2"
    assert verification_format_fichier("test_erreur_unité")==False, "Unité erronée à la ligne 2 dans la colonne 3"