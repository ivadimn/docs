import pandas as pd
from model_data.goal import Goal
from model_data.org import Org
from repositories.goal_repository import GoalRepository
from db.connection import Connection


def load_deps(file_name: str):
    excel_data = pd.read_excel(file_name)
    data = pd.DataFrame(excel_data)
    list_deps = []
    for val in data.values:
        print(val[0], val[1])
