from pandas import isna, notna
from pandas.core.frame import DataFrame
from typing import List
from repositories.org_repository import OrgRepository
from model_data.org import Org, OrgForLoading
from pprint import pprint


class LoadOrgs:

    def __init__(self, data: DataFrame):
        self.raw_orgs: List[OrgForLoading] = list()
        self.data = data
        self.orgs: List[Org] = list()
        self.__load_deps()

# анализ файла производиться по колонкам
    def __load_deps(self):
        for index in range(self.data.shape[1]):
            self.__analyze_column(index)

    def __analyze_column(self, index: int):
        org = OrgForLoading("", "", "")
        for val in self.data.values:
            org.clear()
            if self.__is_empty_Line(val):
                org.name = "Руководство"
            elif isna(val[index]):
                continue
            else:
                org.name = val[index]
            if org.name == "Руководство":
                org.code = "1"
            elif org.name == "Аппарат Правления":
                org.code = "200"
            else:
                org.code = Org.extract_code(org.name)
            if index == 0:
                org.parent_name = ""
            elif index == 1:
                org.parent_name = val[index - 1]
            else:
                org.parent_name = val[index - 1] if notna(val[index-1]) else val[index - 2]

            self.__append_to_dep(org)

    def __append_to_dep(self, org: OrgForLoading):
        if org not in self.raw_orgs:
            add_org = OrgForLoading(org.code, org.name, org.parent_name)
            self.raw_orgs.append(add_org)

    def __is_empty_Line(self, vals) -> bool:
        result = all([isna(val) for val in vals])       # or (pd.notna(vals[0]))
        return result

    def load_orgs(self):
        rep = OrgRepository()
        self.orgs = rep.select()
        for dep in self.raw_orgs:
            lorg = Org(0, dep.code, dep.name, None, "")
            if lorg in self.orgs:
                continue
            if dep.parent_name == "":
                pk = rep.insert([lorg])
            else:
                parent_org = rep.select_by_name(dep.parent_name)
                lorg.parent_id = parent_org.pk
                rep.insert([lorg])

# добавить фуйкцию анализ структуры для закрытия
# закрывается единица и все дочерние узлы и привязка к должностмя