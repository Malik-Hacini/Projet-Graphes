import pytest
from csv_verifier import*

def test_fichier_correct():
    fichier=from_csv("test_cool")
    assert verification_format_fichier(fichier)==(True,"Fichier valide")
    
    fichier=from_csv("test_boucle")
    assert verification_format_fichier(fichier)==(True,"Fichier valide")
    
    
def test_fichier_incorrect():
    fichier=from_csv("test_4_suivi")
    assert verification_format_fichier(fichier)==(False,"Le fichier ne comporte pas les colonnes nécéssaires")
    fichier=from_csv("test_2taches_2")
    assert verification_format_fichier(fichier)==(False,'Il y a 2 fois la même tâche 2 aux lignes 4 et 5')
    fichier=from_csv("test_0tache_finale")
    assert verification_format_fichier(fichier)==(False,"Cette organisation ne prévoit pas de tache finale")
    fichier=from_csv("test_pas_de_durée")
    assert verification_format_fichier(fichier)==(False,"La tâche D Tache de debut n'a pas de durée indiquée à la ligne 2")
    fichier=from_csv("test_erreur_unité")
    assert verification_format_fichier(fichier)==(False, "Unité erronée à la ligne 2 dans la colonne Duree")