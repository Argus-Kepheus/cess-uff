"""
TEMPORARY test script — push-button + green LED only.

Purpose: isolate the push-button (GPIO 17) and the green LED it drives
(GPIO 4) from the rest of the application (red LED, OLED) to confirm the
wiring and the active-HIGH behavior work on their own.

This is NOT part of the graded deliverable — it exists only to validate
diagram.json's push-button/green-LED wiring in isolation. Delete it (or
leave it out of the submission) once the behavior is confirmed.

How to use on wokwi.com:
  1. Open the project and back up the real main.py content somewhere
     (e.g. keep the repository's main.py open in another tab/editor).
  2. Replace the online main.py's content with this file's content.
  3. Start the simulation. With the button released, the green LED must
     be OFF and the console must print "Button: released". Press and
     hold the button (click it, or focus the diagram and hold Space):
     the green LED must turn ON and the console must print
     "Button: pressed". Release it and confirm it goes back to OFF.
  4. Restore the original main.py before continuing with the rest of
     the project.

Deliberately uses a plain blocking loop (no asyncio, no ssd1306 import,
no red LED, no debounce) so a failure here can only mean a GPIO/wiring
problem with the button or the green LED, not an application-logic issue.
Wokwi's simulated push-button does not bounce, so debounce is not needed
for this isolated hardware check (see docs/technical-specification.md,
section 6.2).
"""

from machine import Pin
import time

GREEN_LED_PIN = 4
BUTTON_PIN = 17
POLL_INTERVAL_MS = 100

green_led = Pin(GREEN_LED_PIN, Pin.OUT, value=0)
push_button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_DOWN)

print("Push-button test starting on GPIO {} (green LED on GPIO {})".format(
    BUTTON_PIN, GREEN_LED_PIN
))

last_state = None

while True:
    current_state = bool(push_button.value())
    if current_state != last_state:
        green_led.value(current_state)
        print("Button:", "pressed" if current_state else "released")
        last_state = current_state
    time.sleep_ms(POLL_INTERVAL_MS)
