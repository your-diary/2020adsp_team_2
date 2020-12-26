# 2.py
# 結果: LEDが徐々に明るくなり、今度は徐々に暗くなり、を繰り返す

import time

import gpiozero as gz

output_pin:       int   = 23
interval_sec:     int   = 1
delta_brightness: float = 0.01
wait_sec:         float = 0.5

led: gz.LED = gz.PWMLED(output_pin)

brightness: float = led.value
should_add_brightness: bool = True

while (True):

    if (should_add_brightness):
        brightness += delta_brightness
    else:
        brightness -= delta_brightness

    if (brightness > 1):
        should_add_brightness = False
        brightness = 1
        time.sleep(wait_sec)
    elif (brightness < 0):
        should_add_brightness = True
        brightness = 0
        time.sleep(wait_sec)

    led.value = brightness

    time.sleep(interval_sec * delta_brightness)
