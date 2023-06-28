import pandas as pd
from model_data.pd import Pd
from model_data.category import Category
from model_data.goal import Goal
from repositories.pd_repository import PdRepository
from repositories.category_repository import CategoryRepository
from repositories.goal_repository import GoalRepository
from db.connection import Connection
import openpyxl

conn = Connection()
# excel_data = pd.read_excel('./Data/pd.xlsx')
# data = pd.DataFrame(excel_data)
# list_pd = []
# for val in data.values:
#     list_pd.append(Pd(0, val[0], None))
#
# rep = PdRepository()
# rep.insert(list_pd)


#print("The content of the file is:\n", list_pd)


excel_data = pd.read_excel('./Data/goals.xlsx')
data = pd.DataFrame(excel_data)
list_goal = []
for val in data.values:
    list_goal.append(Goal(0, val[0], val[1]))

rep = GoalRepository()
rep.insert(list_goal)
print("The content of the file is:\n", list_goal)