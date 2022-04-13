"""
Created on Tue July 31 2021

bot link: http://t.me/yakkasaroy_saylov_bot 

@author: jamshid
"""

from docx import Document
from db_helper import VotersDBHelper

document = Document('yakkasaroy2021-voters.docx')
table = document.tables[0]

data = []
from const import VOTERS_DB_NAME
db = VotersDBHelper(VOTERS_DB_NAME)

keys = None
for i, row in enumerate(table.rows):
    text = (cell.text for cell in row.cells)
    # print(text)
    if i == 0:
        keys = tuple(text)
        continue
    row_data = dict(zip(keys, text))
    # print(row_data)
    my_list = []
    for item in row_data:
        my_list.append(row_data[item])
    print(my_list)
    db.set_voters(tuple(my_list))
    


"""
https://www.geeksforgeeks.org/how-to-import-csv-file-in-sqlite-database-using-python/
https://www.tutorialspoint.com/sqlite/sqlite_python.htm

"""