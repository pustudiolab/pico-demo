from machine import Pin, ADC, PWM
import utime

def binary_display(led_list: list, number_to_display: int):
    '''
    Displays a number in binary using the line of onboard LEDs located above the line of buttons.
    
    Args:
        led_list: 8 element list representing the 8 onboard LEDs labelled respectively 1, 2, 4, 8, 16, 32, 64, & 128
        number_to_display: the number to display in binary on the onboard LEDs
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
        rgb_list[idx].duty_u16(int((1 - rgb_tuple[idx]) * 65535))
        
leds = [7, 6, 5, 4, 3, 2, 1, 0]
for x in range(len(leds)):
    leds[x] = Pin(leds[x], Pin.OUT)
    
rgb = [18, 19, 20]
for x in range(len(rgb)):
    rgb[x] = PWM(Pin(rgb[x]))
    rgb[x].freq(1000)
    
buttons = [10, 11, 12, 13, 14]
for x in range(len(buttons)):
    buttons[x] = Pin(buttons[x], Pin.IN, Pin.PULL_UP)

while True:  
    for k in range(3):
        utime.sleep(0.1)
        if k == 0:
            RGB_display(rgb, [0.25, 0, 0])
        elif k == 1:
            RGB_display(rgb, [0, 0.25, 0])
        else:
            RGB_display(rgb, [0, 0, 0.25])
        
        if not buttons[4].value():
            break