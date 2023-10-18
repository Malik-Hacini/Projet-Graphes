import sys
from csv_to_graphe import*
from cycle_detector import*
from chemins_critiques import*
from graphe_visualisation_latex import*


output="""\documentclass{article}
\\usepackage{graphicx}
\\usepackage{amsmath,amssymb,enumerate,graphicx,pgf,tikz,fancyhdr}
\\usepackage{geometry}
\\usepackage{tabvar}
\\usepackage{fontspec}
\\usepackage{dot2texi}
\\usepackage[utf8]{inputenc}
\\usepackage{minted}
\\usetikzlibrary{backgrounds}
\\usetikzlibrary{arrows.meta}
\\usetikzlibrary{shapes.geometric}
\\title{\\centering Peer Review and Evaluation Technique : Votre Projet. 
}

\\author{PERT Maker}
\\date{26 Septembre 2023}
\\renewcommand{\contentsname}{Table des Matières}
\\begin{document}
\\maketitle
\\tableofcontents{}\n"""

i=0
#for compte_rendu in csv_to_graph(f"Tests\\CSV\\test_suivi"):
compte_rendu=csv_to_graph(f"Tests\\CSV\\test_boucle")
print(compte_rendu)

noeuds, arcs_ponderes,duree_finale= compte_rendu[0]
print("noeuds", noeuds)
print("arcs",arcs_ponderes)
print("duree", duree_finale)
graphe_taches=DiGraphe(noeuds,arcs_ponderes)


output+="\section{Votre Graphe de tâches}\n"    
chemin,dist=chemin_critique(graphe_taches,0,len(graphe_taches.noeuds)-1)
output+=graphe_to_tex(graphe_taches,chemin)

output+="\section{Analyse de votre projet}\n"
dates=dates_tot_tard(graphe_taches)

if cycle_detector(graphe_taches):
    output+="Votre projet est infaisable, l'ordonnancement des taches contient une boucle.\n"
else:
    output+=f"""Votre projet possède un temps incompressible de {duree_finale+dist} jours.
    Il s'agit de la durée minimale de votre projet, en supposant que tout se passe mieux que prévu, c'est 
    à dire en suivant le chemin critique (visualisé en rouge).
    Pour terminer le projet dans ces délais, les durées de toutes les tâches parallèles au tâches critiques doivent pouvoir être réduites
    à la même durée que celle des tâches critiques, et qu'aucun retard n'est pris pendant l'ensemble du projet.
    """
output+="\end{document}"
with open(f"output\\output_{i}.tex","w", encoding="utf-8") as fichier_sortie:
    fichier_sortie.write(output) 
i+=1