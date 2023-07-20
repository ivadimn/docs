import pandas as pd
from typing import List
from datetime import datetime
from model_data.goal import Goal
from model_data.org import Org
from repositories.org_repository import OrgRepository
from model_data.org import Org
from db.connection import Connection
from datetime import date
from settings import date_format
from pprint import pprint


class LoadOrgs:

    def __init__(self, file_name: str):
        self.deps = list()
        self.orgs = list()
        self.__load_deps(file_name)                     # из файла

    def __load_deps(self, file_name: str):
        excel_data = pd.read_excel(file_name)
        data = pd.DataFrame(excel_data)
        parent_id = 0
        for val in data.values:
            code_word = None if pd.isna(val[2]) else val[2]
            if pd.notna(val[0]):
                parent_id = val[0]
                self.deps.append(Org(val[0], Org.extract_code(val[1]), val[1], code_word, None, ""))
            else:
                self.deps.append(Org(0, Org.extract_code(val[1]), val[1], val[2], parent_id, ""))
        pprint(self.deps)

    def load_orgs(self):
        rep = OrgRepository()
        self.orgs = rep.select()
        parent_id = 0
        name = ""
        for dep in self.deps:
            if dep.id != 0:
                name = dep.name.upper()
            if dep not in self.orgs:
                if dep.id != 0:
                    parent_id = dep.insert([dep])
                else:
                    parent_org = rep.select_by_name(name)
                    dep.parent_id = parent_org.id
                    parent_id = rep.insert(dep)

    def first_load(self):
        rep = OrgRepository()
        parent_id = 0
        for dep in self.deps:
            if dep.id != 0:
                parent_id = rep.insert([dep])
            else:
                dep.parent_id = parent_id
                rep.insert([dep])
