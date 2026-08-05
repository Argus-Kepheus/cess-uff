"""
TEMPORARY test script — red LED blink only.

Purpose: isolate the red LED (GPIO 2) from the rest of the application
(push-button, green LED, OLED) to confirm the wiring and the ~500 ms
blink behavior work on their own, without any of the other moving parts
that could mask a wiring or timing problem.

This is NOT part of the graded deliverable — it exists only to validate
diagram.json's red LED wiring in isolation. Delete it (or leave it out of
the submission) once the blink is confirmed.

How to use on wokwi.com:
  1. Open the project and back up the real main.py content somewhere
     (e.g. keep the repository's main.py open in another tab/editor).
  2. Replace the online main.py's content with this file's content.
  3. Start the simulation and confirm the red LED toggles every 500 ms,
     continuously, with no other component involved.
  4. Restore the original main.py before continuing with the rest of
     the project.

Deliberately uses a plain blocking loop (no asyncio, no ssd1306 import,
no button) so a failure here can only mean a GPIO/wiring/board issue,
not an application-logic issue.
"""

from machine import Pin
import time

RED_LED_PIN = 2
BLINK_INTERVAL_MS = 500

red_led = Pin(RED_LED_PIN, Pin.OUT, value=0)

print("Red LED blink test starting on GPIO {}".format(RED_LED_PIN))

while True:
    red_led.value(not red_led.value())
    print("Red LED:", "ON" if red_led.value() else "OFF")
    time.sleep_ms(BLINK_INTERVAL_MS)
