import sqlite3 as sql3
from db.connection import Connection


class Db:

    @classmethod
    def select(cls, sql: str, params: tuple = None) -> sql3.Cursor:
        cursor = Connection().connection.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        return cursor

    @classmethod
    def insert(cls, sql: str, params: tuple):
        conn = Connection().connection
        cursor = conn.cursor()
        if len(params) > 0:
            cursor.execute(sql, params)
            conn.commit()
        else:
            cursor.execute(sql)
            conn.commit()
        return cursor.lastrowid

    @classmethod
    def update(cls, sql: str, params: list) -> int:
        conn = Connection().connection
        cursor = conn.cursor()
        if len(params) > 0:
            cursor.executemany(sql, params)
            conn.commit()
        else:
            cursor.execute(sql)
            conn.commit()
        return cursor.lastrowid


class Param:
    def __init__(self, table: str, filed: str, op: str):
        self.table = table
        self.field = filed
        self.op = op

    def __str__(self):
        return "{0}.{1}{2}?".format(self.table, self.field, self.op)