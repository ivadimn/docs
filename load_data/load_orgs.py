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
        length = len(data.values[0])
        for index in range(1, length - 1):
            self.__analyze_column(index, data)
        # for val in data.values:
        #     #print([elem for elem in val])
        #     if pd.notna(val[0]) or self.__is_empty_Line(val):
        #         continue
        #     org = self.__analyze_line(val)
        #     if org.is_empty():
        #         continue
        #     if org not in self.deps:
        #         self.deps.append(org)
        pprint(self.deps)

    def __analyze_column(self, index: int, data):
        org = OrgForLoading("", "", "")
        for val in data.values:
            org.clear()
            if pd.isna(val[index]) or self.__is_empty_Line(val):
                continue
            org.name = val[index]
            if org.name == "Руководство":
                org.code = "1"
            elif org.name == "Аппарат Правления":
                org.code = 200
            else:
                org.code = Org.extract_code(org.name)
            if index == 1:
                org.parent_name = ""
            elif pd.isna(val[index - 1]):
                org.parent_name = val[index - 2]
            else:
                org.parent_name = val[index - 1]
            self.__append_to_dep(org)

    def __append_to_dep(self, org: OrgForLoading):
        if org not in self.deps:
            add_org = OrgForLoading(org.code, org.name, org.parent_name)
            self.deps.append(add_org)

    # def __analyze_line(self, val) -> OrgForLoading:
    #     org = OrgForLoading("", "", "")
    #     if pd.isna(val[1]):
    #         org.code = "1"
    #         org.name = "РУКОВОДСТВО"
    #         return org
    #     if val[1] == "Аппарат Правления":
    #         org.code = "200"
    #         org.name = val[1]
    #     else:
    #         org.code = Org.extract_code(val[1])
    #         org.name = val[1]
    #     if pd.notna(val[2]):
    #         org.code = Org.extract_code(val[2])
    #         org.name = val[2]
    #         org.parent_name = Org.get_parent_code(org.code)
    #     if pd.notna(val[3]):
    #         org.code = Org.extract_code(val[3])
    #         org.name = val[3]
    #         org.parent_code = Org.get_parent_code(org.code)
    #     return org

    def __is_empty_Line(self, vals) -> bool:
        result = all([pd.isna(val) for val in vals]) or (pd.notna(vals[0]))
        return result

    def load_orgs(self):
        rep = OrgRepository()
        self.orgs = rep.select()
        for dep in self.deps:
            lorg = Org(0, dep.code, dep.name, None, "")
            if lorg in self.orgs:
                continue
            if dep.parent_name == "":
                rid = rep.insert([lorg])
            else:
                parent_org = rep.select_by_name(dep.parent_name)
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
