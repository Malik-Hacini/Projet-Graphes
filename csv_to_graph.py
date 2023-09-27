import csv
import graphe

def from_csv(nom_fichier_csv: str)->list:
    """Programme qui ouvre un fichier csv et qui le tranforme en liste de liste mot

    Args:
        nom_fichier_csv (str): Nom du fichier à utiliser

    Returns:
        list: Liste ou chaque terme est une liste qui correspond à une ligne et chaque terme de cette liste est un mot de la ligne
    """
    with open(nom_fichier_csv + ".csv" , 'r', encoding="utf−8" ) as fichier_csv:
        lecture_fichier_csv =csv.reader(fichier_csv, delimiter= "," ,quoting=csv.QUOTE_ALL)
        l=[]
        for r in lecture_fichier_csv:
            l.append(r)
        return l
    
    
