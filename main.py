#### IMPORT ############################################

from machine import Pin, PWM, ADC
from random import randint
import utime

#### VARIABLES AND FUNCTIONS ###########################

leds = [7, 6, 5, 4, 3, 2, 1, 0]
for x in range(len(leds)):
    leds[x] = Pin(leds[x], Pin.OUT)
    
rgb = [20, 19, 18]
for x in range(len(rgb)):
    rgb[x] = PWM(Pin(rgb[x]))
    rgb[x].freq(1000)
    
buttons = [10, 11, 12, 13]
for x in range(len(buttons)):
    buttons[x] = Pin(buttons[x], Pin.IN, Pin.PULL_UP)
    
pot = ADC(27)

program_led = Pin(21, Pin.OUT)
program_led.on()

program_button = Pin(14, Pin.IN, Pin.PULL_UP)

pico_led = Pin(25, Pin.OUT)
pico_led.on()

def binary_display(led_list, number_to_display):
    '''
    Display a number on the main leds
    '''
    __binary_display_recur(led_list, number_to_display, 0)

def __binary_display_recur(led_list: list, number_to_display: int, its: int):
    '''
    DO NOT TOUCH THIS FUNCTION
    Recursive function for displaying binary on the onboard LEDs.
    Use the wrapper function Binary_display.
    '''
    #clear
    for x in range(8):
        led_list[x].off()
    if number_to_display >= 1:
        __binary_display_recur(led_list, number_to_display // 2, its + 1)
    if number_to_display % 2 == 1:
        led_list[7 - its].on()
    else:
        led_list[7 - its].off()
        
def RGB_display(rgb_list: list, rgb_tuple: tuple):
    '''
    Displays a color on the onboard RGB LED, located on the left-hand edge
    
    Args:
        rgb_list: list of objects representing the red, green, & blue pins
        rgb_tuple: tuple of floats in interval [0, 1], representing the intensities of red, green, & blue components
    '''
    for idx in range(3):
        # We subtract from 1 because the RGB LED is common-anode
        rgb_list[idx].duty_u16((1 - rgb_tuple[idx]) * 65535)

def get_button_input_8bit(buttons_list: list):
    input = 15 - int(buttons_list[0].value()) - 2 * int(buttons_list[1].value()) - 4 * int(buttons_list[2].value())   - 8 * int(buttons_list[3].value())
    return input

def wait_no_input(BufferTime: float, buttons_list: list, program_button: Pin):
    while True:
        utime.sleep(0.05)
        if get_button_input_8bit(buttons_list) == 0 and program_button.value() == 1:
            utime.sleep(BufferTime)
            if get_button_input_8bit(buttons_list) == 0 and program_button.value() == 1:
                break

# -------------------------------------------

programs = []
with open('programs.txt','r') as file:
    for line in file:
        line = line.rstrip('\n')
        line = line.rstrip('\r')
        programs.append(line.split(','))

while True:
    pico_led.on()
    program_led.on()
    binary_display(leds, 0)
    
    def get_prog_num(light_level):
        return (1<<min(max(light_level,0),8))-1

    # Select program
    # - uses average of last ten pot readings and converts to binary
    # - only updates when value changes
    prog_num = -1
    readings = []
    while program_button.value() == 1:
        readings.append(pot.read_u16())
        if (len(readings) > 100):
            readings = readings[1:]
        avg_reading = sum(readings)/len(readings)
        light_level = round(8.*(avg_reading)/65536.)
        if prog_num == -1 or get_prog_num(light_level) != prog_num:
            prog_num = get_prog_num(light_level)
            binary_display(leds, prog_num)
        
    searchnum = min(max(light_level,0),8)
    binary_display(leds, searchnum)
    
    print("Running program: ", searchnum, programs[searchnum-1])
    print(programs)

    try:
        completed = False
        for program in programs:
            if int(program[1]) == searchnum:
                utime.sleep(0.25)
                program_led.off()
                pico_led.off()
                binary_display(leds, 0)
                for count in range(5):
                    RGB_display(rgb, (0, 0, 0))
                    utime.sleep(0.1)
                    RGB_display(rgb, (0, 0, 1))
                    utime.sleep(0.2)
                RGB_display(rgb, (0, 0, 0))
                program_to_run = __import__(program[0])
                completed = True
        if completed:
            continue
        raise Exception('Could not load program')
        
    except Exception as e:
        program_led.on()
        pico_led.on()
        print(e)
        wait_no_input(0.1, buttons, program_button)
        while program_button.value() == 1:
            RGB_display(rgb, (1, 0, 0))
            utime.sleep(0.125)
            if program_button.value() == 0:
                break
            RGB_display(rgb, (0, 0, 0))
            utime.sleep(0.125)
        wait_no_input(0.1, buttons, program_button)
    
#     board_led.off()
#     program_to_run = __import__(progname)