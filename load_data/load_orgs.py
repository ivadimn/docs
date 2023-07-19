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


class LoadOrgs:

    def __init__(self, file_name: str):
        self.deps = list()
        self.orgs = list()
        self.__load_deps(file_name)

    def __load_deps(self, file_name: str):
        excel_data = pd.read_excel(file_name)
        data = pd.DataFrame(excel_data)
        for val in data.values:
            self.deps.append((val[0], val[1], val[2],))
        print(self.deps)

    def __load_orgs(self):
        rep = OrgRepository()

    def first_load(self):
        rep = OrgRepository()
        created_at = date.today().strftime(date_format)
        parent_id = 0
        for elem in self.deps:
            code_word = None if pd.isna(elem[2]) else elem[2]
            if pd.notna(elem[0]):
                org = Org(0, Org.extract_code(elem[1]), elem[1], code_word, None, created_at, None)
                parent_id = rep.insert([org])
            else:
                org = Org(0, Org.extract_code(elem[1]), elem[1], code_word, parent_id, created_at, None)
                rep.insert([org])
