class Db:

    @classmethod
    def select(cls, sql: str, params: tuple) -> list:
        with sqlite3.connect("lna.db") as conn:
            if len(params) > 0:
                cursor = conn.execute(sql, params)
            else:
                cursor = conn.execute(sql)
        return cursor.fetchall()

    @classmethod
    def insert(cls, sql: str, params: list) -> int:
        with sqlite3.connect("lna.db") as conn:
            if len(params) > 0:
                for ps in params:
                    cursor = conn.execute(sql, ps)
            else:
                cursor = conn.execute(sql)
        return cursor.lastrowid

    @classmethod
    def delete(cls, sql: str, params: list) -> int:
        with sqlite3.connect("lna.db") as conn:
            if len(params) > 0:
                for ps in params:
                    cursor = conn.execute(sql, ps)
            else:
                cursor = conn.execute(sql)
        return 1

class Param:
    def __init__(self, table: str, filed: str, op: str):
        self.table = table
        self.field = filed
        self.op = op

    def __str__(self):
        return "{0}.{1}{2}?".format(self.table, self.field, self.op)