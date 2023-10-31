import sys
import time
from Graphes import*
from csv_to_graphe import*
from cycle_detector import*
from chemins_critiques import*
from graphe_to_latex import*

"""Ce fichier est le principal du logiciel. C'est lui qu'on compile en éxécutable. On analyse
un graphe, et on écrit les analyses en LaTeX dans des fichiers .tex.
"""


start_document="""\\PassOptionsToPackage{dvipsnames}{xcolor}
\\documentclass{article}
\\usepackage{graphicx}
\\usepackage{amsmath,amssymb,enumerate,graphicx,pgf,tikz,fancyhdr}
\\usepackage[dvipsnames]{xcolor}
\\usepackage{geometry}
\\usepackage{tabvar}
\\usepackage{dot2texi}
\\usetikzlibrary{backgrounds}
\\usetikzlibrary{arrows.meta}
\\usetikzlibrary{shapes.geometric}
\\title{\\centering Peer Review and Evaluation Technique : Votre Projet. 
}

\\author{PERT Maker}
\\renewcommand{\contentsname}{Table des Matières}
\\begin{document}
\\maketitle
\\tableofcontents{}\n"""

i=0

nom_correct=False
liste_fichiers=[fichier for fichier in os.listdir("./Projets") if os.path.splitext(fichier)[-1].lower()==".csv"]
if liste_fichiers ==[]:
    exit=input("""Le dossier Projet est vide, ou ne contient pas de fichier CSV. Veuillez vérifier quer vous avez placé votre fichier CSV dans le dossier,
conformément au manuel d'utilisation. 
Appuyez sur Entrée pour quitter""")
    time.sleep(1)
    sys.exit()
    
print("Voici les fichiers disponibles: ")
for fichier in liste_fichiers:
    print("-", fichier[:-4])
print("Si vous ne voyez pas votre fichier, veuillez vérifier qu'il est bien au format CSV, et situé dans le dossier Projets. ")


while not nom_correct:
    try:
        nom_projet=input("Veuillez entrer le nom du fichier du projet à analyser ? : \n")
        infos_projet=csv_to_graph(f"Projets\\{nom_projet}")
        nom_correct=True
    except OSError:
        print("Fichier introuvable.")
    except Exception:
        print("Fichier de format invalide. Se référer au manuel d'utilisation.")


for cr_exec in infos_projet:
    
    if i==0:
        print(("Analyse Initiale..."))
    else:
        print(f"Compe Rendu d'éxécution {i}")
        
    #On crée le graphe de tâches.
    noeuds, arcs_ponderes,duree_finale= cr_exec
    graphe_taches=DiGraphe(noeuds,arcs_ponderes)
    
    print("Graphe de tâches créé.")
    print("Analyse du graphe et création du LaTeX en cours...")
    
    output=start_document
    output+="\section{Votre Graphe de tâches}\n"  
      
    #On ajoute la visualisation du graphe à l'analyse.
    
    cycle=cycle_detector(graphe_taches)
    if cycle:
        #Si le graphe de tâches du projet est cyclique, l'analyse ne peut pas poursuivre.
        output+=graphe_to_tex(graphe_taches)
        output+="\section{Analyse de votre projet}\n"
        output+="Votre projet est infaisable, l'ordonnancement des taches contient une boucle.\n"
        print("Analyse du graphe terminée.")

    else:
        chemin,dist=chemin_critique(graphe_taches,0,len(graphe_taches.noeuds)-1)
        dates=dates_tot_tard(graphe_taches,duree_finale)
        print("Analyse du graphe terminée.")
        
        output+=graphe_to_tex(graphe_taches,chemin)
        output+="\section{Analyse de votre projet}\n"
        
    
        output+=f"""Votre projet possède un temps incompressible de {round(duree_finale+dist)} jours.
    Il s'agit de la durée totale du \\textcolor{{red}}{{chemin critique}}.
    Pour terminer le projet dans ces délais, les durées de toutes les tâches parallèles au tâches critiques doivent pouvoir être réduites
    à la même durée que celle des tâches critiques, et aucune tâche ne doit prendre du retard."""


        output+="\\subsection{Dates de référence pour chaque tâche}"

        output+="""Commencons par le plus important. Chaque tâche du chemin critique ne doit pas prendre de
    retard, car cela entrainerait un retard global du projet.
    Chaque tâche possède trois dates de référence : La date de début au plus tôt,
    fin au plus tôt, fin au plus tard.
    Voici le tableau récapitulatif des dates de référence pour votre projet :\\newline \n"""

        #On écrit le tableau des dates en LaTeX
        output+="""\\begin{tabular}{ |p{3cm}||p{3cm}|p{3cm}|p{3cm}|  }
        \\hline
        \\multicolumn{4}{|c|}{Dates de références} \\\\
        \\hline 
        Tâche&Début au plus tôt&Fin au plus tôt&Fin au plus tard \\\\ 
        \\hline \n"""

        for tache in dates.keys():
            if tache=='D':
                output+=f" {graphe_taches.noeuds[tache]}&T0&T0+{round(dates[tache][1])}&T0+{round(dates[tache][2])} \\\\ \n"
            else:
                output+=f" {graphe_taches.noeuds[tache]}&T0+{round(dates[tache][0])}&T0+{round(dates[tache][1])}&T0+{round(dates[tache][2])} \\\\ \n"
        
        output+="""\\hline
    \\end{tabular} \n"""
    output+="\\end{document}"

    print("LaTeX généré.")
    
    
   #Ecriture des résultats
   
    print("Ecriture des résultats...")
   #Si nécéssaire, on crée les dossiers manquants grace au module os.
    if i==0:
        dir=f"Historique_{nom_projet}"
        if not(os.path.exists(f"./Analyses/{dir}") and os.path.isdir(f"./Analyses/{dir}")):
            os.makedirs(f"./Analyses/{dir}")
        nom_analyse="Analyse_Initiale"
    else:
        nom_analyse=f"Compte_Rendu_Execution_{i}"
    
    
    if not(os.path.exists(f"./Analyses/{dir}/{nom_analyse}") and os.path.isdir(f"./Analyses/{dir}/{nom_analyse}")):
        os.mkdir(f"./Analyses/{dir}/{nom_analyse}")
        
    #On écrit dans le fichier de sortie.
    with open(f"Analyses\\{dir}\\{nom_analyse}\\{nom_analyse}.tex","w", encoding="utf-8") as fichier_sortie:
        fichier_sortie.write(output) 
        "Ecriture terminée."
    i+=1

#Fin
exit=input("""Analyse correctement effectuée.\n
Appuyez sur Entrée pour quitter.""")
print("Merci d'avoir utilisé PERT-Maker !")
time.sleep(1)
sys.exit()