#!/usr/bin/env python3
# -*-

import RPi.GPIO as GPIO
import time

class GpioTimbreuse:
    
    """
        Cette classe gere le GPIO pour la timbreuse jMb
    """

    def __init__(self):
        
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
        self.BTN_RED = 6
        self.BTN_GREEN = 19
        self.BTN_BLUE = 26
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
        
        # initialise the GPIO buttons inputs
        GPIO.setup(self.BTN_RED, GPIO.IN, GPIO.PUD_DOWN)
        GPIO.setup(self.BTN_GREEN, GPIO.IN, GPIO.PUD_DOWN)
        GPIO.setup(self.BTN_BLUE, GPIO.IN, GPIO.PUD_DOWN)
        GPIO.setup(self.BTN_YELLOW, GPIO.IN, GPIO.PUD_DOWN)
        GPIO.setup(self.BTN_GRAY, GPIO.IN, GPIO.PUD_DOWN)
        
 
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
  
