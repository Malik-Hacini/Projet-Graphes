import sys
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
        
output="""\documentclass{article}
\usepackage{graphicx}
\usepackage{amsmath,amssymb,enumerate,graphicx,pgf,tikz,fancyhdr}
\usepackage{geometry}
\usepackage{tabvar}
\usepackage{fontspec}
\usepackage{dot2texi}

\usepackage{minted}
\usetikzlibrary{backgrounds}
\usetikzlibrary{arrows.meta}
\usetikzlibrary{shapes.geometric}

\begin{document}"""


for compte_rendu in csv_to_graph(f"Tests\\CSV\\test_cool"):
    noeuds, arcs_ponderes, duree_finale = compte_rendu
    graphe_taches=DiGraphe(noeuds,arcs_ponderes)


    output+="\section{Votre Graphe de tâches}\n"    
    chemin,dist=chemin_critique(graphe_taches,0,len(graphe_taches.noeuds)-1)
    graphe_dot=graphe_to_tex(graphe_taches,chemin)
    
    dates=dates_tot_tard(graphe_taches)

    if cycle_detector(g):
        print("Votre projet est infaisable, l'ordonnancement des taches contient une boucle.")
        sys.exit()
        
        
            
         
with open("//output//output.tex","w") as fichier_sortie:
    fichier_sortie.write(output)