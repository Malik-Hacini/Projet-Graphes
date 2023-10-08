from csv_to_graphe import*
from Algo_graphes import*
""" nom_correct=False
while not nom_correct:
    try:
        nom=input("Quel est le nom du csv de votre projet ? \n")
        f=open(f"Test\\{nom}.csv","r")
        f.close()
        nom_correct=True
    except:
        print("Fichier introuvable ou format incorrect")
         """
         
noeuds, arcs_ponderes= csv_to_graph(f"Tests\\test")
graphe_to_tex(g)