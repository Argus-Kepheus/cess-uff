# Project Pinout

For the full board/module identification and selection rationale (why
ESP32-DevKitC V4 specifically, WROOM vs. WROVER compatibility, electrical
characteristics), see
[`docs/hardware-reference.md`](hardware-reference.md).

## 1. Target Board

| Property | Specification |
|---|---|
| Board | Espressif ESP32-DevKitC V4 |
| Wokwi part identifier | `board-esp32-devkit-c-v4` |
| Recommended physical module | ESP32-WROOM-32E |
| Header layout | 38 pins, 19 pins per side |
| Firmware | MicroPython for ESP32 |
| GPIO logic level | 3.3 V |

All source-code and circuit references use the ESP32 GPIO number. They do
not represent the sequential physical position of a terminal on the board
header.

For example, `GPIO25` means the microcontroller signal named GPIO25, not
the twenty-fifth physical terminal of the development board.

## 2. Project GPIO Assignment

| Function | Wokwi component ID | Python variable | Python constant | GPIO | Physical header |
|---|---|---|---|---:|---|
| Red LED output | `red-led` | `red_led` | `RED_LED_PIN` | GPIO2 | J3-15 |
| Green LED output | `green-led` | `green_led` | `GREEN_LED_PIN` | GPIO4 | J3-13 |
| Push-button input | `push-button` | `push_button` | `BUTTON_PIN` | GPIO17 | J3-11 |
| OLED I²C data | `oled-display` | `oled_display` | `OLED_SDA_PIN` | GPIO16 | J3-12 |
| OLED I²C clock | `oled-display` | `oled_display` | `OLED_SCL_PIN` | GPIO25 | J2-9 |

The corresponding firmware constants are:

```python
RED_LED_PIN = 2
GREEN_LED_PIN = 4
BUTTON_PIN = 17
OLED_SDA_PIN = 16
OLED_SCL_PIN = 25
```

## 3. Power and Ground Connections

| Peripheral terminal | ESP32 connection | Purpose |
|---|---|---|
| OLED `VCC` | `3V3`, J2-1 | OLED power supply |
| OLED `GND` | Any available `GND` | Common electrical reference |
| Red LED cathode | `GND` | LED current return |
| Green LED cathode | `GND` | LED current return |
| Push-button supply side | `3V3` | Produces HIGH when pressed |

All peripherals must share the same ground reference.

The OLED and push-button must use the 3.3 V rail. ESP32 GPIO terminals are
not 5 V tolerant.

## 4. Red LED Connection

The red LED is controlled by GPIO2.

```text
GPIO2 ── 220 Ω resistor ── LED anode
LED cathode ── GND
```

The current-limiting resistor is represented in Wokwi by:

```text
Component ID: red-led-resistor
Resistance: 220 Ω
```

The red LED alternates its state every 500 milliseconds:

| Interval | Red LED state |
|---:|---|
| First 500 ms | ON |
| Next 500 ms | OFF |
| Following intervals | Repeated continuously |

A complete ON/OFF cycle lasts approximately one second.

The red LED runs as an independent asynchronous task and must continue
blinking regardless of the button, green LED, or OLED state.

GPIO2 is an ESP32 bootstrapping pin. The project assignment is valid, but
a physical circuit must not force an unsuitable logic level on GPIO2
during startup. The series resistor and LED connection used in this
project do not intentionally drive the pin externally.

## 5. Green LED Connection

The green LED is controlled by GPIO4.

```text
GPIO4 ── 220 Ω resistor ── LED anode
LED cathode ── GND
```

The current-limiting resistor is represented in Wokwi by:

```text
Component ID: green-led-resistor
Resistance: 220 Ω
```

The green LED follows the debounced logical state of the push-button:

| Push-button state | GPIO17 level | Green LED |
|---|---:|---|
| Released | LOW | OFF |
| Pressed | HIGH | ON |

## 6. Push-Button Connection

The project uses a normally open momentary push-button connected between
3.3 V and GPIO17.

```text
3V3 ── normally open push-button ── GPIO17
```

The GPIO is configured as an input with the ESP32 internal pull-down
resistor:

```python
push_button = Pin(
    BUTTON_PIN,
    Pin.IN,
    Pin.PULL_DOWN,
)
```

This configuration produces the required active-high behavior:

| Mechanical state | Electrical condition | GPIO17 level |
|---|---|---:|
| Released | Contact open | LOW |
| Pressed | GPIO17 connected to 3.3 V | HIGH |

No external pull-down resistor is required.

No external RC debounce filter is included. Mechanical contact bounce is
handled by non-blocking software debounce.

The adopted debounce strategy periodically samples the input and accepts a
change only after the new level remains stable for approximately 30 ms.

```python
BUTTON_SAMPLE_INTERVAL_MS = 5
BUTTON_DEBOUNCE_MS = 30
```

## 7. OLED Connection

The project uses an SSD1306 OLED display with an I²C interface.

| OLED terminal | ESP32 connection | Project constant |
|---|---|---|
| `SCL` | GPIO25, J2-9 | `OLED_SCL_PIN` |
| `SDA` | GPIO16, J3-12 | `OLED_SDA_PIN` |
| `VCC` | 3.3 V, J2-1 | Not applicable |
| `GND` | GND | Not applicable |

The adopted MicroPython configuration is:

```python
i2c = SoftI2C(
    scl=Pin(OLED_SCL_PIN),
    sda=Pin(OLED_SDA_PIN),
    freq=400_000,
)
```

A software (bit-banged) `SoftI2C` bus is used instead of the hardware `I2C`
peripheral. This is a defensive compatibility choice for Wokwi's simulated
ESP32 — see `docs/technical-specification.md`, §16 decision log, including
the note that this still needs to be confirmed against a live wokwi.com
run.

The GPIO assignment is a predefined project requirement:

```text
GPIO25 = SCL
GPIO16 = SDA
```

This mapping was not selected as an optimization and must not be silently
replaced with the common ESP32 default I²C pins.

It must be declared consistently in:

- `main.py`;
- `diagram.json`;
- `README.md`;
- `docs/project-pinout.md`;
- `docs/technical-specification.md`;
- any submitted circuit diagram.

The Wokwi OLED uses the following address:

```python
OLED_I2C_ADDRESS = 0x3C
```

The simulated display dimensions are:

```python
OLED_WIDTH = 128
OLED_HEIGHT = 64
```

## 8. OLED Messages

The displayed messages must remain exactly in Portuguese:

| Stable push-button state | OLED message |
|---|---|
| Released | `Boa sorte!!` |
| Pressed | `Consegui!` |

The OLED is initialized with the message corresponding to the current
button state.

After initialization, the framebuffer is transmitted only when the stable
button state changes.

This event-driven update strategy avoids:

- unnecessary I²C traffic;
- unnecessary processor usage;
- repeated framebuffer transmissions;
- visible display flickering;
- additional latency in other asynchronous tasks.

## 9. Consolidated Functional State Table

| Stable button state | Red LED | Green LED | OLED message |
|---|---|---|---|
| Released | Blinks independently | OFF | `Boa sorte!!` |
| Pressed | Blinks independently | ON | `Consegui!` |

The red LED behavior is independent of all button-controlled outputs.

## 10. Wokwi Circuit Identifiers

The following identifiers must be used in `diagram.json`:

| Component | Required Wokwi ID |
|---|---|
| ESP32 board | `esp32` |
| Red LED | `red-led` |
| Red LED resistor | `red-led-resistor` |
| Green LED | `green-led` |
| Green LED resistor | `green-led-resistor` |
| Push-button | `push-button` |
| OLED display | `oled-display` |

Python identifiers cannot contain hyphens. Therefore, the source code uses
underscores:

```python
red_led
green_led
push_button
oled_display
```

## 11. Reserved Flash Terminals

The following ESP32-DevKitC V4 terminals must not be used by this project:

- `CLK`;
- `D0`;
- `D1`;
- `D2`;
- `D3`;
- `CMD`.

These terminals correspond to signals used internally for SPI flash
communication.

Using them as general-purpose inputs or outputs can prevent the firmware
from starting or operating correctly.

## 12. Module Compatibility

GPIO16 and GPIO17 are required by the project.

These GPIOs are available for normal use on ESP32-DevKitC V4 boards fitted
with an ESP32-WROOM module.

On ESP32-WROVER-based versions, GPIO16 and GPIO17 may be assigned to the
external PSRAM interface and may therefore be unavailable.

The recommended physical target is:

```text
Espressif ESP32-DevKitC V4
Module: ESP32-WROOM-32E
```

The following configuration should be avoided for the exact project
pinout:

```text
ESP32-DevKitC V4 with ESP32-WROVER module
```

## 13. Physical Wiring Checklist

Before powering a physical implementation, verify that:

- the board is an ESP32-DevKitC V4 or a fully compatible equivalent;
- the module provides GPIO16 and GPIO17 for general-purpose use;
- the OLED is powered from 3.3 V;
- all grounds are connected together;
- each LED includes a 220 Ω series resistor;
- the red LED is connected to GPIO2;
- the green LED is connected to GPIO4;
- the push-button is connected between GPIO17 and 3.3 V;
- no external pull-up resistor is connected to GPIO17;
- OLED SDA is connected to GPIO16;
- OLED SCL is connected to GPIO25;
- no peripheral is connected to `CLK`, `D0`, `D1`, `D2`, `D3`, or `CMD`;
- no GPIO terminal receives 5 V.
