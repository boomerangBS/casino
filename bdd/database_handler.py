
# PROFILES

# id : id du l'utilisateur (not null)
# tokens : nombre de jetons (not null)
# coins : nombre de coins (not null)
# messages : nombre de messages envoyé (avant reinitialisation pour gains) (not null)
# voice_minutes : nombre de minutes en vocal (avant reinitialisation pour gains) (not null)
# badges : roles badges gagnés (roleid,roleid,roleid)
# points : points GDC (not null)
# rob_availables : nombre de pillages disponibles (not null)
# clan : id du clan si fait parti d'un clan

# --------------------------------------------

# TOKENS

# messages : nombre de messages pour obtenir un jeton (not null)
# voice_hours : nombre d'heures en vocal pour obtenir un jeton (not null)
# status : status a avoir pour etre eligible aux gains status (not null)
# status_time : temps a attendre pour gagner un jeton si on a le status (not null)
# status_count : nombre de jetons a gagner si on a le status (not null)





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
    
    def check_user(self, user_id: int):
        cursor = self.con.cursor()
        cursor.execute("SELECT * FROM profiles WHERE id = ?", (user_id,))
        return list(map(dict,cursor.fetchall()))
    
    def set_message(self, messages: int,user_id: int):
        cursor = self.con.cursor()
        cursor.execute("UPDATE profiles SET messages = ? WHERE id = ?", (messages,user_id,))
        self.con.commit()
    
    def get_tokens_settings(self):
        cursor = self.con.cursor()
        cursor.execute("SELECT * FROM tokens")
        return list(map(dict,cursor.fetchall()))
    
    def set_tokens(self, tokens: int,user_id: int):
        cursor = self.con.cursor()
        cursor.execute("UPDATE profiles SET tokens = ? WHERE id = ?", (tokens,user_id,))
        self.con.commit()
    
    def set_voice(self, voice_minutes: int,user_id: int):
        cursor = self.con.cursor()
        cursor.execute("UPDATE profiles SET voice_minutes = ? WHERE id = ?", (voice_minutes,user_id,))
        self.con.commit()
    
    def set_points(self, points: int,user_id: int):
        cursor = self.con.cursor()
        cursor.execute("UPDATE profiles SET points = ? WHERE id = ?", (points,user_id,))
        self.con.commit()