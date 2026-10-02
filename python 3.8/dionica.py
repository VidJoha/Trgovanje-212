import random
from typing import Any,Callable
import json
type Data = dict [str,Any]
type ExportFn = Callable[[Data],None]



class Dionica:
    
    def __init__(self,ime,cijena):
        self.ime=ime
        self.cijena=cijena
        self.povijestCijene=[cijena]

    def opisi(self):
        print(f"Cijena {self.ime} dionice je {self.cijena}")

    def dobar_dan(self):
        granica=random.uniform(1,10)
        faktor=random.uniform(0,granica)
        self.cijena+=self.cijena*faktor

    def los_dan(self):
        granica=random.uniform(-10,-1)
        faktor=radnint(granica,0)
        self.cijena-=self.cijena*faktor

    def nuetralan_dan(self):
        granica=random.uniform(-10,-1)
        faktor=radnint(granica,0)
        self.cijena-=self.cijena*faktor
        
    exporters: dict[str,ExportFn] = {
        "dobar": dobar_dan,
        "los": los_dan,
        "neutralan": nuetralan_dan,}
    
    def simuliraj(self,uvjet):
        exporter =  exporters.get(uvjet)
        if exporter is None:
            raise ValueError(f"Nema exportera za uvjet {uvjet}")
        exporter(uvjet)

        
