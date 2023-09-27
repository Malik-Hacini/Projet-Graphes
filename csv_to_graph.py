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

def traitement_information(liste_informations)->tuple:
    """Fonction qui prend la listes des lignes du fichier csv et qui ressort la liste des noeuds du graphe 
    et ses différentes arrêtes ainsi que leur pondéraatio n

    Args:
        liste_informations (list): la liste des lignes d'un fichier

    Returns:
        tuple: 
    """
    noeuds=set()
    arcs=set()
    for ligne in liste_informations:
        noeud=ligne[0]
        noeuds.add(noeud)
        try:
            pre_noeuds=ligne[3]
            for pre_noeud in pre_noeuds.split():
                arcs.add((pre_noeud,noeud))
        except:
            pass
    
    return(noeuds, arcs)



def csv_to_graph(nom_fichier_csv:str)-> DiGraphe:
    """Fonction qui convertie un fichier CSV en graphe pondérée

    Args:
        nom_fichier_csv (str): Nom du fichier à convertir

    Returns:
        DiGraphe: Graphe pondérée
    """
    
    liste_csv=from_csv(nom_fichier_csv)
    liste_csv.pop(0)
    noeuds, arcs = traitement_information(liste_csv)
    return(noeuds, arcs)


print(csv_to_graph(test))