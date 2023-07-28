import pandas as pd
from typing import List
from repositories.org_repository import OrgRepository
from model_data.org import Org, OrgForLoading
from pprint import pprint


class LoadOrgs:

    def __init__(self, file_name: str):
        self.deps: List[OrgForLoading] = list()
        self.orgs = list()
        self.__load_deps(file_name)                     # из файла

    def __load_deps(self, file_name: str):
        excel_data = pd.read_excel(file_name)
        data = pd.DataFrame(excel_data)
        org = OrgForLoading("", "", "")
        for val in data.values:
            #print([elem for elem in val])
            if pd.notna(val[0]) or self.__is_empty_Line(val):
                continue
            org = self.__analyze_line(val)
            if org.is_empty():
                continue
            if org not in self.deps:
                self.deps.append(org)
        pprint(self.deps)

    def __analyze_line(self, val) -> OrgForLoading:
        org = OrgForLoading("", "", "")
        if pd.isna(val[1]):
            org.code = "1"
            org.name = "РУКОВОДСТВО"
            return org
        if val[1] == "Аппарат Правления":
            org.code = "200"
            org.name = "Аппарат Правления".upper()
        else:
            org.code = Org.extract_code(val[1])
            org.name = val[1]
        if pd.notna(val[2]):
            org.code = Org.extract_code(val[2])
            org.name = val[2]
            org.parent_code = Org.get_parent_code(org.code)
        if pd.notna(val[3]):
            org.code = Org.extract_code(val[3])
            org.name = val[3]
            org.parent_code = Org.get_parent_code(org.code)
        return org

    def __is_empty_Line(self, vals) -> bool:
        return all([pd.isna(val) for val in vals])

    def load_orgs(self):
        rep = OrgRepository()
        self.orgs = rep.select()
        for dep in self.deps:
            lorg = Org(0, dep.code, dep.name, None, "")
            if lorg in self.orgs:
                continue
            if dep.parent_code == "":
                rid = rep.insert([lorg])
            else:
                parent_org = rep.select_by_code(dep.parent_code)
                lorg.parent_id = parent_org.id
                rep.insert([lorg])

    def first_load(self):
        rep = OrgRepository()
        parent_id = 0
        for dep in self.deps:
            if dep.id != 0:
                parent_id = rep.insert([dep])
            else:
                dep.parent_id = parent_id
                rep.insert([dep])
