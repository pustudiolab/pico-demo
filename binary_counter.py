"""
Basic demo for the board: binary counting with variable
    speed using pot 0
"""

#### IMPORT ############################################

from machine import Pin, ADC
from random import randint
import math
import utime


#### VARIABLES AND FUNCTIONS ###########################

leds = [0, 1, 2, 3, 4, 5, 6, 7]
for x in range(len(leds)):
    leds[x] = Pin(x, Pin.OUT)

# speaker is pin 15

indicator = Pin(21, Pin.OUT)

rgbs = [18, 19, 20]
for x in range(len(rgbs)):
    rgbs[x] = Pin(rgbs[x], Pin.OUT)
    
buttons = [13, 12, 11, 10]
for x in range(len(buttons)):
    buttons[x] = Pin(buttons[x], Pin.IN, Pin.PULL_UP)
    
program_button = Pin(14, Pin.IN, Pin.PULL_UP)

# light sensor is ADC(26)
pot1 = ADC(27)


# -------------------------------------------
    
def BinaryDisplay(num, its):
    #clear
    for x in range(8):
        leds[x].off()
    if num >= 1:
        BinaryDisplay(num // 2, its + 1)
        if num % 2 == 1:
            leds[its].on()
        else:
            leds[its].off()
             
        
##### LOOP #############################################        

while True:
    end_program = False
    for step in range(255):       
        if program_button.value() == 0:
                utime.sleep(0.1)
                if program_button.value() == 0:
                    end_program = True
                    break

        BinaryDisplay(step,0)
        raw_value = pot1.read_u16() / 65535
        # the potentiometer output is nonlinear,
        #  the exponential below corrects
        speedFactor = 1 - (math.pow(raw_value, 0.1))
        utime.sleep(speedFactor + 0.1)
        print(step, speedFactor)

        if not buttons[0].value():
            break
    if end_program:
        break
#              
# 
#     for pin in range(1, 30):
#         print(pin)
#         for x in range(1, 30):
#             Pin(x, Pin.OUT).off()
#         Pin(pin, Pin.OUT).on()
#         utime.sleep(1)
#     print()
#     utime.sleep(.25)
                  

# RGB Test ----------------------------
#     rgbs[randint(0, 2)].toggle()
#     utime.sleep(1)
                  

# Pots Test ---------------------------
#     print(pot0.read_u16())
#     print(pot1.read_u16())
#     utime.sleep(0.2)


#######################################################