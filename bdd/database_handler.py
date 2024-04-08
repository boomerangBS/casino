
# PROFILES

# id : id du l'utilisateur (not null)
# tokens : nombre de jetons (not null)
# coins : nombre de coins (not null)
# messages : nombre de messages envoyé (avant reinitialisation pour gains) (not null)
# voice_minutes : nombre de minutes en vocal (avant reinitialisation pour gains) (not null)
# badges : roles badges gagnés (roulette : id de l'item,id de l'item,id de l'item)
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

# --------------------------------------------

# ROULETTE_CATEGORY

# id : id de la categorie (not null) (clée primaire autoincrement)
# name : nom de la categorie (not null)

# --------------------------------------------

# ROULETTE_ITEMS

# id : id de l'item (not null) (clée primaire autoincrement)
# categoty_id : id de la categorie (not null)
# name : nom de l'item (not null)
# type : type de l'item (not null) (role,badge,coins,jetons)
# data : data additionnelle (id du role, nombre de coins)
# rarity : rareté de l'item (not null) (INT) (pourcentage (mais % pas mis dans la db juste le chiffre))

# --------------------------------------------

# SHOP
# id : id de l'item (not null) (clée primaire autoincrement)
# name : nom de l'item (not null)
# type : type de l'item (not null) (role,badge,coins,jetons)
# data : data additionnelle (id du role, nombre de coins)
# price : prix de l'item (not null)

import os
import sqlite3
import json

f = open("config.json", "r")
config = json.load(f)
f.close()

class DatabaseHandler():
    def __init__(self, database_name: str):
        self.con = sqlite3.connect(f"{os.path.dirname(os.path.abspath(__file__))}/{database_name}")
        self.con.row_factory = sqlite3.Row
    
    ## USER RELATED
    def list_users(self):
        cursor = self.con.cursor()
        cursor.execute("SELECT * FROM profiles")
        return list(map(dict,cursor.fetchall()))

    def check_user(self, user_id: int):
        cursor = self.con.cursor()
        cursor.execute("SELECT * FROM profiles WHERE id = ?", (user_id,))
        return list(map(dict,cursor.fetchall()))
    
    def set_message(self, messages: int,user_id: int):
        cursor = self.con.cursor()
        cursor.execute("UPDATE profiles SET messages = ? WHERE id = ?", (messages,user_id,))
        self.con.commit()
    
    def set_coins(self, coins: int,user_id: int):
        cursor = self.con.cursor()
        cursor.execute("UPDATE profiles SET coins = ? WHERE id = ?", (coins,user_id,))
        self.con.commit()
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
    
    def set_badges(self, badges: str,user_id: int):
        cursor = self.con.cursor()
        cursor.execute("UPDATE profiles SET badges = ? WHERE id = ?", (badges,user_id,))
        self.con.commit()
        
    def create_user(self, user_id: int):
        cursor = self.con.cursor()
        cursor.execute("INSERT INTO profiles (id,tokens,coins,messages,voice_minutes,points,rob_availables) VALUES (?,?,?,?,?,?,?)", (user_id,5,0,0,0,0,0))
        self.con.commit()

    def get_badges(self, user_id: int):
        cursor = self.con.cursor()
        cursor.execute("SELECT badges FROM profiles WHERE id = ?", (user_id,))
        return cursor.fetchone()[0]
    
    ## CONFIG RELATED

    def get_tokens_settings(self):
        cursor = self.con.cursor()
        cursor.execute("SELECT * FROM tokens")
        return list(map(dict,cursor.fetchall()))
    
    def set_tokens_settings(self, key: str, value: str):
        cursor = self.con.cursor()
        cursor.execute(f"UPDATE tokens SET {key} = ?", (value,))
        self.con.commit()
    
    ## ROULETTE RELATED
    def get_roulette_category(self):
        cursor = self.con.cursor()
        cursor.execute("SELECT * FROM roulette_category")
        return list(map(dict,cursor.fetchall()))
    
    def get_roulette_items(self, category_id: int=None):
        cursor = self.con.cursor()
        if category_id == None:
            cursor.execute("SELECT * FROM roulette_items")
        else:
            cursor.execute("SELECT * FROM roulette_items WHERE category_id = ?", (category_id,))
        return list(map(dict,cursor.fetchall()))
    
    def add_roulette_category(self, name: str):
        cursor = self.con.cursor()
        cursor.execute("INSERT INTO roulette_category (name) VALUES (?)", (name,))
        self.con.commit()
    
    def remove_roulette_category(self, category_id: int):
        cursor = self.con.cursor()
        cursor.execute("DELETE FROM roulette_category WHERE id = ?", (category_id,))
        cursor.execute("DELETE FROM roulette_items WHERE category_id = ?", (category_id,))
        self.con.commit()
    
    def add_roulette_item(self, category_id: int, name: str, type: str, data: str, rarity: int):
        cursor = self.con.cursor()
        cursor.execute("INSERT INTO roulette_items (category_id,name,type,data,rarity) VALUES (?,?,?,?,?)", (category_id,name,type,data,rarity))
        self.con.commit()

    def remove_roulette_item(self, item_id: int):
        cursor = self.con.cursor()
        cursor.execute("DELETE FROM roulette_items WHERE id = ?", (item_id,))
        self.con.commit()

    def add_roulette_nothing(self,id:int,catid:int,rarity:int):
        cursor = self.con.cursor()
        cursor.execute("INSERT INTO roulette_items (id,category_id,name,type,rarity) VALUES (?,?,?,?,?)", (id,catid,"Rien","nothing",rarity,))
        self.con.commit()    
    ## SHOP RELATED

    def get_shop(self):
        cursor = self.con.cursor()
        cursor.execute("SELECT * FROM shop")
        return list(map(dict,cursor.fetchall()))
    
    def check_item(self, item_id: int):
        cursor = self.con.cursor()
        cursor.execute("SELECT * FROM shop WHERE id = ?", (item_id,))
        return list(map(dict,cursor.fetchall()))
    
    def add_shop_item(self, name: str, type: str, data: str, price: int):
        cursor = self.con.cursor()
        cursor.execute("INSERT INTO shop (name,type,data,price) VALUES (?,?,?,?)", (name,type,data,price))
        self.con.commit()

    def remove_shop_item(self, item_id: int):
        cursor = self.con.cursor()
        cursor.execute("DELETE FROM shop WHERE id = ?", (item_id,))
        self.con.commit()