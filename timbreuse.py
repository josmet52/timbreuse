#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#--------------------------------------
#
#            /\  /\      
#        /  /  \/  \   /_
#     /_/  /        \ /_/
#
#  timbreuse.py
#  jMb home timbreuse Script
#
# Author  : Joseph Métrailler
#
#--------------------------------------
# import RPi.GPIO as GPIO
import time
import datetime

import pdb

import RPi.GPIO as GPIO
from mysql_lib_timbreuse import MysqlTimbreuse
from gpio_lib_timbreuse import GpioTimbreuse


class Timbreuse:
    """
        Ce programme, élaboré à but de formation, permet la saisie des temps de travail de la famille jMb
        Les fonctionnalités seront les suivantes:
            - pour chaque personne enregistrer les début du travail anisi que le mandat pour lequel l'activité est effectuée
                (un mandat peut être spécifique à un utilisateur ou attribué à plusieurs personnes)
            - enregistrer la fin du travail
            - les utilisateurs les mandats et les temps de travail sont enregistrés dans une base de donnée
            - la base de donnée est accessible depuis n'importe quel ordi sur le même WLAN
        Un affichage informe de la situation et/ou de l'avancement d'une saisie
        Des boutons permettent différentes actions. Plusieurs variantes ont été évaluées soit
            - version 1 ->  5 btn (blue-green-red-yellow-gray)
                - blue : défiler une liste
                - green : démarrer une activité
                - red : terminer une activité
                - yellow : OK
                - gray : CANCEL
            - version 2 -> 4 btn (green-red-yellow-gray)
                - green démarer une activité et défiler la liste
                - red : terminer une activité
                - yellow : OK
                - gray : CANCEL
            - version 3 -> 3 btn (green-red-gray)
                - green démarer une activité, défiler la liste et OK
                - red : terminer une activité
                - gray : CANCEL
            - version 4 -> 2 btn (green-gray)
                - green démarer une activité, défiler la liste, OK et terminer une activité
                - gray : CANCEL
                
            La version 1 (5 btn) est trop compliquée, l'utilisateur fait le disque jockey,
            la version 2 (4 bnt) est intuitive mais comprend beaucoup de boutons
            la version 3 (3 btn) utilise des pressions brèves et longues, elle est assez intuitive mais la calibrage des temps est difficile
            la version 4 (2 btn) implique une connaissace parfaite de la séquece des opérations par l'utilisateur -> difficile
            
            Finalement la version 2 avec 4 boutons qui ont des fonctionalités claires semble la plus adéquate
            mais la version 3 mériterait d'être testée par d'autres utiliateurs.
        
    """
    
    def __init__(self):
        
        # version infos
        VERSION_NAME = "jMb timbreuse" 
        VERSION_NO = "0.01.24" 
        VERSION_DATE = "05.06.2020"
        VERSION_DESCRIPTION = "Saisie des temps de travail jMb"
        VERSION_STATUS = "prototype en service "
        VERSION_AUTEUR = "josmet"
        
        self.button_working = False # si True empèche la ilde_task de mettre à jour l'affichage
        
        # initialisation de la classe MysqlTimbreuse
        self.ip_db_server = "192.168.1.109"
        self.mysql_timbreuse = MysqlTimbreuse(self.ip_db_server)
        self.choose_person = False      
        self.choose_task = False
        
        # initialisation de la classe GpioTimbreuse
        self.gpio_timbreuse = GpioTimbreuse()
        
        # initialisation variable globales
        self.qui_en_cours = ""
        self.no_qui_en_cours = 0
        self.id_qui_en_cours = 0
        
        self.quoi_en_cours = ""
        self.no_quoi_en_cours = 0
        self.id_quoi_en_cours = 0
        
        # pour mémoriser les activités en cours
        self.tasks_running = []
        
        # gestion de la fin d'une activité
        self.id_qui_stop_en_cours = 0
        self.qui_stop_en_cours = ""
        self.stop_running = False
#         
#         # Define GPIO to LCD mapping
#         self.LCD_RS = 7
#         self.LCD_E  = 12
#         self.LCD_D4 = 27
#         self.LCD_D5 = 24
#         self.LCD_D6 = 23
#         self.LCD_D7 = 18
#         self.LCD_BACKLIGHT = 20
#  
#         # Define some device constants
#         self.LCD_WIDTH = 16    # Maximum characters per line
#         self.LCD_CHR = True
#         self.LCD_CMD = False
#          
#         self.LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
#         self.LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
#          
#         # Timing constants
#         self.E_PULSE = 0.0001
#         self.E_DELAY = 0.0001
# 
#         # initialise buttons adress
#         self.BTN_RED = 6
#         self.BTN_GREEN = 19
#         self.BTN_BLUE = 26
#         self.BTN_YELLOW = 13
#         self.BTN_GRAY = 5
#         
#         GPIO.setwarnings(False)
#         GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
#         
#         GPIO.setup(self.LCD_E, GPIO.OUT, initial=0)  # E
#         GPIO.setup(self.LCD_RS, GPIO.OUT, initial=0) # RS
#         GPIO.setup(self.LCD_D4, GPIO.OUT, initial=0) # DB4
#         GPIO.setup(self.LCD_D5, GPIO.OUT, initial=0) # DB5
#         GPIO.setup(self.LCD_D6, GPIO.OUT, initial=0) # DB6
#         GPIO.setup(self.LCD_D7, GPIO.OUT, initial=0) # DB7
#         
#         GPIO.setup(self.LCD_BACKLIGHT, GPIO.OUT, initial=1) # backlight
#         GPIO.output(self.LCD_BACKLIGHT, False) # put backlight on
#         
#         # initialise the GPIO buttons inputs
#         GPIO.setup(self.BTN_RED, GPIO.IN, GPIO.PUD_DOWN)
#         GPIO.setup(self.BTN_GREEN, GPIO.IN, GPIO.PUD_DOWN)
#         GPIO.setup(self.BTN_BLUE, GPIO.IN, GPIO.PUD_DOWN)
#         GPIO.setup(self.BTN_YELLOW, GPIO.IN, GPIO.PUD_DOWN)
#         GPIO.setup(self.BTN_GRAY, GPIO.IN, GPIO.PUD_DOWN)

        # initialise buttons interrupts
        GPIO.add_event_detect(self.gpio_timbreuse.BTN_RED, GPIO.BOTH, callback = self.button_pressed_callback, bouncetime = 50)
        GPIO.add_event_detect(self.gpio_timbreuse.BTN_GREEN, GPIO.BOTH, callback = self.button_pressed_callback, bouncetime = 50)
        GPIO.add_event_detect(self.gpio_timbreuse.BTN_BLUE, GPIO.BOTH, callback = self.button_pressed_callback, bouncetime = 50)
        GPIO.add_event_detect(self.gpio_timbreuse.BTN_YELLOW, GPIO.BOTH, callback = self.button_pressed_callback, bouncetime = 50)
        GPIO.add_event_detect(self.gpio_timbreuse.BTN_GRAY, GPIO.BOTH, callback = self.button_pressed_callback, bouncetime = 50)
        
        # flags pour gestion des boutons sans rebonds
        self.red_btn_fire = False
        self.green_btn_fire = False
        self.blue_btn_fire = False
        self.yellow_btn_fire = False
        self.gray_btn_fire = False

    # procédure appelée lors de la pression sur une boutons
    def button_pressed_callback(self, channel):

        # empêcher la idle_task d'accéder à l'affichage
        self.button_working = True
        
        # red button
        if channel == self.gpio_timbreuse.BTN_RED and GPIO.input(self.gpio_timbreuse.BTN_RED) and not self.red_btn_fire:
            self.red_btn_fire = True
            self.red_button_fired()
        else:
            self.red_btn_fire = False
            
        # green button
        if channel == self.gpio_timbreuse.BTN_GREEN and GPIO.input(self.gpio_timbreuse.BTN_GREEN) and not self.green_btn_fire:
            self.green_btn_fire = True
            self.green_button_fired()
        else:
            self.green_btn_fire = False
            
        # blue button
        if channel == self.gpio_timbreuse.BTN_BLUE and GPIO.input(self.gpio_timbreuse.BTN_BLUE) and not self.blue_btn_fire:
            self.blue_btn_fire = True
            self.blue_button_fired()
        else:
            self.blue_btn_fire = False
            
        # yellow button
        if channel == self.gpio_timbreuse.BTN_YELLOW and GPIO.input(self.gpio_timbreuse.BTN_YELLOW) and not self.yellow_btn_fire:
            self.yellow_btn_fire = True
            self.yellow_button_fired()
        else:
            self.yellow_btn_fire = False
            
        # gray button
        if channel == self.gpio_timbreuse.BTN_GRAY and GPIO.input(self.gpio_timbreuse.BTN_GRAY) and not self.gray_btn_fire:
            self.gray_btn_fire = True
            self.gray_button_fired()
        else:
            self.gray_btn_fire = False
            
        # si aucune saisie en cours alors autoriser la idle_task d'accéder à l'affichage
        if not self.choose_person and not self.choose_task and not self.stop_running:
            self.button_working = False

    def green_button_fired(self): # on commence le boulot
        
        # connect to the db
        con, e = self.mysql_timbreuse.get_db_connexion()
        cur = con.cursor()
            
        # si aucune saisie n'est en cours alors on propose le choix de la 1ere personne de la db par ordre alphabetique
        if not self.choose_person and not self.choose_task and not self.stop_running:
            # select the first person
            sql_txt = "SELECT prenom, idqui FROM qui ORDER BY prenom LIMIT 1;" 
            cur.execute(sql_txt)
            rec = cur.fetchone()
            self.qui_en_cours = rec[0]
            self.no_qui_en_cours = 0
            self.id_qui_en_cours = rec[1]
            # update display
            self.gpio_timbreuse.lcd_string(self.qui_en_cours, self.gpio_timbreuse.LCD_LINE_1)
            self.gpio_timbreuse.lcd_string("", self.gpio_timbreuse.LCD_LINE_2)
            self.choose_person = True
            
        # si on est en train de choisr la personne alors on affiche la personne suivante
        elif self.choose_person:
            # find the last idqui
            sql_txt = "SELECT prenom, idqui FROM qui ORDER BY prenom;"
            cur.execute(sql_txt)
            rec = cur.fetchall()
            nbre_qui = len(rec) - 1
            # find the next person 
            if self.no_qui_en_cours >= nbre_qui:
                # if last then restart to first
                self.no_qui_en_cours = 0
            else:
                # else select the next
                self.no_qui_en_cours += 1
            # execute the query
            self.qui_en_cours = rec[self.no_qui_en_cours][0]
            self.id_qui_en_cours = rec[self.no_qui_en_cours][1]
            # display the person
            self.gpio_timbreuse.lcd_string(self.qui_en_cours, self.gpio_timbreuse.LCD_LINE_1)
            
        # si on est en train de choisr le mandat alors on affiche le mandat suivant
        # self.choose_task est initialisé par le yellow button (OK) losque la personne est validée
        elif self.choose_task:
            # find the last idquoi
            sql_txt = "".join(["SELECT quoi.activite, quoi.idquoi",
                               " FROM qui INNER JOIN (quoi INNER JOIN quiquoi ON (quoi.idquoi = quiquoi.idquoi)",
                               " AND (quoi.idquoi = quiquoi.idquoi)) ON (qui.idqui = quiquoi.idqui) AND (qui.idqui = quiquoi.idqui)",
                               " WHERE (((qui.prenom)='" , str(self.qui_en_cours), "'))",
                               " ORDER BY quoi.activite;"])
            cur.execute(sql_txt)
            rec = cur.fetchall()
            nbre_quoi = len(rec) - 1
            # find the next person 
            if self.no_quoi_en_cours >= nbre_quoi:
                # if last then restart to first
                self.no_quoi_en_cours = 0
            else:
                # else select the next
                self.no_quoi_en_cours += 1
                # if last then restart to first
            self.quoi_en_cours = rec[self.no_quoi_en_cours][0]
            self.id_quoi_en_cours = rec[self.no_quoi_en_cours][1]
            # display the person
            self.gpio_timbreuse.lcd_string(self.quoi_en_cours, self.gpio_timbreuse.LCD_LINE_2)
            
        # close the db cursor and connexion
        cur.close()
        con.close()

    
    def red_button_fired(self): # on quitte le boulot

        if self.stop_running:
            
            nbre_qui_running = len(self.tasks_running)
            if nbre_qui_running <= 1:
                return # do nothing because there is only on peron working
                
            # si plusieurs personnes trvaillent alors on peut sélectionner la bonne personne par pressions successives
            if self.no_qui_stoping >= nbre_qui_running - 1:
                # if last then restart to first
                self.no_qui_stoping = 0
            else:
                # else select the next
                self.no_qui_stoping += 1
            # execute the query
            self.qui_stoping = self.tasks_running[self.no_qui_stoping][3]
            self.id_qui_stoping = self.tasks_running[self.no_qui_stoping][0]
            # display the person
        
            self.gpio_timbreuse.lcd_string(self.qui_stoping, self.gpio_timbreuse.LCD_LINE_1)
            self.gpio_timbreuse.lcd_string("stop job ?", self.gpio_timbreuse.LCD_LINE_2)
        
        else:

            # si une seule personne travaille alors on popose la fin de cette activité
            if len(self.tasks_running) == 0:
                return
            # create the list of working persons
            self.id_qui_stoping = self.tasks_running[0][0]
            self.qui_stoping = self.tasks_running[0][3]
            self.no_qui_stoping = 0
            self.stop_running = True
            
            self.gpio_timbreuse.lcd_string(self.qui_stoping, self.gpio_timbreuse.LCD_LINE_1)
            self.gpio_timbreuse.lcd_string("stop job ?", self.gpio_timbreuse.LCD_LINE_2)

    # confirmation des actions en cours
    def yellow_button_fired(self): # ok
        
        # connect to the db
        con, e = self.mysql_timbreuse.get_db_connexion()
        cur = con.cursor(buffered=True)
        
        if self.choose_person:
        # close choose_person and start choose_task
            for task in self.tasks_running:
                if task[0] == self.id_qui_en_cours:
                    disp_txt_1 = " ".join([task[3][0], "->", task[4]])
                    disp_txt_2 = " ".join(["stop before new"])
                    
                    self.gpio_timbreuse.lcd_string(disp_txt_1, self.gpio_timbreuse.LCD_LINE_1)
                    self.gpio_timbreuse.lcd_string(disp_txt_2, self.gpio_timbreuse.LCD_LINE_2)
                    
                    self.choose_person = False
                    self.choose_task = False
                    return
                
            # find the tasks for this user first the default ans after order by activite
            sql_txt = "".join(["SELECT quoi.activite",
                               " FROM qui INNER JOIN (quoi INNER JOIN quiquoi ON (quoi.idquoi = quiquoi.idquoi)",
                               " AND (quoi.idquoi = quiquoi.idquoi)) ON (qui.idqui = quiquoi.idqui) AND (qui.idqui = quiquoi.idqui)",
                               " WHERE (((qui.prenom)='" , str(self.qui_en_cours), "'))",
                               " ORDER BY quoi.activite;"])
            cur.execute(sql_txt)
            rec = cur.fetchone()
            self.no_quoi_en_cours = 0
            self.quoi_en_cours = rec[0]
            # display the first task
            self.gpio_timbreuse.lcd_string(self.quoi_en_cours, self.gpio_timbreuse.LCD_LINE_2)
            
            self.choose_person = False
            self.choose_task = True
            
        elif self.choose_task:
            # set the program in task choosing mode            
            self.choose_person = False
            self.choose_task = False
            disp_txt_1 = " ".join([str(self.qui_en_cours)[0], "->", str(self.quoi_en_cours)])
            disp_txt_2 = " ".join(["Starting", time.strftime("%H:%M")])
            self.gpio_timbreuse.lcd_string(disp_txt_1, self.gpio_timbreuse.LCD_LINE_1)
            self.gpio_timbreuse.lcd_string(disp_txt_2, self.gpio_timbreuse.LCD_LINE_2)
            
            sql_txt = "INSERT INTO quand (idqui, idquoi, begindatetime) VALUES(%s, %s, %s)"
            val_tuple = (str(self.id_qui_en_cours), str(self.id_quoi_en_cours), time.strftime("%Y-%m-%d %H:%M:%S"))
            cur.execute(sql_txt, val_tuple)
            con.commit()
            
            self.tasks_running.append((self.id_qui_en_cours, self.id_quoi_en_cours, time.strftime("%Y-%m-%d %H:%M:%S"), self.qui_en_cours, self.quoi_en_cours))
            print(" ".join(["begin", self.qui_en_cours, "->", self.quoi_en_cours]))

        elif self.stop_running:
            # if stopping 
            
            id_qui_stoping = self.tasks_running[self.no_qui_stoping][0]
            id_quoi_stoping = self.tasks_running[self.no_qui_stoping][1]
            
            sql_txt = "".join(["UPDATE quand SET enddatetime='", time.strftime("%Y-%m-%d %H:%M:%S"), "'"
                               " WHERE (idqui=", str(id_qui_stoping), " AND idquoi=", str(id_quoi_stoping)," AND enddatetime IS NULL);"])
            cur.execute(sql_txt)
            con.commit()

            disp_txt_1 = " ".join([str(self.tasks_running[self.no_qui_stoping][3])[0], "->", str(self.tasks_running[self.no_qui_stoping][4])])
            disp_txt_2 = " ".join(["Stoped at", time.strftime("%H:%M")])
            self.gpio_timbreuse.lcd_string(disp_txt_1, self.gpio_timbreuse.LCD_LINE_1)
            self.gpio_timbreuse.lcd_string(disp_txt_2, self.gpio_timbreuse.LCD_LINE_2)
            print(" ".join(["finish", str(self.tasks_running[self.no_qui_stoping][3]), "->", str(self.tasks_running[self.no_qui_stoping][4])]))

            self.tasks_running.pop(self.no_qui_stoping)
            self.choose_person = False
            self.choose_task = False
            self.stop_running = False
        
        cur.close()
        con.close()
#         self.button_working = False

    def gray_button_fired(self): # cancel

        if self.choose_person or self.choose_task or self.stop_running:
            # cancel the running operation
            # reset all the flags
            # dispaly date and time
            self.choose_person = False
            self.choose_task = False
            self.stop_running = False
            
            self.qui_en_cours = ''
            self.idqui_en_cours = 0
            self.quoi_en_cours = ''
            self.idquoi_en_cours = 0
            
            self.gpio_timbreuse.lcd_string("action canceled", self.gpio_timbreuse.LCD_LINE_2)
            time.sleep(1)
            
            self.update_idle_display()
            self.button_working = False
        
        
    def blue_button_fired(self): # down
        pass
#  
#     def lcd_init(self): 
#         # Initialise display
#         self.lcd_byte(0x33, self.LCD_CMD) # 110011 Initialise
#         self.lcd_byte(0x32, self.LCD_CMD) # 110010 Initialise
#         self.lcd_byte(0x06, self.LCD_CMD) # 000110 Cursor move direction
#         self.lcd_byte(0x0C, self.LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
#         self.lcd_byte(0x28, self.LCD_CMD) # 101000 Data length, number of lines, font size
#         self.lcd_byte(0x01, self.LCD_CMD) # 000001 Clear display
#         time.sleep(self.E_DELAY)
# 
#     def lcd_byte(self, bits, mode):
#         # Send byte to data pins
#         # bits = data
#         # mode = True  for character
#         #        False for command
# 
#         GPIO.output(self.LCD_RS, mode) # RS
#         # High bits
#         GPIO.output(self.LCD_D4, False)
#         GPIO.output(self.LCD_D5, False)
#         GPIO.output(self.LCD_D6, False)
#         GPIO.output(self.LCD_D7, False)
#         if bits&0x10==0x10:
#             GPIO.output(self.LCD_D4, True)
#         if bits&0x20==0x20:
#             GPIO.output(self.LCD_D5, True)
#         if bits&0x40==0x40:
#             GPIO.output(self.LCD_D6, True)
#         if bits&0x80==0x80:
#             GPIO.output(self.LCD_D7, True)
# 
#         # Toggle 'Enable' pin
#         self.lcd_toggle_enable()
# 
#         # Low bits
#         GPIO.output(self.LCD_D4, False)
#         GPIO.output(self.LCD_D5, False)
#         GPIO.output(self.LCD_D6, False)
#         GPIO.output(self.LCD_D7, False)
#         if bits&0x01==0x01:
#             GPIO.output(self.LCD_D4, True)
#         if bits&0x02==0x02:
#             GPIO.output(self.LCD_D5, True)
#         if bits&0x04==0x04:
#             GPIO.output(self.LCD_D6, True)
#         if bits&0x08==0x08:
#             GPIO.output(self.LCD_D7, True)
# 
#         # Toggle 'Enable' pin
#         self.lcd_toggle_enable()
#      
#     def lcd_toggle_enable(self):
# 
#         # Toggle enable
#         time.sleep(self.E_DELAY)
#         GPIO.output(self.LCD_E, True)
#         time.sleep(self.E_PULSE)
#         GPIO.output(self.LCD_E, False)
#         time.sleep(self.E_DELAY)
#      
#     def lcd_string(self, message,line):
#         # Send string to display
# 
#         message = message.ljust(self.LCD_WIDTH," ")
# 
#         self.lcd_byte(line, self.LCD_CMD)
# 
#         for i in range(self.LCD_WIDTH):
#             self.lcd_byte(ord(message[i]),self.LCD_CHR)
#   
    def update_idle_display(self):
        
        if len(self.tasks_running) > 0:
            
            if len(self.tasks_running) == 1: 
                txt_1 = "".join([self.tasks_running[0][3][0], " -> ", self.tasks_running[0][4]])
                self.gpio_timbreuse.lcd_string(txt_1,self.gpio_timbreuse.LCD_LINE_1)
                self.gpio_timbreuse.lcd_string(str(datetime.datetime.now()),self.gpio_timbreuse.LCD_LINE_2)
                
            elif len(self.tasks_running) == 2: 
                txt_1 = "".join([self.tasks_running[0][3][0], " -> ", self.tasks_running[0][4]])
                txt_2 = "".join([self.tasks_running[1][3][0], " -> ", self.tasks_running[1][4]])
                self.gpio_timbreuse.lcd_string(txt_1,self.gpio_timbreuse.LCD_LINE_1)
                self.gpio_timbreuse.lcd_string(txt_2, self.gpio_timbreuse.LCD_LINE_2)
                
            else: 
                self.gpio_timbreuse.lcd_string(str(datetime.datetime.now()),self.gpio_timbreuse.LCD_LINE_1)
                self.gpio_timbreuse.lcd_string("users working", self.gpio_timbreuse.LCD_LINE_2)
        else:
            self.gpio_timbreuse.lcd_string(str(datetime.datetime.now()),self.gpio_timbreuse.LCD_LINE_1)
            self.gpio_timbreuse.lcd_string("nobody working", self.gpio_timbreuse.LCD_LINE_2)
    
        
    def waiting_loop(self):
        
        self.gpio_timbreuse.lcd_init()
        
        last_time = datetime.datetime.now()
        passe_no = 0
        self.gpio_timbreuse.lcd_string(str(datetime.datetime.now()), self.gpio_timbreuse.LCD_LINE_1)
        self.gpio_timbreuse.lcd_string("Welcome         ", self.gpio_timbreuse.LCD_LINE_2)
        
        pause_time = 10
        
        while True:
            elapsed = (datetime.datetime.now() - last_time).total_seconds()
            
            if elapsed >= pause_time:
                while self.button_working:
                    time.sleep(0.1)
                    
                self.update_idle_display()
                last_time = datetime.datetime.now()
                time.sleep(pause_time -0.5)
            
        
if __name__ == '__main__':
    
    timbreuse = Timbreuse()
    print("program timbreuse started")
    timbreuse.waiting_loop()
        
        
