import pandas as pd
from model_data.pd import Pd
from repositories.pd_repository import PdRepository
from db.connection import Connection
import openpyxl

# wookbook = openpyxl.load_workbook("./Data/pd.xlsx")
# worksheet = wookbook.active
# for i in range(0, worksheet.max_row):
#     for col in worksheet.iter_cols(1, worksheet.max_column):
#         print(col[i].value, end="\t\t")
#     print('')

conn = Connection()
excel_data = pd.read_excel('./Data/pd.xlsx')
data = pd.DataFrame(excel_data)
list_pd = []
for val in data.values:
    list_pd.append(Pd(0, val[0], None))

rep = PdRepository()
rep.insert(list_pd)


print("The content of the file is:\n", list_pd)
