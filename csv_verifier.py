from csv_to_graphe import*

def verification_format_fichier(fichier):
    """Fonction qui verifie si le fichier CSV est au bon format selon la notice d'utilisation

    Args:
        fichier (list): la liste obtenue après l'execution du programme from_csv

    Returns:
        bool: Si le fachier est valide (True <=> le fichier est valide)
        str: Message d'erreur ou de validation
    """
    nombre_tache_finale=0 #Compteur de tache finale
    taches=[] #Listes des taches
    
    fichier.pop(0) #On enlève le premier terlme de la liste qui correspond aux informations
    if len(fichier[0])!=7:
        return False, "Le fichier ne comporte pas les colonnes nécéssaires"
    for ligne in fichier: #Pour chaque ligne
        if ligne[0] in taches: #Si la tache de la ligne est deja dans la liste des taches
            return False, 'Il y a 2 fois la même tâche '+ligne[0]+ ' aux lignes ' + str(taches.index(ligne[0])+2) + ' et ' +str(fichier.index(ligne)+2)
        else: #Sinon
            taches.append(ligne[0]) #On rajoute la tache a la liste
        if ligne[2]=='': #Si la tache n'a pas de duree
            return False, "La tâche "+str(ligne[0]) + str(ligne[1]) + " ne comporte pas de durée à la ligne " +str(fichier.index(ligne)+2)
        if ligne[0]=='F': #Si la tache est finale
            nombre_tache_finale+=1 #On rajoute un au compteur de tache finale
            if nombre_tache_finale>1: #Si il y a plus d'une tache finale
                return False, "Cette organisation prévoit plusieurs tâches finales"
        try: #On essaie 
            colonne_erreur="Duree" #L'erreur si elle à lieu est sur la colonne de la duree
            conversion_unite(ligne[2]) #De convertir la duree de la colonne duree
            for i in range(4,7): #Pour chaque suivi
                if ligne[i]!='':  #Si il y a un suivi
                    colonne_erreur="S"+str(i-4) #L'erreur si elle à lieu est sur la colonne du suivi
                    conversion_unite(ligne[i]) #Conversion de l'unite du suivi
        except UniteError: #Si il y a une erreur d'unite dans une des colonne essaye
            return False, "Unité erronée à la ligne "+str(fichier.index(ligne)+2)+" dans la colonne "+ colonne_erreur 
    if nombre_tache_finale==0: #Si il n'y à pas de tache finale
        return False, "Cette organisation ne prévoit pas de tache finale"
    
    return True,"Fichier valide"