from machine import Pin, ADC, PWM
import utime

pot = ADC(Pin(27))
speaker = PWM(Pin(15))

buttons = [10, 11, 12, 13, 14]
for x in range(len(buttons)):
    buttons[x] = Pin(buttons[x], Pin.IN, Pin.PULL_UP)

sleap_time = 0.1
while True:
    utime.sleep(sleap_time)
    reading = pot.read_u16()
    print(reading)
    freq = max(440. * 4 * reading / 65536., 130.81)
    speaker.freq(round(freq))
    speaker.duty_u16(2 ** 15)
    
    if not buttons[0].value():
        sleap_time = 0.025
    elif not buttons[1].value():
        sleap_time = 0.05
    elif not buttons[2].value():
        sleap_time = 0.1
    elif not buttons[3].value():
        sleap_time = 0.2
    elif not buttons[4].value():
        break
    
speaker.deinit()