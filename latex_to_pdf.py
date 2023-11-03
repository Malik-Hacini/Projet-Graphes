import subprocess

def latex_to_pdf(fichier_latex, systeme):
    """fonction qui convertit un latex en pdf qui supprime les fichiers qu l'oon utiise pas qui ont été crée lors de 
    l'execution du latex et quiu ouvre le PDF  

    Args:
        fichier_latex (str): Chemin pour arriver au fichier latex que l'on veut convertir en pdf
        systeme(str): OS du PC (Window Linux ou Mac)
    """
    # Utilisez le module subprocess pour appeler pdflatex et générer le PDF
    subprocess.call(["pdflatex", latex_file])

    # On supprime les fichiers intermédiaires générés par pdflatex
    subprocess.call(["del", f"{latex_file}.log"], shell=True)
    subprocess.call(["del", f"{latex_file}.aux"], shell=True)
    subprocess.call(["del", f"{latex_file}.toc"], shell=True)
    subprocess.call(["del", f"{latex_file}-dot2tex-fig1.dot"], shell=True)
    
    # Le fichier PDF généré aura le même nom que votre fichier LaTeX, mais avec l'extension .pdf
    fichier_pdf = f"{latex_file}.pdf"
    print(f"Le fichier PDF a été généré : {pdf_file}")

    #La commande pour ouvrir un fichier est différente selon le OS
    if systeme=="Window":
        commande="start"
    elif systeme=="Linux":
        commande=="xdg-open"
    elif systeme=="Mac":
        commande=="open"
        
    # Ouvrir le PDF avec le lecteur de PDF par défaut du système (Windows)
    subprocess.call([commannde, pdf_file], shell=True) 