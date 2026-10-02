import random
from typing import Any,Callable
import json
type Data = dict [str,Any]
type ExportFn = Callable[[Data],None]



class Dionica:
    
    def __init__(self,id_dionice,ime,cijena):
        self.id_dionice=id_dionice
        self.ime=ime
        self.cijena=float(cijena)

    def __str__(self):
        return f"Cijena {self.ime} dionice je {self.cijena}"

    def __repr__(self):
        return f"Dionica: (ime={self.ime}), (cijena={self.cijena}, tip={type(self.cijena)})"

    def dobar_dan(self):
        faktor=random.uniform(0,10)
        self.cijena+=self.cijena*faktor/100

    def los_dan(self):
        faktor=random.uniform(-10,0)
        self.cijena+=self.cijena*faktor/100

    def neutralan_dan(self):
        faktor=random.uniform(-10,10)
        self.cijena+=self.cijena*faktor/100
        
    exporters: dict[str,ExportFn] = {
        "dobar": dobar_dan,
        "los": los_dan,
        "neutralan": neutralan_dan,}
    
    def simuliraj(self,uvjet):
        exporter =  self.exporters.get(uvjet)
        if exporter is None:
            raise ValueError(f"Nema exportera za uvjet {uvjet}")
        self=exporter(self)
