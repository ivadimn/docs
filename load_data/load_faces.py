import pandas as pd
from typing import List
from repositories.face_repository import FaceRepository
from model_data.face import Face
from settings import birthday_format


class LoadFaces:
    def __init__(self, filename: str):
        self.faces: List[Face] = list()
        self.__load_faces(filename)

    def __load_faces(self, filename: str):
        excel_data = pd.read_excel(filename)
        data = pd.DataFrame(excel_data)
        for val in data.values:
            self.faces.append(Face(0, val[0], val[1], val[2].strftime(birthday_format), val[3], val[4], val[5], val[6]))

    def update_db_faces(self):
        print("Now updating list faces ...")
        rep = FaceRepository()
        rep.insert(self.faces)
        print("Update list faces was finished!")





