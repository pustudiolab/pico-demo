from machine import Pin, PWM, ADC
import utime

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
    input = (15 - int(buttons_list[0].value())\n                        - 2 * int(buttons_list[1].value())\n                        - 4 * int(buttons_list[2].value())\n                        - 8 * int(buttons_list[3].value()))
    return input

def wait_no_input(BufferTime: float, buttons_list: list, program_button: Pin):
    while True:
        utime.sleep(0.05)
        if get_button_input_8bit(buttons_list) == 0 and program_button.value() == 1:
            utime.sleep(BufferTime)
            if get_button_input_8bit(buttons_list) == 0 and program_button.value() == 1:
                break