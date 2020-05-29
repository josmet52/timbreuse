#!/usr/bin/env python3
# -*-

import RPi.GPIO as GPIO
import time, datetime

# initialise buttons adress
BTN_RED = 6
BTN_GREEN = 19
BTN_BLUE = 26
BTN_YELLOW = 13
BTN_GRAY = 5
    
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers

# initialise the GPIO buttons inputs
GPIO.setup(BTN_RED, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(BTN_GREEN, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(BTN_BLUE, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(BTN_YELLOW, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(BTN_GRAY, GPIO.IN, GPIO.PUD_DOWN)

# pour la mesure de la durée de l'impulsion
time_btn_pressed = 0
pulse_length_soll = 400


# procédure appelée lors de la pression sur une boutons
def button_pressed_callback(channel):

    # empêcher la idle_task d'accéder à l'affichage
    button_working = True
        
    # green button
    if channel == BTN_GREEN and GPIO.input(BTN_GREEN) and not green_btn_fire:
        time_btn_pressed = datetime.datetime.now()
        green_btn_fire = True
        green_button_fired()
        pulse_length_ist = 0
#             while pulse_length_ist < pulse_length_soll:
#                 pulse_length_ist = int((datetime.datetime.now() - time_btn_pressed).microseconds / 1000)
#                 print(pulse_length_ist)
        
        print("Pressed: GPIO.input(BTN_GREEN)",GPIO.input(BTN_GREEN))
    elif channel == BTN_GREEN and green_btn_fire:
        green_btn_fire = False
        pulse_length_ist = int((datetime.datetime.now() - time_btn_pressed).microseconds / 1000)
        print("Release: GPIO.input(BTN_GREEN)",GPIO.input(BTN_GREEN))
        print(pulse_length_ist)
        if pulse_length_ist > pulse_length_soll : 
            yellow_button_fired()

def init():
#     # initialise buttons adress
#     BTN_RED = 6
#     BTN_GREEN = 19
#     BTN_BLUE = 26
#     BTN_YELLOW = 13
#     BTN_GRAY = 5
#         
#     GPIO.setwarnings(False)
#     GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
# 
#     # initialise the GPIO buttons inputs
#     GPIO.setup(BTN_RED, GPIO.IN, GPIO.PUD_DOWN)
#     GPIO.setup(BTN_GREEN, GPIO.IN, GPIO.PUD_DOWN)
#     GPIO.setup(BTN_BLUE, GPIO.IN, GPIO.PUD_DOWN)
#     GPIO.setup(BTN_YELLOW, GPIO.IN, GPIO.PUD_DOWN)
#     GPIO.setup(BTN_GRAY, GPIO.IN, GPIO.PUD_DOWN)

    # initialise buttons interrupts
    GPIO.add_event_detect(BTN_RED, GPIO.BOTH, callback = button_pressed_callback, bouncetime = 50)
    GPIO.add_event_detect(BTN_GREEN, GPIO.BOTH, callback = button_pressed_callback, bouncetime = 50)
    GPIO.add_event_detect(BTN_BLUE, GPIO.BOTH, callback = button_pressed_callback, bouncetime = 50)
    GPIO.add_event_detect(BTN_YELLOW, GPIO.BOTH, callback = button_pressed_callback, bouncetime = 50)
    GPIO.add_event_detect(BTN_GRAY, GPIO.BOTH, callback = button_pressed_callback, bouncetime = 50)

    # flags pour gestion des boutons sans rebonds
    red_btn_fire = False
    green_btn_fire = False
    blue_btn_fire = False
    yellow_btn_fire = False
    gray_btn_fire = False
# 
#     # pour la mesure de la durée de l'impulsion
#     time_btn_pressed = 0
#     pulse_length_soll = 400

def waiting_loop():
    n_loop = 0
    elapsed = 0
    while True:
        last_time = datetime.datetime.now()
        while elapsed < 10:
            elapsed = (datetime.datetime.now() - last_time).total_seconds()
#             print(elapsed)
        print(n_loop)
        n_loop += 1
        elapsed = 0
        
if __name__ == '__main__':
    init()
    waiting_loop()

