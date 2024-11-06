from machine import Pin, PWM
from time import sleep
from math import sin

leds = [7, 6, 5, 4, 3, 2, 1, 0]
for x in range(len(leds)):
    leds[x] = PWM(leds[x])
    leds[x].freq(1000)

rgb = [20, 19, 18]
for x in range(len(rgb)):
    rgb[x] = Pin(rgb[x], Pin.OUT)
    rgb[x].on()

amplitude = 65025

t = 0
while True:
    if t > 2 * amplitude:
        t = 0
    for i, led in enumerate(leds):
        duty = round((t + 5000 * i)) % (2 * amplitude)
        if duty > amplitude:
            led.duty_u16(2 * amplitude - duty)
        else:
            led.duty_u16(duty)
    t += 100
    sleep(0.001)

# while True:
#     for t in range(0, 10000, 1):
#         print(t)
#         for i, led in enumerate(leds):
#             led.duty_u16(round(amplitude * sin(0.005 * (t + 50 * i) + amplitude)))
#         sleep(0.001)