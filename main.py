from csv_to_graphe import*
from cycle_detector import*
from chemins_critiques import*
from graphe_visualisation_latex import*

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
         
noeuds, arcs_ponderes= csv_to_graph(f"Tests\\test_suivi")
g=DiGraphe(noeuds,arcs_ponderes)
print(g.noeuds,g.dict_adj)
chemin,dist=chemin_critique(g,0,len(g.noeuds)-1)
graphe_to_tex(g,chemin)

print(chemin,dist)