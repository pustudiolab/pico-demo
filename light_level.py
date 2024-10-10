from machine import Pin, ADC, PWM
import utime

pr = ADC(Pin(26))

leds = [7, 6, 5, 4, 3, 2, 1, 0]
for x in range(len(leds)):
    leds[x] = Pin(leds[x], Pin.OUT)

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

speaker = PWM(Pin(15))

buttons = [10, 11, 12, 13, 14]
for x in range(len(buttons)):
    buttons[x] = Pin(buttons[x], Pin.IN, Pin.PULL_UP)

mxsf = 0
mnsf = 65536
while True:
    utime.sleep(0.05)
    reading = pr.read_u16()
    freq = max(440.*8*(mxsf-reading)/(abs(mxsf)+1), 130.81)
    mxsf = (mxsf + max(reading, mxsf)) / 2.
    mnsf = (mnsf + min(reading, mnsf)) / 2.
    light_level = round(8.*(mxsf-reading)/(abs(mxsf-mnsf)+1))
    if mnsf < mxsf:
        binary_display(leds,(1<<min(max(light_level,0),8))-1)
    if not buttons[0].value():
        speaker.freq(round(freq))
        speaker.duty_u16(2 ** 15)
    else:
        speaker.duty_u16(0)
    print(mnsf,reading,mxsf)
    
speaker.deinit()