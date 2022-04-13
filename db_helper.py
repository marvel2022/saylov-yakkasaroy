"""
Created on Tue July 31 2021

bot link: http://t.me/yakkasaroy_saylov_bot 

@author: jamshid

sqlite with python3 connection: https://www.tutorialspoint.com/sqlite/sqlite_python.htm
"""

import sqlite3


class StationsDBHelper:

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def get_stations(self):
        return self.cursor.execute('select id, number from stations order by number').fetchall()

    def get_station_by_id(self, station_id):
        return self.cursor.execute('select * from stations where id=?', (station_id,)).fetchone()
    
    def get_station_by_pasport(self, pasport_data):
        return self.cursor.execute('select * from voters where pasport_data=?', (pasport_data,)).fetchone()
    
    def set_station(self, record):
        # print(len(record))
        self.cursor.execute(
            "INSERT INTO stations(number,sector,number_voters,name_mfy,building,"
            "building_address,cadastre,chairman,phone_ch,position_ch,assistant,"
            "phone_a,position_a,secretary,phone_s,position_s,latitude,longitude) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", 
            (
                int(record[0]),int(record[1]), int(record[2]),
                record[3],record[4],record[5],record[6],record[7],record[8],record[9],record[10],record[11],record[12],record[13],record[14],record[15],
                record[16], record[17],
            )
        )
        self.conn.commit()



class VotersDBHelper:

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
    
    def get_voter_by_pasport(self, pasport_data):
        print(pasport_data)
        for db_number in range(543, 578):
            try:
                voter=self.cursor.execute(f'select * from station{db_number} where passport=?', (pasport_data,)).fetchone()
            except:
                voter=None
            if voter is not None:
                break
        # voter=self.cursor.execute('select * from station544 where passport=?', (pasport_data,)).fetchone()
        # try:
        #     voter=self.cursor.execute(f'select * from 544 where passport=?', (pasport_data,)).fetchone()
        # except:
        #     voter=None
        return voter
    
    def set_voters(self, record):
        self.cursor.execute(
            "INSERT INTO voters(pasport, voter_fish, polling_station, polling_station_number) VALUES (?,?,?,?)", (record[0], record[1], record[2], int(record[3]))
        )
        self.conn.commit()

       
"""

id,
number,
sector,
number_voters,
name_mfy,
building,
building_address,
cadastre,
chairman,
phone_ch,
position_ch,
assistant,
phone_a,
position_a,
secretary,
phone_s,
position_s,
latitude,
longitude,

"""

