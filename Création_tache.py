from __future__ import annotations 

Class Tache :
    def __init__(self,duree,précédence,execution,date_fin,critique):
        self.duree = duree 
        self.pre = précédence
        self.exe = execution
        self.fin = date_fin
        self.cri=critique
        

import csv
def to_csv(namecsvfile:str,fieldnames:list[str] ,rows : list[list [str]])−>None :
    with open (name_csv_file+ '.csv','w', encoding="utf_8") as csvfile :
        csvwriter = csv.writer(csvfile,delimiter=',',quoting=csv.QUOTE_ALL)
        csvwriter.writerow(fieldnames)
        for r in rows:
            csvwriter.writerow(r)
            
            