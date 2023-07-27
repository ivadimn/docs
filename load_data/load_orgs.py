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
        tmp_line = {"code": "", "name": "", "parent_code": ""}
        for val in data.values:
            if pd.notna(val[0]):
                continue
            if pd.isna(val[1]):
                tmp_line["code"] = "1"
                tmp_line["name"] = "РУКОВОДСТВО"
            elif val[1] == "Аппарат Правления":





            code_word = None if pd.isna(val[2]) else val[2]
            if pd.notna(val[0]):
                parent_id = val[0]
                self.deps.append(Org(val[0], Org.extract_code(val[1]), val[1], code_word, None, ""))
            else:
                self.deps.append(Org(0, Org.extract_code(val[1]), val[1], val[2], parent_id, ""))
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
        return org

    def __clear_tmp_Line(self, tmp: dict):
        tmp["code"] = ""
        tmp["name"] = ""
        tmp["parent_code"] = ""

    def load_orgs(self):
        rep = OrgRepository()
        self.orgs = rep.select()
        for dep in self.deps:
            if dep in self.orgs:
                continue
            if dep.id != 0:
                rid = rep.insert([dep])
            else:
                code_parent = Org.get_parent_code(dep.code)
                parent_org = rep.select_by_code(code_parent)
                dep.parent_id = parent_org.id
                rep.insert([dep])

    def first_load(self):
        rep = OrgRepository()
        parent_id = 0
        for dep in self.deps:
            if dep.id != 0:
                parent_id = rep.insert([dep])
            else:
                dep.parent_id = parent_id
                rep.insert([dep])
