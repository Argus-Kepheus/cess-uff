# ESP32-DevKitC V4 Hardware Reference

## 1. Purpose

This document identifies the exact ESP32 development board used by the
CESS-UFF project and records the technical criteria behind its selection.

Its purpose is to eliminate ambiguity between different ESP32 development
boards, module versions, header layouts, and GPIO numbering conventions.

This document complements:

- `README.md`;
- `docs/project-pinout.md`;
- `docs/component-specifications.md`;
- `docs/technical-specification.md`;
- `diagram.json`;
- `main.py`.

## 2. Selected Development Board

| Property | Project definition |
|---|---|
| Manufacturer | Espressif Systems |
| Board name | ESP32-DevKitC V4 |
| Wokwi component type | `board-esp32-devkit-c-v4` |
| Header arrangement | 38 pins, 19 pins per side |
| Microcontroller family | Original ESP32 family |
| Recommended physical module | ESP32-WROOM-32E |
| Firmware environment | MicroPython for ESP32 |
| Logic voltage | 3.3 V |

The board is declared in `diagram.json` as:

```json
{
  "type": "board-esp32-devkit-c-v4",
  "id": "esp32"
}
```

This declaration is part of the circuit definition and must not be replaced
with another board type without reviewing the complete pin mapping.

## 3. Board Selection Rationale

The original project specification requires only:

```text
MicroPython for ESP32
```

It does not mandate a particular ESP32 development board.

The ESP32-DevKitC V4 was selected because it:

- is an official Espressif development board;
- is supported natively by Wokwi;
- exposes every GPIO required by the project;
- has an unambiguous Wokwi component identifier;
- has official manufacturer documentation;
- provides a reproducible 38-pin header arrangement;
- reduces ambiguity associated with generic ESP32 clone boards;
- is suitable for both simulation and future physical implementation.

The selection is therefore based on documentation, reproducibility, and
pin availability rather than on a special performance requirement.

The project functions would also be technically possible on other ESP32
boards, provided that they:

- support MicroPython;
- expose GPIO2, GPIO4, GPIO16, GPIO17, and GPIO25;
- provide 3.3 V logic;
- support I²C communication;
- do not reserve GPIO16 or GPIO17 for another hardware function;
- have their circuit mapping reviewed and documented.

## 4. Why a Generic "ESP32" Description Is Insufficient

The term "ESP32 board" can refer to many different products, including:

- ESP32-DevKitC revisions;
- ESP32 DevKit v1 clone boards;
- NodeMCU-style ESP32 boards;
- boards with 30, 36, or 38 header terminals;
- boards using WROOM modules;
- boards using WROVER modules;
- ESP32-S2, ESP32-S3, ESP32-C3, and ESP32-C6 families.

These boards may differ in:

- physical terminal position;
- available GPIOs;
- flash and PSRAM connections;
- USB interface;
- onboard LEDs;
- boot circuitry;
- module dimensions;
- printed terminal labels.

For this reason, the project must identify both the board and the GPIO
numbers explicitly.

The approved designation is:

```text
Espressif ESP32-DevKitC V4
Wokwi part: board-esp32-devkit-c-v4
```

The project must not be documented only as:

```text
ESP32
```

or:

```text
ESP32 DevKit
```

## 5. Development Board and Module Are Different Items

The development board and the radio module are separate levels of
hardware identification.

### 5.1 Development board

The ESP32-DevKitC V4 includes:

- USB connector;
- USB-to-serial converter;
- voltage regulation;
- reset and boot buttons;
- breakout headers;
- support components;
- an installed ESP32 module.

### 5.2 ESP32 module

The metal-shielded module contains the ESP32 system-on-chip and associated
flash memory, antenna circuitry, and optional PSRAM depending on the
module variant.

A physical ESP32-DevKitC V4 can be fitted with different modules.

For this project, the preferred module is:

```text
ESP32-WROOM-32E
```

This choice preserves GPIO16 and GPIO17 for the required OLED and
push-button connections.

## 6. WROOM and WROVER Compatibility

The project uses:

```text
GPIO16 = OLED SDA
GPIO17 = push-button input
```

On ESP32-WROOM-based boards, these GPIOs are normally available for
general-purpose use.

On ESP32-WROVER-based boards, GPIO16 and GPIO17 may be connected internally
to the external PSRAM interface.

Therefore:

| Module family | Project compatibility |
|---|---|
| ESP32-WROOM | Recommended |
| ESP32-WROOM-32E | Preferred physical target |
| ESP32-WROVER | Not recommended for the current pin mapping |

A WROVER-based board would require a pin reassignment and corresponding
changes to:

- `main.py`;
- `diagram.json`;
- the circuit wiring;
- project documentation;
- validation tests.

Because GPIO16 and GPIO17 are predefined project assignments, changing
them is outside the current design scope.

## 7. Main Hardware Characteristics

The selected board is based on the original ESP32 family.

Relevant capabilities include:

- 32-bit Xtensa processor architecture;
- Wi-Fi connectivity in the 2.4 GHz band;
- Bluetooth support;
- digital input and output GPIOs;
- configurable internal pull-up and pull-down resistors;
- hardware I²C controllers;
- hardware SPI controllers;
- UART interfaces;
- PWM generation;
- hardware timers;
- interrupt-capable GPIOs;
- MicroPython support.

The current project uses only:

- digital outputs;
- one digital input with an internal pull-down resistor;
- one I²C bus (bit-banged via `SoftI2C`, see §12);
- cooperative asynchronous software tasks.

Wi-Fi, Bluetooth, ADC, DAC, PWM, and hardware timers are not required by
the current specification.

## 8. Electrical Characteristics Relevant to the Project

### 8.1 Logic voltage

ESP32 GPIOs operate at 3.3 V logic levels.

The project must not apply 5 V directly to any GPIO.

### 8.2 Peripheral power

The SSD1306 OLED used by this project is powered from the board 3.3 V
output.

The push-button also connects GPIO17 to 3.3 V when pressed.

### 8.3 Common reference

All components must share a common ground.

Without a common ground, the GPIO voltage levels and I²C signals do not
have a valid shared electrical reference.

### 8.4 LED current limiting

Each external LED uses a 220 Ω series resistor.

The resistor limits GPIO and LED current and must not be omitted in a
physical implementation.

## 9. Header Numbering Convention

The ESP32-DevKitC V4 uses two 19-terminal headers:

- J2;
- J3.

The project primarily references GPIO names rather than physical header
sequence numbers.

Examples:

| Firmware reference | Board terminal |
|---|---|
| `Pin(2)` | GPIO2, J3-15 |
| `Pin(4)` | GPIO4, J3-13 |
| `Pin(17)` | GPIO17, J3-11 |
| `Pin(16)` | GPIO16, J3-12 |
| `Pin(25)` | GPIO25, J2-9 |

GPIO numbering must not be inferred from the physical terminal order.

## 10. Project Pin Summary

| Project function | GPIO | Header position |
|---|---:|---|
| Red LED | GPIO2 | J3-15 |
| Green LED | GPIO4 | J3-13 |
| Push-button | GPIO17 | J3-11 |
| OLED SDA | GPIO16 | J3-12 |
| OLED SCL | GPIO25 | J2-9 |

The authoritative project-specific wiring description is contained in:

```text
docs/project-pinout.md
```

## 11. GPIO Restrictions

### 11.1 Internal flash signals

The following terminals are reserved for internal SPI flash communication:

- `CLK`;
- `D0`;
- `D1`;
- `D2`;
- `D3`;
- `CMD`.

They must not be used as project GPIOs.

### 11.2 Input-only GPIOs

On the original ESP32, GPIO34 through GPIO39 are input-only.

They cannot drive LEDs or other outputs.

These GPIOs also do not provide the same internal pull-up or pull-down
capabilities as the general-purpose bidirectional pins.

### 11.3 Bootstrapping GPIOs

Some GPIOs are sampled during startup to select ESP32 boot configuration.

These include GPIO0, GPIO2, GPIO5, GPIO12, and GPIO15.

The project uses GPIO2 for the red LED because this assignment is part of
the requirements.

The external LED circuit must not force GPIO2 to an unsuitable state while
the ESP32 is starting.

### 11.4 Serial communication GPIOs

GPIO1 and GPIO3 are commonly used by the primary UART for programming,
diagnostic output, and the Wokwi serial monitor.

They are not used by the project peripherals.

## 12. OLED Interface

The SSD1306 display uses I²C.

The required signal assignment is:

```text
GPIO25 = SCL
GPIO16 = SDA
```

This is a predefined project constraint rather than the common default
ESP32 I²C mapping.

The project assigns the I²C controller explicitly, using a software
(bit-banged) bus rather than a hardware I²C peripheral — a defensive
compatibility choice for Wokwi's simulated ESP32 that still needs to be
confirmed against a live wokwi.com run (see `docs/technical-specification.md`,
§16 decision log):

```python
i2c = SoftI2C(
    scl=Pin(25),
    sda=Pin(16),
    freq=400_000,
)
```

The use of I²C requires four OLED connections:

- SCL;
- SDA;
- VCC;
- GND.

Only SCL and SDA are communication signals.

VCC and GND provide power and electrical reference.

## 13. I²C Versus SPI

Some physical SSD1306 modules use SPI instead of I²C.

A typical SPI connection may require:

- SCK;
- MOSI;
- CS;
- DC;
- RST;
- VCC;
- GND.

SPI can provide a higher transfer rate, but it requires more signal
connections and additional GPIO assignments.

The project does not use SPI because:

- GPIO25 and GPIO16 were predefined for display communication;
- the Wokwi `board-ssd1306` component uses I²C;
- the display contains only short static messages;
- the OLED is updated only when the stable button state changes;
- the additional SPI throughput would not provide a meaningful functional
  advantage for the current application.

The use of I²C is therefore fully adequate for the project.

## 14. Dynamic Display Update Strategy

The OLED is not refreshed continuously.

The framebuffer is transmitted:

1. once during system initialization;
2. whenever the debounced button state changes.

This approach reduces:

- I²C bus traffic;
- processor occupation;
- unnecessary display writes;
- visible flickering;
- interference with the red LED task;
- unnecessary energy consumption.

The strategy is especially appropriate because the messages remain static
between button transitions.

## 15. Asynchronous Software Architecture

The firmware uses MicroPython `asyncio`.

The architecture separates the system into cooperative tasks, including:

- continuous red LED blinking;
- periodic push-button sampling;
- software debounce;
- event-driven green LED control;
- event-driven OLED updates.

Blocking delays such as the following are intentionally avoided:

```python
time.sleep(0.5)
```

The project uses cooperative delays instead:

```python
await asyncio.sleep_ms(500)
```

The asynchronous approach was selected because it:

- separates independent responsibilities;
- improves readability;
- improves maintainability;
- simplifies future expansion;
- prevents simple delays from freezing all functions;
- accommodates possible I²C display latency;
- allows additional sensors and actuators to be integrated later.

## 16. Wokwi Representation

The virtual board is defined by:

```json
"type": "board-esp32-devkit-c-v4"
```

The Wokwi simulation contains:

- one ESP32-DevKitC V4;
- one red LED;
- one green LED;
- two 220 Ω resistors;
- one normally open push-button;
- one SSD1306 I²C OLED.

The circuit topology and all virtual connections are stored in:

```text
diagram.json
```

The Wokwi component IDs are:

```text
esp32
red-led
red-led-resistor
green-led
green-led-resistor
push-button
oled-display
```

## 17. Physical Implementation Compatibility

A future physical implementation should use:

```text
Board: Espressif ESP32-DevKitC V4
Module: ESP32-WROOM-32E
Logic level: 3.3 V
```

A physically similar generic board must not be assumed to have an
identical terminal layout.

Before replacing the target board, verify:

- the exact board model;
- the module model;
- the number of header terminals;
- the printed GPIO labels;
- GPIO16 and GPIO17 availability;
- the 3.3 V supply location;
- available GND terminals;
- bootstrapping-pin behavior;
- flash-reserved terminals.

## 18. Reproducibility Requirements

A developer reproducing the project must use the following authoritative
configuration:

```text
Wokwi board:
board-esp32-devkit-c-v4

Firmware:
MicroPython for ESP32

Red LED:
GPIO2

Green LED:
GPIO4

Push-button:
GPIO17, active HIGH, internal pull-down enabled

OLED SDA:
GPIO16

OLED SCL:
GPIO25

OLED address:
0x3C

OLED size:
128 × 64 pixels
```

Any deviation must be explicitly documented and validated.

## 19. Required Technical Documentation

The project repository must include or reference the following technical
materials:

1. ESP32-DevKitC V4 official user guide;
2. ESP32-DevKitC V4 schematic;
3. ESP32-DevKitC V4 PCB layout;
4. ESP32-DevKitC V4 dimensional drawing;
5. ESP32 datasheet;
6. ESP32-WROOM-32E datasheet;
7. Wokwi ESP32-DevKitC V4 component documentation;
8. Wokwi diagram-format documentation;
9. MicroPython ESP32 quick reference;
10. MicroPython `machine.Pin` documentation;
11. MicroPython `machine.I2C` documentation;
12. MicroPython `asyncio` documentation.

## 20. Official References

### 20.1 Espressif ESP32-DevKitC V4 user guide

```text
https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html
```

### 20.2 ESP32 datasheet

```text
https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf
```

### 20.3 ESP32-WROOM-32E and ESP32-WROOM-32UE datasheet

```text
https://www.espressif.com/sites/default/files/documentation/esp32-wroom-32e_esp32-wroom-32ue_datasheet_en.pdf
```

### 20.4 Wokwi ESP32-DevKitC V4 component

```text
https://docs.wokwi.com/parts/board-esp32-devkit-c-v4
```

### 20.5 Wokwi diagram format

```text
https://docs.wokwi.com/diagram-format
```

### 20.6 MicroPython ESP32 quick reference

```text
https://docs.micropython.org/en/latest/esp32/quickref.html
```

### 20.7 MicroPython `machine.Pin`

```text
https://docs.micropython.org/en/latest/library/machine.Pin.html
```

### 20.8 MicroPython `machine.I2C`

```text
https://docs.micropython.org/en/latest/library/machine.I2C.html
```

### 20.9 MicroPython `asyncio`

```text
https://docs.micropython.org/en/latest/library/asyncio.html
```

## 21. Board Identification Statement

The following statement should be used in reports and submission
documentation:

> The project targets the official Espressif ESP32-DevKitC V4 development
> board, represented in Wokwi by `board-esp32-devkit-c-v4`. A physical
> implementation should preferably use an ESP32-DevKitC V4 fitted with an
> ESP32-WROOM-32E module so that GPIO16 and GPIO17 remain available for the
> predefined OLED and push-button connections. All pin references use ESP32
> GPIO numbers rather than sequential physical header positions.
