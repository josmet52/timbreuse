#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    class Mysql to manage de db access for the programm timbreuse
"""
import socket
import sys
import tkinter as tk
from tkinter import messagebox
import mysql.connector

from datetime import datetime, timedelta


class MysqlTimbreuse:
    
    """
        Cette classe gere les acces sur la base de données de la timbreuse jMb
    """

    def __init__(self, ip_db_server):
        
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

if __name__ == '__main__':

    # ERROR : direct acces to this class is not ok, reason = ????? (21.04.2020 jm)
    mysql_init = MysqlTimbreuse('192.168.1.109')
    ip  = mysql_init.local_ip
    connexion = mysql_init.get_db_connexion()
    
    # verify connexion
    if connexion:
        print("connected to db server on ip",ip)
    
    
    
