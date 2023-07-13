import pandas as pd
from model_data.goal import Goal
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



rep = GoalRepository()
rep.insert(list_goal)
print("The content of the file is:\n", list_goal)