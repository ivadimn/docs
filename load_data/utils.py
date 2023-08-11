from typing import List, Optional
from model_data.sap_data import SapData
from model_data.dep import Dep
from model_data.org import Org


def extract_org_list(sap: List[str]) -> List[Dep]:
    local_deps = list(set(sap))
    local_deps = list(filter(lambda s: type(s) == str, local_deps))
    org_list: List[Dep] = list()
    for dep in local_deps:
        code = extract_code(dep)
        parent_code = extract_parent_code(code)
        org_list.append(Dep(0, code, dep, parent_code))
    return org_list


def extract_code(name: str) -> str:
    if name.upper() == "РУКОВОДСТВО":
        code = "1"
    elif name.upper() == "АППАРАТ ПРАВЛЕНИЯ":
        code = "200"
    else:
        nc = name.strip().split(" ")
        if len(nc) == 1:
            code = nc[0]
        else:
            code = nc[-1]
    return code


def extract_parent_code(p_code: str) -> str:
    cl = p_code.strip().split("/")
    p_code: Optional[str] = None
    if len(cl) > 1:
        p_code = "/".join(cl[:-1])
    return p_code
