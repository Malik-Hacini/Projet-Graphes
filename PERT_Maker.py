import sys
import time
import os
from Graphes import*
from csv_to_graphe import*
from csv_verifier import*
from cycle_detector import*
from chemins_critiques import*
from graphe_to_latex import*

"""Ce fichier est le logiciel en lui même. C'est lui qu'on compile en éxécutable. L'utilisateur indique quel fichier analyse, on en crée le graphe,
On l'analyse, et on écrit les analyses en LaTeX dans des fichiers .tex, situées dans le dossier historique du projet.
"""
def initialisation_fichier_projet()->list:
    """Demande à l'utilisateur quel fichier analyser parmi la liste des fichiers disponibles, tout en vérifiant son format.
    S'appuie sur la fonction verification_format_fichier. 
     
    Returns: nom_projet (str),infos_projet (list) : Les informations du fichier projet à analyser
    """
    #On extrait et affiche les fichiers projets disponibles
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

    #On demande le nom du projet à l'utilisateur et on vérifie le format.
    fichier_valide=False
    while not fichier_valide:
        nom_projet=input("Veuillez entrer le nom du fichier du projet à analyser : \n")
        try:
            infos_projet=from_csv(f"Projets\\{nom_projet}")
        except OSError:
            print("Fichier introuvable.")
            continue
        
        verif=verification_format_fichier(infos_projet)
        print(verif[1]) #On affiche le message d'erreur
        if not verif[0]:
            print("Veuillez vous référer au manuel d'utilisation.")
        else:
            fichier_valide=True  
    return nom_projet

def tri_infos_fichier(nombre_analyses: int)->list:
    """Demande à un utilisateur quelles analyses mener sur son fichier projet, 
    selon ce qui est rempli dans le fichier.
    

    Args:
        nombres_analyses (int): le nombre possibles d'analyses différentes.
    Returns:
        infos_a_anlyser
    """
    if nombre_analyses!=1:#Si des suivis sont remplis, on demande à l'utilisateur quoi analyser
        print("Voici les analyses possibles:")
        for i in range(nombre_analyses): #On affiche les analyses possibles du projet à l'utilisateur
            if i==0:
                print("0 - Analyse Initiale")
            else:
                print(f"{i} - Compte Rendu {i}")

        choix_correct=False
        while not choix_correct: #On vérifie le choix, et on renvoie l'erreur adaptée si besoin.
            choix_correct=True
            
            choix=input("Que séléctionnez vous d'analyser ? Entrez tout les choix séparés d'un espace (ex: 0 1)\n").split()
            if choix==[]:
                print("Séléction vide.")
                choix_correct=False
                continue
            elif len(choix)>nombre_analyses:
                print("Séléction trop grande.")
                choix_correct=False
                continue
            for i in choix:
                try:
                    assert len(i)==1 #Pour rendre "000" invalide, car int(000)=0
                    i=int(i)
                except:
                    print(f"{i} n'est pas un entier valide.")
                    choix_correct=False
                    continue
                if i not in list(range(nombre_analyses)):
                    print(f"{i} n'est pas valide.")
                    choix_correct=False
                    
        infos_a_analyser=[infos_projet[int(i)] for i in choix] 
        
    else:#Sinon, on effectue simplement l'analyse initiale.
            infos_a_analyser=infos_projet
    
    return infos_a_analyser

def analyse_fichier_to_latex(cr_exec):
    num_analyse=infos_projet.index(cr_exec)
    
    if num_analyse==0:
        print(("\nAnalyse Initiale..."))
    else:
        print(f"\nCompe Rendu d'éxécution {num_analyse}...")
        
    #On crée le graphe de tâches.
    noeuds, arcs_ponderes,duree_finale= cr_exec
    graphe_taches=DiGraphe(noeuds,arcs_ponderes)
    
    print("Graphe de tâches créé.")
    print("Analyse du graphe et création du LaTeX en cours...")
    
    code_latex=start_document
    code_latex+="\section{Votre Graphe de tâches}\n"  
      
    #On ajoute la visualisation du graphe à l'analyse.
    cycle=cycle_detector(graphe_taches)
    if cycle:
        #Si le graphe de tâches du projet est cyclique, l'analyse ne peut pas poursuivre.
        code_latex+=graphe_to_latex(graphe_taches)
        code_latex+="\section{Analyse de votre projet}\n"
        code_latex+="Votre projet est infaisable, l'ordonnancement des taches contient une boucle.\n"
        print("Analyse du graphe terminée.")

    else:
        arcs_critiques,noeuds_critiques,dist=chemin_critique(graphe_taches,0,len(graphe_taches.noeuds)-1)
        print(arcs_critiques,noeuds_critiques)
        dates=dates_tot_tard(graphe_taches,duree_finale,noeuds_critiques)
        print("Analyse du graphe terminée.")
        
        code_latex+=graphe_to_latex(graphe_taches,arcs_critiques)
        code_latex+="\section{Analyse de votre projet}\n"
        
    
        code_latex+=f"""Votre projet possède un temps incompressible de {round(duree_finale+dist)} jours.
    Il s'agit de la durée totale du \\textcolor{{red}}{{chemin critique}}.
    Pour terminer le projet dans ces délais, les \\textcolor{{red}}{{tâches critiques}} ne doivent prendre aucun retard."""


        code_latex+="\\subsection{Dates de référence pour chaque tâche}"

        code_latex+="""Chaque tâche du chemin critique ne doit pas prendre de
    retard, car cela entrainerait un retard global du projet. 
    Chaque tâche possède trois dates de référence : La date de début au plus tôt,
    fin au plus tôt, fin au plus tard.
    Attention, chaque tâche du chemin critique ne doit pas prendre de
    retard, car cela entrainerait un retard global du projet. Leurs dates de début au plu
    Voici le tableau récapitulatif des dates de référence pour votre projet :\\newline \n"""

        #On écrit le tableau des dates en LaTeX
        code_latex+="""\\begin{tabular}{ |p{3cm}||p{3cm}|p{3cm}|p{3cm}|  }
        \\hline
        \\multicolumn{4}{|c|}{Dates de références} \\\\
        \\hline 
        Tâche&Début au plus tôt&Fin au plus tôt&Fin au plus tard \\\\ 
        \\hline \n"""

        for index,tache in enumerate(dates.keys()):
            if index==0:
                code_latex+=f" {graphe_taches.noeuds[tache]}&T0&T0+{round(dates[tache][1])}&T0+{round(dates[tache][2])} \\\\ \n"
            else:
                code_latex+=f" {graphe_taches.noeuds[tache]}&T0+{round(dates[tache][0])}&T0+{round(dates[tache][1])}&T0+{round(dates[tache][2])} \\\\ \n"
        
        code_latex+="""\\hline
    \\end{tabular} \n"""
    code_latex+="\\end{document}"

    return num_analyse,code_latex

def ecrire_analyse_dans_document(code_latex,dossier,num_analyse):
    if num_analyse==0:
        nom_analyse="Analyse_Initiale"
    else:
        nom_analyse=f"Compte_Rendu_Execution_{num_analyse}"
    
    
    if not(os.path.exists(f"./Analyses/{dossier}/{nom_analyse}") and os.path.isdir(f"./Analyses/{dossier}/{nom_analyse}")):
        os.mkdir(f"./Analyses/{dossier}/{nom_analyse}")
        
    #On écrit dans le fichier de sortie.
    with open(f"Analyses\\{dossier}\\{nom_analyse}\\{nom_analyse}.tex","w", encoding="utf-8") as fichier_sortie:
        fichier_sortie.write(code_latex) 


nom_projet=initialisation_fichier_projet()
infos_projet=csv_to_graph(f"Projets\\{nom_projet}")
nombre_analyses=len(infos_projet)
infos_a_analyser=tri_infos_fichier(nombre_analyses)
#On initialise le début du document LaTeX d'analyse. Il ne dépend que du nom du projet.
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
\\title{\\centering Peer Review and Evaluation Technique : """ + nom_projet.replace("_"," ").capitalize() +"""
}

\\author{PERT Maker}
\\renewcommand{\contentsname}{Table des Matières}
\\begin{document}
\\maketitle
\\tableofcontents{}\n"""       
    
#On crée le dossier Historique du projet. On y placera les analyses dans leur dossiers respectifs.
dossier=f"Historique_{nom_projet}"
if not(os.path.exists(f"./Analyses/{dossier}") and os.path.isdir(f"./Analyses/{dossier}")):
    os.makedirs(f"./Analyses/{dossier}")

#On analyse le fichier.
for cr_exec in infos_a_analyser:
    num_analyse,code_latex=analyse_fichier_to_latex(cr_exec)
    print("LaTeX généré.") 
    #On écrit les résultats de l'analyse au bon emplacement.
    ecrire_analyse_dans_document(code_latex,dossier,num_analyse)
    print("Document créé.")

#Fin
exit=input("""Analyses correctement effectuées.\n
Merci d'avoir utilisé PERT-Maker !
Appuyez sur Entrée pour quitter.""")
sys.exit()