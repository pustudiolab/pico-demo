from machine import Pin, ADC, PWM
import utime

pr = ADC(Pin(26))

leds = [7, 6, 5, 4, 3, 2, 1, 0]
for x in range(len(leds)):
    leds[x] = Pin(leds[x], Pin.OUT)

speaker = PWM(Pin(15))

buttons = [10, 11, 12, 13, 14]
for x in range(len(buttons)):
    buttons[x] = Pin(buttons[x], Pin.IN, Pin.PULL_UP)

# These values represent the lowest and highest readings, and
# the actual reading will be a percentage between these two
mxsf = 0
mnsf = 65536
raw_readings = []
while True:
    utime.sleep(0.01)
    raw_readings.append(pr.read_u16())
    if len(raw_readings) > 1000:
        raw_readings = raw_readings[1:]
    
    if (len(raw_readings) < 10):
        continue

    raw_reading = sum(raw_readings[-10:]) / 10
    mxsf = max(raw_readings)
    mnsf = min(raw_readings)

    # Value from 0 to 1 
    value = (mxsf - raw_reading) / (abs(mxsf-mnsf)+1)
    light_level = round(8 * value)
    if mnsf < mxsf:
        for led in leds[0:light_level-1]:
            led.on()
        for led in leds[light_level:]:
            led.off()

    # play on the speaker if rightmost button pressed
    if not buttons[0].value():
        freq = max(440.*8*(mxsf-raw_reading)/(abs(mxsf)+1), 130.81)
        speaker.freq(round(freq))
        speaker.duty_u16(2 ** 15)
    else:
        speaker.duty_u16(0)
    print(mnsf,raw_reading,mxsf)
    
speaker.deinit()