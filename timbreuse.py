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
# Date    : 15.05.2020
# Version : 0.1
#
#--------------------------------------
import RPi.GPIO as GPIO
import time
import pdb
import datetime
import signal

class Timbreuse:
    """
    """
    
    def __init__(self):
        
        self.button_working = False
        
        # Define GPIO to LCD mapping
        self.LCD_RS = 7
        self.LCD_E  = 12
        self.LCD_D4 = 27
        self.LCD_D5 = 24
        self.LCD_D6 = 23
        self.LCD_D7 = 18
        self.LCD_BACKLIGHT = 20
 
        # Define some device constants
        self.LCD_WIDTH = 16    # Maximum characters per line
        self.LCD_CHR = True
        self.LCD_CMD = False
         
        self.LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
        self.LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
         
        # Timing constants
        self.E_PULSE = 0.0001
        self.E_DELAY = 0.0001

        # initialise buttons adress
        self.BTN_RED = 26
        self.BTN_GREEN = 19
        self.BTN_BLUE = 6
        self.BTN_YELLOW = 13
        self.BTN_GRAY = 5
        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
        GPIO.setup(self.LCD_E, GPIO.OUT, initial=0)  # E
        GPIO.setup(self.LCD_RS, GPIO.OUT, initial=0) # RS
        GPIO.setup(self.LCD_D4, GPIO.OUT, initial=0) # DB4
        GPIO.setup(self.LCD_D5, GPIO.OUT, initial=0) # DB5
        GPIO.setup(self.LCD_D6, GPIO.OUT, initial=0) # DB6
        GPIO.setup(self.LCD_D7, GPIO.OUT, initial=0) # DB7
        
        GPIO.setup(self.LCD_BACKLIGHT, GPIO.OUT, initial=1) # backlight
        GPIO.output(self.LCD_BACKLIGHT, False) # put backlight on
        
        # initialise the BPIO buttons inputs
        GPIO.setup(self.BTN_RED, GPIO.IN, GPIO.PUD_DOWN)
        GPIO.setup(self.BTN_GREEN, GPIO.IN, GPIO.PUD_DOWN)
        GPIO.setup(self.BTN_BLUE, GPIO.IN, GPIO.PUD_DOWN)
        GPIO.setup(self.BTN_YELLOW, GPIO.IN, GPIO.PUD_DOWN)
        GPIO.setup(self.BTN_GRAY, GPIO.IN, GPIO.PUD_DOWN)

        # initialise buttons interrupts
        GPIO.add_event_detect(self.BTN_RED, GPIO.BOTH, callback = self.button_pressed_callback, bouncetime = 50)
        GPIO.add_event_detect(self.BTN_GREEN, GPIO.BOTH, callback = self.button_pressed_callback, bouncetime = 50)
        GPIO.add_event_detect(self.BTN_BLUE, GPIO.BOTH, callback = self.button_pressed_callback, bouncetime = 50)
        GPIO.add_event_detect(self.BTN_YELLOW, GPIO.BOTH, callback = self.button_pressed_callback, bouncetime = 50)
        GPIO.add_event_detect(self.BTN_GRAY, GPIO.BOTH, callback = self.button_pressed_callback, bouncetime = 50)
        
        self.red_btn_fire = False
        self.green_btn_fire = False
        self.blue_btn_fire = False
        self.yellow_btn_fire = False
        self.gray_btn_fire = False
        
        self.btn_red_count = 0

    def button_pressed_callback(self, channel):

        self.button_working = True
        
        # red button
        if channel == self.BTN_RED and GPIO.input(self.BTN_RED) and not self.red_btn_fire:
            self.red_btn_fire = True
            self.red_button_fired()
        else:
            self.red_btn_fire = False
            
        # green button
        if channel == self.BTN_GREEN and GPIO.input(self.BTN_GREEN) and not self.green_btn_fire:
            self.green_btn_fire = True
            self.green_button_fired()
        else:
            self.green_btn_fire = False
            
        # blue button
        if channel == self.BTN_BLUE and GPIO.input(self.BTN_BLUE) and not self.blue_btn_fire:
            self.blue_btn_fire = True
            self.blue_button_fired()
        else:
            self.blue_btn_fire = False
            
        # yellow button
        if channel == self.BTN_YELLOW and GPIO.input(self.BTN_YELLOW) and not self.yellow_btn_fire:
            self.yellow_btn_fire = True
            self.yellow_button_fired()
        else:
            self.yellow_btn_fire = False
            
        # gray button
        if channel == self.BTN_GRAY and GPIO.input(self.BTN_GRAY) and not self.gray_btn_fire:
            self.gray_btn_fire = True
            self.gray_button_fired()
        else:
            self.gray_btn_fire = False
            
        self.button_working = False

    def red_button_fired(self):
        self.lcd_string(str(datetime.datetime.now()),self.LCD_LINE_1)
        self.lcd_string("red fired", self.LCD_LINE_2)

    def green_button_fired(self):
        self.lcd_string(str(datetime.datetime.now()),self.LCD_LINE_1)
        self.lcd_string("green fired", self.LCD_LINE_2)

    def blue_button_fired(self):
        self.lcd_string(str(datetime.datetime.now()),self.LCD_LINE_1)
        self.lcd_string("blue fired", self.LCD_LINE_2)

    def yellow_button_fired(self):
        self.lcd_string(str(datetime.datetime.now()),self.LCD_LINE_1)
        self.lcd_string("yellow fired", self.LCD_LINE_2)

    def gray_button_fired(self):
        self.lcd_string(str(datetime.datetime.now()),self.LCD_LINE_1)
        self.lcd_string("gray fired", self.LCD_LINE_2)
 
    def lcd_init(self):
        # Initialise display
        self.lcd_byte(0x33, self.LCD_CMD) # 110011 Initialise
        self.lcd_byte(0x32, self.LCD_CMD) # 110010 Initialise
        self.lcd_byte(0x06, self.LCD_CMD) # 000110 Cursor move direction
        self.lcd_byte(0x0C, self.LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
        self.lcd_byte(0x28, self.LCD_CMD) # 101000 Data length, number of lines, font size
        self.lcd_byte(0x01, self.LCD_CMD) # 000001 Clear display
        time.sleep(self.E_DELAY)

    def lcd_byte(self, bits, mode):
        # Send byte to data pins
        # bits = data
        # mode = True  for character
        #        False for command

        GPIO.output(self.LCD_RS, mode) # RS
        # High bits
        GPIO.output(self.LCD_D4, False)
        GPIO.output(self.LCD_D5, False)
        GPIO.output(self.LCD_D6, False)
        GPIO.output(self.LCD_D7, False)
        if bits&0x10==0x10:
            GPIO.output(self.LCD_D4, True)
        if bits&0x20==0x20:
            GPIO.output(self.LCD_D5, True)
        if bits&0x40==0x40:
            GPIO.output(self.LCD_D6, True)
        if bits&0x80==0x80:
            GPIO.output(self.LCD_D7, True)

        # Toggle 'Enable' pin
        self.lcd_toggle_enable()

        # Low bits
        GPIO.output(self.LCD_D4, False)
        GPIO.output(self.LCD_D5, False)
        GPIO.output(self.LCD_D6, False)
        GPIO.output(self.LCD_D7, False)
        if bits&0x01==0x01:
            GPIO.output(self.LCD_D4, True)
        if bits&0x02==0x02:
            GPIO.output(self.LCD_D5, True)
        if bits&0x04==0x04:
            GPIO.output(self.LCD_D6, True)
        if bits&0x08==0x08:
            GPIO.output(self.LCD_D7, True)

        # Toggle 'Enable' pin
        self.lcd_toggle_enable()
     
    def lcd_toggle_enable(self):

        # Toggle enable
        time.sleep(self.E_DELAY)
        GPIO.output(self.LCD_E, True)
        time.sleep(self.E_PULSE)
        GPIO.output(self.LCD_E, False)
        time.sleep(self.E_DELAY)
     
    def lcd_string(self, message,line):
        # Send string to display

        message = message.ljust(self.LCD_WIDTH," ")

        self.lcd_byte(line, self.LCD_CMD)

        for i in range(self.LCD_WIDTH):
            self.lcd_byte(ord(message[i]),self.LCD_CHR)
  
        
    def waiting_loop(self):
        
        self.lcd_init()
        
        last_time = datetime.datetime.now()
        passe_no = 0
        self.lcd_string(str(datetime.datetime.now()), self.LCD_LINE_1)
        self.lcd_string("Welcome         ", self.LCD_LINE_2)
        
        pause_time = 10
        
        while True:
            elapsed = (datetime.datetime.now() - last_time).total_seconds()
            
            if elapsed >= pause_time:
                while self.button_working:
                    time.sleep(0.1)
                self.lcd_string(str(datetime.datetime.now()),self.LCD_LINE_1)
                self.lcd_string("                ", self.LCD_LINE_2)
                last_time = datetime.datetime.now()
                time.sleep(pause_time -0.5)
            
        
if __name__ == '__main__':
    
    timbreuse = Timbreuse()
    print("program started")
    timbreuse.waiting_loop()
        
        
