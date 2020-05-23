#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pdb
import sqlite3
conn = sqlite3.connect('timbreuse.db')
cur = conn.cursor()

sql_txt = "CREATE TABLE qui(idqui INTEGER PRIMARY KEY AUTOINCREMENT, prenom TEXT NOT NULL)"
cur.execute(sql_txt)
sql_txt = "CREATE TABLE quoi(idquoi INTEGER PRIMARY KEY AUTOINCREMENT, activite TEXT NOT NULL)"
cur.execute(sql_txt)
sql_txt = "CREATE TABLE quiquoi(idquiquoi INTEGER PRIMARY KEY AUTOINCREMENT, idqui INTEGER, idquoi INTEGER, defaut INTEGER)"
cur.execute(sql_txt)
sql_txt = "CREATE TABLE quand(idquand INTEGER PRIMARY KEY AUTOINCREMENT, idqui INTEGER, idquoi INTEGER, begindatetime TEXT, enddatetime TEXT)"
cur.execute(sql_txt)
 
sql_txt = "INSERT INTO quand('idqui', 'idquoi', 'begindatetime', 'enddatetime') VALUES (1,1,'2020-05-14 15:45', '2020-05-14 17:25')"
cur.execute(sql_txt)
sql_txt = "INSERT INTO quand('idqui', 'idquoi', 'begindatetime', 'enddatetime') VALUES (1,1,'2020-05-15 10:45', '2020-05-15 12:25')"
cur.execute(sql_txt)
sql_txt = "INSERT INTO quand('idqui', 'idquoi', 'begindatetime', 'enddatetime') VALUES (1,5,'2020-05-15 15:45', '2020-05-15 16:25')"
cur.execute(sql_txt)
sql_txt = "INSERT INTO quand('idqui', 'idquoi', 'begindatetime', 'enddatetime') VALUES (2,3,'2020-05-15 15:45', '2020-05-15 16:25')"
cur.execute(sql_txt)

sql_txt = "INSERT INTO qui('prenom') VALUES ('Maryse')" #1
cur.execute(sql_txt)
sql_txt = "INSERT INTO qui('prenom') VALUES ('Joseph')" #2
cur.execute(sql_txt)
 
sql_txt = "INSERT INTO quoi('activite') VALUES ('couture')" #1 m
cur.execute(sql_txt)
sql_txt = "INSERT INTO quoi('activite') VALUES ('monitor')" #2 j
cur.execute(sql_txt)
sql_txt = "INSERT INTO quoi('activite') VALUES ('timbreuse')" #3 j
cur.execute(sql_txt)
sql_txt = "INSERT INTO quoi('activite') VALUES ('cuisine')" #4 mj
cur.execute(sql_txt)
sql_txt = "INSERT INTO quoi('activite') VALUES ('lavage')" #5 m
cur.execute(sql_txt)
sql_txt = "INSERT INTO quoi('activite') VALUES ('menage')" #6 m
cur.execute(sql_txt)
sql_txt = "INSERT INTO quoi('activite') VALUES ('exterieur')" #7 j
cur.execute(sql_txt)
sql_txt = "INSERT INTO quoi('activite') VALUES ('courses')" #8 mj
cur.execute(sql_txt)
sql_txt = "INSERT INTO quoi('activite') VALUES ('sport')" #9 mj
cur.execute(sql_txt)
 
sql_txt = "INSERT INTO quiquoi('idqui', 'idquoi', 'defaut') VALUES (1,1,1)"
cur.execute(sql_txt)
sql_txt = "INSERT INTO quiquoi('idqui', 'idquoi', 'defaut') VALUES (1,4,0)"
cur.execute(sql_txt)
sql_txt = "INSERT INTO quiquoi('idqui', 'idquoi', 'defaut') VALUES (1,5,0)"
cur.execute(sql_txt)
sql_txt = "INSERT INTO quiquoi('idqui', 'idquoi', 'defaut') VALUES (1,6,0)"
cur.execute(sql_txt)
sql_txt = "INSERT INTO quiquoi('idqui', 'idquoi', 'defaut') VALUES (1,8,0)"
cur.execute(sql_txt)
sql_txt = "INSERT INTO quiquoi('idqui', 'idquoi', 'defaut') VALUES (1,9,0)"
cur.execute(sql_txt)
 
sql_txt = "INSERT INTO quiquoi('idqui', 'idquoi', 'defaut') VALUES (2,2,0)"
cur.execute(sql_txt)
sql_txt = "INSERT INTO quiquoi('idqui', 'idquoi', 'defaut') VALUES (2,3,1)"
cur.execute(sql_txt)
sql_txt = "INSERT INTO quiquoi('idqui', 'idquoi', 'defaut') VALUES (2,4,0)"
cur.execute(sql_txt)
sql_txt = "INSERT INTO quiquoi('idqui', 'idquoi', 'defaut') VALUES (2,7,0)"
cur.execute(sql_txt)
sql_txt = "INSERT INTO quiquoi('idqui', 'idquoi', 'defaut') VALUES (2,8,0)"
cur.execute(sql_txt)
sql_txt = "INSERT INTO quiquoi('idqui', 'idquoi', 'defaut') VALUES (2,9,0)"
cur.execute(sql_txt)
 
conn.commit()

sql_txt = " ".join(["SELECT quoi.activite",
                    "FROM quoi INNER JOIN (qui INNER JOIN quiquoi ON qui.idqui = quiquoi.idqui) ON quoi.idquoi = quiquoi.idquoi",
                    "WHERE (((qui.prenom)='Maryse'))",
                    "ORDER BY quiquoi.defaut DESC;"])
print(sql_txt)
data_set = cur.execute(sql_txt)

for job in data_set:
    print(job)
    
sql_txt = " ".join(["SELECT qui.prenom, quoi.activite, quand.begindatetime, quand.enddatetime, (JulianDay(quand.enddatetime) - JulianDay(quand.begindatetime)) * 24",
                    "FROM quoi INNER JOIN (qui INNER JOIN quand ON qui.idqui = quand.idqui) ON quoi.idquoi = quand.idquoi",
                    "WHERE (((qui.prenom)='Maryse'));" ])#,
#                     "GROUP BY quoi.activite",
#                     "ORDER BY quoi.activite;"])
print(sql_txt)
data_set = cur.execute(sql_txt)

for activite in data_set:
    print(activite)
    
conn.close()
