from hashlib import sha1
from sqlite3 import Error as SqlError
from dataclasses import dataclass
from typing import List
from model_data.entity import Entity
from db.sql import query
from db.db import Db
import logging

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


@dataclass
class Shtat(Entity):
    org_id: int = None
    pos_id: int = None
    tn: int = None
    pd_id: int = None
    created_at: str = None
    closed_at: str = None

    @classmethod
    def select(cls) -> List["Shtat"]:
        shs = list()
        try:
            cursor = Db.select(query["Shtat"]["_SELECT"])
            for sh in cursor:
                shs.append(Shtat(pk=sh[0], org_id=sh[1], pos_id=sh[2], tn=sh[3], pd_id=sh[4]))
        except SqlError as ex:
            LOG.info("Ошибка получения данных штатного расписания: {0}".format(ex.args[0]))
        return shs

    @classmethod
    def select_tmp(cls) -> List["Shtat"]:
        shs = list()
        try:
            cursor = Db.select(query["Shtat"]["_SELECT_TMP"])
            for sh in cursor:
                shs.append(Shtat(org_id=sh[0], pos_id=sh[1], tn=sh[2], pd_id=sh[3]))
        except SqlError as ex:
            LOG.info("Ошибка получения данных штатного расписания: {0}".format(ex.args[0]))
        return shs

    @classmethod
    def load_from_tmp(cls):
        shs = set(cls.select())
        shs_tmp = set(cls.select_tmp())
        dsh = shs_tmp - shs
        if len(dsh) > 0:
            Db.update(query["Shtat"]["_INSERT"], [(sh.org_id, sh.pos_id, sh.tn, sh.pd_id,) for sh in dsh])
        dsclose = (shs - shs_tmp)
        if len(dsclose) > 0:
            Db.update(query["Shtat"]["_CLOSE"], [(sh.pk,) for sh in dsclose])

    @property
    def row(self) -> tuple:
        return self.pk, self.org_id, self.pos_id, self.tn, self.pd_id

    def __eq__(self, other):
        return (self.pk == other.pk and self.org_id == other.org_id
                and self.pos_id == other.pos_id and self.tn == other.tn and self.pd_id == other.pd_id)

    def __hash__(self):
        data = "{0}{1}{2}{3}".format(self.org_id, self.pos_id, self.tn, self.pd_id)
        hash_code = int(sha1(data.encode("utf-8")).hexdigest(), 16)
        return hash_code
