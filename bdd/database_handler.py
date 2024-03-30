
# PROFILES

# id : id du l'utilisateur
# tokens : nombre de jetons
# coins : nombre de coins
# messages : nombre de messages envoyé (avant reinitialisation pour gains)
# voice_hours : nombre d'heures en vocal (avant reinitialisation pour gains)
# badges : roles badges gagnés (roleid,roleid,roleid)
# points : points GDC
# rob_availables : nombre de pillages disponibles
# clan : id du clan si fait parti d'un clan

# --------------------------------------------

# TOKENS

# messages : nombre de messages pour obtenir un jeton
# voice_hours : nombre d'heures en vocal pour obtenir un jeton
# status : status a avoir pour etre eligible aux gains status
# status_time : temps a attendre pour gagner un jeton si on a le status
# status_count : nombre de jetons a gagner si on a le status




import os
import sqlite3
import json
from datetime import date

f = open("config.json", "r")
config = json.load(f)
f.close()

class DatabaseHandler():
    def __init__(self, database_name: str):
        self.con = sqlite3.connect(f"{os.path.dirname(os.path.abspath(__file__))}/{database_name}")
        self.con.row_factory = sqlite3.Row

    def add_streamer(self, username, channel, serverid:int):
        cursor = self.con.cursor()
        query = f"INSERT INTO streamers_{serverid}(username,pingchannel,state) VALUES(?,?,?);"
        cursor.execute(query, (username,int(channel),"ok",))
        self.con.commit()
        cursor.close()
        return "ok"
    
    def get_lang(self, serverid:int):
        cursor = self.con.cursor()
        query = f"SELECT lang FROM aservers WHERE id=?;"
        cursor.execute(query, (serverid,))
        data = cursor.fetchone()
        cursor.close()
        return data['lang']
    
    def add_server(self, serverid:int, name:str, member_count:int,lang:str):
        cursor = self.con.cursor()
        query = "INSERT INTO aservers(id,name,member_count,lang) VALUES(?,?,?,?);"
        cursor.execute(query, (serverid,name,member_count,lang,))
        self.con.commit()
        cursor.close()
        return "ok"
    