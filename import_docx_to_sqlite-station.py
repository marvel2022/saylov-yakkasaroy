"""
Created on Tue July 31 2021

bot link: http://t.me/yakkasaroy_saylov_bot 

@author: jamshid
"""

from docx import Document
from db_helper import StationsDBHelper

document = Document('stations-info/station-info.docx')
table = document.tables[0]

data = []
from const import DB_NAME
db = StationsDBHelper(DB_NAME)

keys = None
for i, row in enumerate(table.rows):
    text = (cell.text for cell in row.cells)
    # print(text)
    if i == 0:
        keys = tuple(text)
        continue
    row_data = dict(zip(keys, text))
    my_list = []
    for item in row_data:
        my_list.append(row_data[item])
    my_list[8] = "+998(" + my_list[8][:2]+")"+my_list[8][2:]
    my_list[11] = "+998(" + my_list[11][:2]+")"+my_list[11][2:]
    my_list[14] = "+998(" + my_list[14][:2]+")"+my_list[14][2:]
    db.set_station(tuple(my_list))


"""
https://www.geeksforgeeks.org/how-to-import-csv-file-in-sqlite-database-using-python/
https://www.tutorialspoint.com/sqlite/sqlite_python.html

"""