from csv_to_graphe import*

nom_correct=False
while not nom_correct:
    try:
        nom=input("Quel est le nom du csv de votre projet ?")
        f=open(nom+"csv","r")
        f.close()
        nom_correct=True
    except:
        print("Fichier introuvable ou format incorrect")
        
noeuds, arcs_ponderes= csv_to_graph("Tests\\test_cour")
g=DiGraphe(noeuds,arcs_ponderes)
graphe_to_tex(g)