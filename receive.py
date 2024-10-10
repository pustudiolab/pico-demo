from machine import UART, Pin, ADC
import time

uart1 = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9), timeout=5)
uart0 = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17), timeout=5)

leds = list(range(8))
for x in range(len(leds)):
    leds[x] = Pin(7-x, Pin.OUT)

uart1 = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
uart0 = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17))

pot0 = ADC(27)

board_led = Pin(25, Pin.OUT)

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

rxData = bytes()
prevres = -1
while True:
    board_led.on()
    rxData = uart0.readline()
    board_led.off()
    if rxData is None:
        rxData = uart1.readline()
    if not rxData is None:
        try:
            print(rxData.decode('utf-8'))
            size = len(rxData)
            result = int(rxData[:size])
            if prevres != result:
                binary_display(leds,(1<<min(max(result,0),8))-1)
            prevres = result
            rxData = bytes()
        except:
            pass
