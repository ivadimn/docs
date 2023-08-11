import pandas as pd
from model_data.sap_data import SapData
from model_data.org import Org
from typing import List
from model_data.face import Face
from settings import birthday_format
from .utils import  extract_org_list
from pprint import pprint


class ImportData:

    def __init__(self, filename: str):
        self.sap_data: List[SapData] = list()
        self.__load_data(filename)

    def __load_data(self, filename: str):
        excel_data = pd.read_excel(filename)
        data = pd.DataFrame(excel_data)
        data_orgs = data.iloc[:, [6, 7, 8]]
        print(data_orgs)
        # for val in data.values:
        #     self.sap_data.append(SapData(0, val[0], val[1], val[2].strftime(birthday_format),
        #                                  val[3], val[4], val[5],
        #                                  val[6] if pd.notna(val[6]) else "Руководство",
        #                                  val[7], val[8]))
        # self.prepare_orgs()

    def prepare_orgs(self):
        orgs = extract_org_list([sap.dep for sap in self.sap_data])
        uprs = extract_org_list([sap.upr for sap in self.sap_data])
        otdels =  extract_org_list([sap.otdel for sap in self.sap_data])
        for org in orgs:
            code = org.code
            childs1 = list(filter(lambda s: s.parent_code == code, uprs))
            childs2 = list(filter(lambda s: s.parent_code == code, otdels))
            if len(childs1) > 0 or len(childs2) > 0:
                org.childs = childs1 + childs2
                for child in org.childs:
                    code = child.code
                    childs3 = list(filter(lambda s: s.parent_code == code, otdels))
                    if len(childs3) > 0:
                        child.childs = childs3
        pprint(orgs)
