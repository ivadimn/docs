from pandas.core.frame import DataFrame
from pandas import notna
from typing import List
from repositories.face_repository import FaceRepository
from repositories.org_repository import OrgRepository
from model_data.face import Face
from pprint import pprint
from settings import birthday_format


class LoadFaces:
    def __init__(self, data: DataFrame):
        self.orgs = dict()
        self.data = data
        self.__load_faces()

    def __load_faces(self):
        for val in self.data.values:
            if notna(val[8]):
                org_name = val[8]
            elif notna(val[7]):
                org_name = val[7]
            elif notna(val[6]):
                org_name = val[6]
            else:
                org_name = "Руководство"
            if self.orgs.get(org_name) is None:
                self.orgs[org_name] = []

            self.orgs[org_name].append(Face(0, val[0], val[1], val[2].strftime(birthday_format),
                                            (val[3], val[4], val[5])))
            print(self.orgs)

    def update_db_faces(self):
        print("Now updating list faces ...")
        rep = FaceRepository()
        ex_faces = rep.select()
        rep_org = OrgRepository()
        for key, val in self.orgs:
            org_id = rep_org.select_by_name(key).pk
            for face in val:
                if face not in ex_faces:
                    rep.insert([face], org_id)

        print("Update list faces was finished!")





