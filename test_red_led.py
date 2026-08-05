from machine import Pin
from time import sleep_ms

RED_LED_PIN = 2
BLINK_INTERVAL_MS = 500

red_led = Pin(RED_LED_PIN, Pin.OUT)
red_led.off()

print("GPIO2 red LED test started")

while True:
    red_led.on()
    print("GPIO2 =", red_led.value(), "- LED ON")
    sleep_ms(BLINK_INTERVAL_MS)

    red_led.off()
    print("GPIO2 =", red_led.value(), "- LED OFF")
    sleep_ms(BLINK_INTERVAL_MS)