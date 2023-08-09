import pandas as pd
from typing import List
from repositories.dep_repository import DepRepository
from model_data.dep import Dep
from pprint import pprint


class LoadSimple:

    def __init__(self, file_name: str):
        self.deps: List[Dep] = list()
        self.__load_deps(file_name)

    def __load_deps(self, file_name: str):
        excel_data = pd.read_excel(file_name)
        data = pd.DataFrame(excel_data)
        for val in data.values:
            if pd.isna(val[0]):
                continue
            dep = Dep(name=val[1])
            if dep.name.upper() == "РУКОВОДСТВО":
                dep.code = "1"
            elif dep.name.upper() == "АППАРАТ ПРАВЛЕНИЯ":
                dep.code = "200"
            else:
                dep.extract_code()
            self.deps.append(dep)
        pprint(self.deps)

    def update_db_deps(self):
        rep = DepRepository()
        orgs = rep.select()
        for dep in self.deps:
            if dep not in orgs:
                rep.insert([dep])
        for org in orgs:
            if org not in self.deps:
                rep.delete({"pk": org.pk})
