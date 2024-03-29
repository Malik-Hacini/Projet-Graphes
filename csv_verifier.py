from csv_to_graphe import*

def verification_format_fichier(fichier):
    """Vérfie qu'un fichier CSV est au format prévu par le manuel d'utilisation.

    Args:
        fichier (list): la liste des données du fichier obtenue après l'execution du programme from_csv

    Returns:
        bool: True <=> le fichier est valide
        str: Message d'erreur ou de validation
    """
    taches=[] #Listes des tâches
    
    fichier.pop(0) #On enlève le premier terme de la liste qui correspond aux informations
    if len(fichier[0])!=7:
        return False, "Le fichier ne comporte pas les colonnes nécéssaires"
    for ligne in fichier: #Pour chaque ligne
        if ligne[0] in taches: #Si la tâche de la ligne est déjà dans la liste des tâches
            return False, 'Il y a 2 fois la même tâche '+ligne[0]+ ' aux lignes ' + str(taches.index(ligne[0])+2) + ' et ' +str(fichier.index(ligne)+2)
        else: #Sinon
            taches.append(ligne[0]) #On rajoute la tâche a la liste
        if ligne[2]=='': #Si la tâche n'a pas de durée
            return False, "La tâche "+str(ligne[0]) + str(ligne[1]) + " n'a pas de durée indiquée à la ligne " +str(fichier.index(ligne)+2)

        try: #On essaie 
            colonne_erreur="Duree" #L'erreur si elle à lieu est sur la colonne de la durée
            conversion_unite(ligne[2]) 
            for i in range(4,7): #Pour chaque compte rendu d'éxécution
                if ligne[i]!='':  #Si il y a des informations pour le cr_exec
                    colonne_erreur="S"+str(i-4) #L'erreur si elle à lieu est sur la colonne du cr_exec
                    conversion_unite(ligne[i]) #Conversion de l'unite du cr_exec
        except UniteError: #Si il y a une erreur d'unite dans une des colonne essaye
            return False, "Unité erronée à la ligne "+str(fichier.index(ligne)+2)+" dans la colonne "+ colonne_erreur 
    
    return True,"Fichier valide."