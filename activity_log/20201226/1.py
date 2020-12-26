# 1.py
# 結果: LEDが付いたり消えたりする

import time

import gpiozero as gz

output_pin:   int = 23
interval_sec: int = 1

led: gz.LED = gz.LED(output_pin)

while (True):
    print('ON')
    led.on()
    time.sleep(interval_sec)
    print('OFF')
    led.off()
    time.sleep(interval_sec)
