def gen_select(cls: type, table: str) -> list:
    fields = cls.__dict__.get("__dataclass_fields__")
    sql = list()
    sql.append("SELECT")
    for fk in fields.keys():
        sql.append("{0}.{1}".format(table, fk))
        sql.append(",")
    sql.pop()
    sql.append("FROM {0}".format(table))
    return sql


def gen_select_all(cls: type, table: str) -> str:
    sql = gen_select(cls, table)
    return " ".join(sql)


def gen_select_by_id(cls: type, table: str, key: str) -> str:
    sql = gen_select(cls, table)
    sql.append("WHERE {0}.{1} = ?".format(table, key))
    return " ".join(sql)


def gen_select_by_like(cls: type, table: str, key: str) -> str:
    sql = gen_select(cls, table)
    sql.append("WHERE {0}.{1} LIKE ?".format(table, key))
    return " ".join(sql)


def gen_insert(cls: type, table: str, autoincrement: bool = True) -> str:
    fields = cls.__dict__.get("__dataclass_fields__")
    sql = list()
    sql.append("INSERT INTO {0} (".format(table))
    for fk in fields.keys():
        if autoincrement and fk == "id":
            continue
        sql.append("{0}".format(fk))
        sql.append(",")
    sql.pop()
    sql.append(") VALUES (")
    for fk in fields.keys():
        if autoincrement and fk == "id":
            continue
        sql.append("?")
        sql.append(",")
    sql.pop()
    sql.append(")")
    return " ".join(sql)


def gen_delete_by_id(table: str, key: str) -> str:
    sql = list()
    sql.append("DELETE FROM {0}".format(table))
    sql.append("WHERE {0}.{1} = ?".format(table, key))
    return " ".join(sql)
