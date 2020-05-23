#!/usr/bin/env python3
# -*-
"""
    class Mysql to manage de db access for the programm temp_db
"""
import socket
import sys
from tkinter import messagebox
import mysql.connector

import tkinter as tk
from datetime import datetime, timedelta
# import time


class MysqlTimbreuse:
    
    """
        Cette classe gere les accès sur la base de données de la timbreuse jMb
    """

    def __init__(self, ip_db_server):
        
        # version infos
        VERSION_NAME = "jMb timbreuse" 
        VERSION_NO = "0.01.01" 
        VERSION_DATE = "23.05.2020"
        VERSION_DESCRIPTION = "tout au début"
        VERSION_STATUS = "en développement "
        VERSION_AUTEUR = "josmet"
        
        self.database_username = "pi"  # YOUR MYSQL USERNAME, USUALLY ROOT
        self.database_password = "mablonde"  # YOUR MYSQL PASSWORD
        self.database_name = "timbreuse"  # YOUR DATABASE NAME
        self.host_name = "localhost"
        self.server_ip = ip_db_server
        self.record = ""
        # get the local IP adress
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.local_ip = s.getsockname()[0]
        s.close()
        
        con, e = self.get_db_connexion()
        if not con:
            print("mysql_lib_timbreuse : _init_ -> DB UNEXPECTED ERROR\n" + str(e[0]), "/", str(e[1]), "/", str(e[2]) + "\nLe programme va s'arrêter")
            msg = "".join(["ERROR " + str(e[0]), "/ ", str(e[1]), "/ ", str(e[2]) + "Le programme va s'arrêter"])
            tk.messagebox.showerror("mysql_lib_timbreuse ERROR", msg)
            print("DB UNEXPECTED ERROR", msg)
            sys.exit()
            
    def get_db_connexion(self):
        
        # verify if the mysql server is ok and the db avaliable
        try:
            if self.local_ip == self.server_ip: #.split('.')[3]: # if we are on the RPI with mysql server (RPI making temp acquis)
                # test the local database connection
#                 con = mdb.connect(self.host_name, self.database_username, self.database_password, self.database_name)
                con = mysql.connector.connect(user=self.database_username, password=self.database_password, host=self.host_name, database=self.database_name)
                "".join(['Connected on local DB "', self.database_name, '"'])
            else:
                # test the distant database connection
                con = mysql.connector.connect(user=self.database_username, password=self.database_password, host=self.server_ip, database=self.database_name)
                "".join(['Connected on distant DB "', self.database_name, '" on "', self.server_ip, '"'])
            return con, sys.exc_info()
        
        except:
            # return error
            return False, sys.exc_info()
        
    def create_tables_and_fill_design_records(self):

      
        con, e = self.get_db_connexion()
        cur = con.cursor()
        
#         sql_txt = "CREATE TABLE IF NOT EXISTS qui(idqui INT PRIMARY KEY AUTO_INCREMENT, prenom TEXT NOT NULL);"
#         cur.execute(sql_txt)
#         sql_txt = "CREATE TABLE IF NOT EXISTS quoi(idquoi INT PRIMARY KEY AUTO_INCREMENT, activite TEXT NOT NULL);"
#         cur.execute(sql_txt)
#         sql_txt = "CREATE TABLE IF NOT EXISTS quiquoi(idquiquoi INT PRIMARY KEY AUTO_INCREMENT, idqui INT, idquoi INT, defaut INT);"
#         cur.execute(sql_txt)
#         sql_txt = "CREATE TABLE IF NOT EXISTS quand(idquand INT PRIMARY KEY AUTO_INCREMENT, idqui INT, idquoi INT, begindatetime DATETIME, enddatetime DATETIME);"
#         cur.execute(sql_txt)
#          
#         sql_txt = "INSERT INTO quand(idqui, idquoi, begindatetime, enddatetime) VALUES (1,1,'2020-05-14 15:45', '2020-05-14 17:25');"
#         cur.execute(sql_txt)
#         sql_txt = "INSERT INTO quand(idqui, idquoi, begindatetime, enddatetime) VALUES (1,1,'2020-05-15 10:45', '2020-05-15 12:25');"
#         cur.execute(sql_txt)
#         sql_txt = "INSERT INTO quand(idqui, idquoi, begindatetime, enddatetime) VALUES (1,5,'2020-05-15 15:45', '2020-05-15 16:25');"
#         cur.execute(sql_txt)
#         sql_txt = "INSERT INTO quand(idqui, idquoi, begindatetime, enddatetime) VALUES (2,3,'2020-05-15 15:45', '2020-05-15 16:25');"
#         cur.execute(sql_txt)
# 
#         sql_txt = "INSERT INTO qui(prenom) VALUES ('Maryse');" #1
#         cur.execute(sql_txt)
#         sql_txt = "INSERT INTO qui(prenom) VALUES ('Joseph');" #2
#         cur.execute(sql_txt)
#          
#         sql_txt = "INSERT INTO quoi(activite) VALUES ('couture');" #1 m
#         cur.execute(sql_txt)
#         sql_txt = "INSERT INTO quoi(activite) VALUES ('monitor');" #2 j
#         cur.execute(sql_txt)
#         sql_txt = "INSERT INTO quoi(activite) VALUES ('timbreuse');" #3 j
#         cur.execute(sql_txt)
#         sql_txt = "INSERT INTO quoi(activite) VALUES ('cuisine');" #4 mj
#         cur.execute(sql_txt)
#         sql_txt = "INSERT INTO quoi(activite) VALUES ('lavage');" #5 m
#         cur.execute(sql_txt)
#         sql_txt = "INSERT INTO quoi(activite) VALUES ('menage');" #6 m
#         cur.execute(sql_txt)
#         sql_txt = "INSERT INTO quoi(activite) VALUES ('exterieur');" #7 j
#         cur.execute(sql_txt)
#         sql_txt = "INSERT INTO quoi(activite) VALUES ('courses');" #8 mj
#         cur.execute(sql_txt)
#         sql_txt = "INSERT INTO quoi(activite) VALUES ('sport');" #9 m
#         cur.execute(sql_txt)
#          
#         sql_txt = "INSERT INTO quiquoi(idqui, idquoi, defaut) VALUES (1,1,1);"
#         cur.execute(sql_txt)
#         sql_txt = "INSERT INTO quiquoi(idqui, idquoi, defaut) VALUES (1,4,0);"
#         cur.execute(sql_txt)
#         sql_txt = "INSERT INTO quiquoi(idqui, idquoi, defaut) VALUES (1,5,0);"
#         cur.execute(sql_txt)
#         sql_txt = "INSERT INTO quiquoi(idqui, idquoi, defaut) VALUES (1,6,0);"
#         cur.execute(sql_txt)
#         sql_txt = "INSERT INTO quiquoi(idqui, idquoi, defaut) VALUES (1,8,0);"
#         cur.execute(sql_txt)
#         sql_txt = "INSERT INTO quiquoi(idqui, idquoi, defaut) VALUES (1,9,0);"
#         cur.execute(sql_txt)
#          
#         sql_txt = "INSERT INTO quiquoi(idqui, idquoi, defaut) VALUES (2,2,0);"
#         cur.execute(sql_txt)
#         sql_txt = "INSERT INTO quiquoi(idqui, idquoi, defaut) VALUES (2,3,1);"
#         cur.execute(sql_txt)
#         sql_txt = "INSERT INTO quiquoi(idqui, idquoi, defaut) VALUES (2,4,0);"
#         cur.execute(sql_txt)
#         sql_txt = "INSERT INTO quiquoi(idqui, idquoi, defaut) VALUES (2,7,0);"
#         cur.execute(sql_txt)
#         sql_txt = "INSERT INTO quiquoi(idqui, idquoi, defaut) VALUES (2,8,0);"
#         cur.execute(sql_txt)
#         sql_txt = "INSERT INTO quiquoi(idqui, idquoi, defaut) VALUES (2,9,0);"
#         cur.execute(sql_txt)
#          
#         con.commit()

        sql_txt = " ".join(["SELECT quoi.activite",
                            "FROM quoi INNER JOIN (qui INNER JOIN quiquoi ON qui.idqui = quiquoi.idqui) ON quoi.idquoi = quiquoi.idquoi",
                            "WHERE (((qui.prenom)='Maryse'))",
                            "ORDER BY quiquoi.defaut DESC;"])
        print(sql_txt)
        cur.execute(sql_txt)
        data_set = cur.fetchall()

        for job in data_set:
            print(job)
            
        sql_txt = " ".join(["SELECT qui.prenom, quoi.activite, quand.begindatetime, quand.enddatetime, TIMESTAMPDIFF(MINUTE, quand.begindatetime, quand.enddatetime)",
                            "FROM quoi INNER JOIN (qui INNER JOIN quand ON qui.idqui = quand.idqui) ON quoi.idquoi = quand.idquoi",
                            "WHERE (((qui.prenom)='Maryse'));" ])#,
        #                     "GROUP BY quoi.activite",
        #                     "ORDER BY quoi.activite;"])
        print(sql_txt)
        cur.execute(sql_txt)
        data_set = cur.fetchall()

        for activite in data_set:
            print(activite)
            
        con.close()


if __name__ == '__main__':

    # ERROR : direct acces to this class is not ok, reason = ????? (21.04.2020 jm)
    mysql_init = MysqlTimbreuse('192.168.1.142')
    ip  = mysql_init.local_ip
    connexion = mysql_init.get_db_connexion()
    
    # verify connexion
    if connexion:
        print("connected to db server on ip",ip)
        
    # create the tables and dev records
    data = mysql_init.create_tables_and_fill_design_records()
    
    
    
