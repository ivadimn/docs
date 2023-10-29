import sqlite3 as sql3
from settings import db_params


class Connection:
    #_instance = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,  "instance"):
            cls.instance = super().__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        # self.connection = QSqlDatabase.addDatabase("QSQLITE")
        # self.connection.setDatabaseName(db_params["dbname"])
        # ok = self.connection.open()
        if not hasattr(self, "connection"):
            self.connection = sql3.connect(db_params["dbname"])
            if self.connection:
                print("Connection successed!")
            else:
                print("Connection failed!")

    def __del__(self):
        if self.connection:
            self.connection.close()
