from csv_to_graphe import*

def verification_format_fichier(nom_fichier):
    nombre_tache_finale=0
    taches=[]
    fichier=from_csv(nom_fichier)
    fichier.pop(0)
    if len(fichier[0])!=7:
        return False, "Le fichier ne comporte pas 7 colonnes"
    for ligne in fichier:
        if ligne[0] in taches:
            return False, 'Il y a 2 fois la même tache '+ligne[0]+ ' aux lignes ' + str(taches.index(ligne[0])+2) + ' et ' +str(fichier.index(ligne)+2)
        else:
            taches.append(ligne[0])
        if ligne[2]=='':
            return False, "La tache "+str(ligne[0]) + str(ligne[1]) + " ne comporte pas de durée à la ligne " +str(fichier.index(ligne)+2)
        if ligne[0]=='F':
            nombre_tache_finale+=1
            if nombre_tache_finale>1:
                return False, "Cette organisation prévois plusieurs taches finales"
        try:
            colonne_erreur="Duree"
            conversion_unite(ligne[2])
            for i in range(4,7):
                if ligne[i]!='':
                    colonne_erreur="S"+str(i-4)
                    conversion_unite(ligne[i])
        except UniteError:
            return False, "Il y a un problème d'unité à la ligne "+str(fichier.index(ligne)+2)+" dans la colonne "+ colonne_erreur    
    if nombre_tache_finale==0:
        return False, "Cette organisation ne prévois pas de tache finale"
    
    return True, "Tout va bien"


print(verification_format_fichier("test"))