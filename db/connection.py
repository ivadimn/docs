from PyQt6.QtSql import QSqlDatabase
from settings import db_params


class Connection:

    _instance: ["Connection"] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.connection = QSqlDatabase.addDatabase("QPSQL")
        self.connection.setHostName(db_params["host"])
        self.connection.setDatabaseName(db_params["dbname"])
        self.connection.setPort(db_params["port"])
        self.connection.setUserName(db_params["user"])
        self.connection.setPassword(db_params["password"])
        ok = self.connection.open()
        if ok:
            print("Connection successed!")
        else:
            print("Connection failed!")

    def __del__(self):
        if self.connection:
            self.connection.close()