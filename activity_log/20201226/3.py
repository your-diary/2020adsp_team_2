# 3.py
# 結果: r,g,b,r+g,r+b,g+b,r+g+bの順に点灯するのを繰り返す

import time

import gpiozero as gz

output_pin: dict = {
    'red':   24,
    'green': 18,
    'blue':  23,
}
interval_sec:    int  = 1

led_red:   gz.LED = gz.LED(output_pin['red'])
led_green: gz.LED = gz.LED(output_pin['green'])
led_blue:  gz.LED = gz.LED(output_pin['blue'])

def led_toggle(led_list: list) -> None:
    if (type(led_list) != list):
        led_list = [led_list]
    for led in led_list:
        led.toggle()

def led_blink(*args, **kwargs) -> None:
    for i in range(2):
        led_toggle(*args, **kwargs)
        time.sleep(interval_sec)

while (True):

    print('r')
    led_blink(led_red)

    print('g')
    led_blink(led_green)

    print('b')
    led_blink(led_blue)

    print('rg')
    led_blink([led_red, led_green])

    print('rb')
    led_blink([led_red, led_blue])

    print('gb')
    led_blink([led_green, led_blue])

    print('rgb')
    led_blink([led_red, led_green, led_blue])
