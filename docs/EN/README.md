# CESS-UFF — ESP32 & MicroPython Practical Assessment

**Language / Idioma:** [English](README.md) | [Português](../PT/README.md)

ESP32 (MicroPython) practical assessment — Instrumentation, Electronics and
Programming Logic. Two LEDs and an SSD1306 OLED display react to a push
button, simulated in [Wokwi](https://wokwi.com).

> **Status:** this is the unified, consolidated version of the project. It
> replaces three independent drafts previously kept in `g/`, `p/` and `c/`
> (all removed after their reusable content was folded in here), merging
> the best documentation, code and design decisions from each. It also
> fixes one confirmed circuit bug (an invalid push-button pin reference,
> see design summary) and, as of the first live wokwi.com runs, one
> confirmed **boot-loop bug**: a pinned MicroPython firmware `env` in
> `diagram.json` (inherited from one of the drafts) made the board reset
> forever before any code — not just this project's code — ever ran. It
> has been removed; see `technical-specification.md` §16. The
> [`tests/`](../../tests/README.md) scripts have since confirmed every GPIO,
> `asyncio`, and hardware I2C all work on wokwi.com — `main.py` was
> reverted from the earlier defensive `SoftI2C` workaround back to
> hardware `I2C` accordingly.

**Wokwi project link (circuit + simulation):** `<add the wokwi.com/projects/... link here after publishing>`
**GitHub repository link:** `<GITHUB_REPOSITORY_URL>`

## What it does

| Input or task | Expected output |
|---|---|
| Independent red LED task | GPIO 2 toggles every 500 ms, never blocked by the other tasks |
| Push-button released | Green LED (GPIO 4) OFF, OLED shows `Boa sorte!!` |
| Push-button pressed | Green LED (GPIO 4) ON, OLED shows `Consegui!` |

The push-button (GPIO 17) is active HIGH and uses the ESP32's internal
pull-down resistor, so no external resistor is required. The OLED is
refreshed only at startup and after a state transition, which avoids
unnecessary I2C traffic and visible flicker.

## Required pin mapping

| Component | Wokwi ID | ESP32 pin | Notes |
|---|---|---:|---|
| Red LED | `red-led` | GPIO 2 | Continuous 500 ms blink, independent of everything else |
| Green LED | `green-led` | GPIO 4 | Mirrors the debounced button state |
| Push-button | `push-button` | GPIO 17 | Normally-open, active HIGH, internal `Pin.PULL_DOWN` |
| OLED clock | `oled-display` / SCL | GPIO 25 | I2C clock |
| OLED data | `oled-display` / SDA | GPIO 16 | I2C data |

GPIO 25 as SCL and GPIO 16 as SDA, and the LED/button GPIOs above, are
predefined project requirements, not the result of an interface
optimization — see [`technical-specification.md`](technical-specification.md).
Full per-component spec sheets (board, display, LEDs, resistors,
push-button — exact Wokwi identifiers and pin names) are in
[`component-specifications.md`](component-specifications.md), and
the board/module identification, GPIO-to-physical-header map, reserved
pins, and a physical wiring checklist are in
[`hardware-reference.md`](hardware-reference.md).

## Repository structure

```text
cess-uff/
├── main.py                          # application entry point (MicroPython)
├── ssd1306.py                       # SSD1306 OLED driver
├── diagram.json                     # Wokwi circuit (components + wiring)
├── wokwi.toml                       # Wokwi simulator config (local VS Code only)
├── README.md                        # main repository README (English)
├── LICENSE                          # CC0 1.0 Universal
├── .gitignore
├── docs/
│   ├── EN/                          # English documentation
│   │   ├── README.md
│   │   ├── technical-specification.md   # requirements + design decision log
│   │   ├── component-specifications.md  # per-component spec sheets
│   │   └── hardware-reference.md        # board ID, pin map, wiring checklist
│   └── PT/                          # Portuguese documentation
│       ├── README.md
│       ├── technical-specification.md
│       ├── component-specifications.md
│       └── hardware-reference.md
└── tests/                           # standalone diagnostic scripts
    ├── README.md
    ├── 01_red_led_basic.py
    ├── 02_red_led_blink.py
    ├── 03_red_led_asyncio.py
    ├── 04_push_button_green_led.py
    ├── 05_oled_basic.py
    └── 06_oled_full_diagnostic.py
```

## Documentation links

- [Technical Specification](technical-specification.md)
- [Component Specifications](component-specifications.md)
- [Hardware Reference](hardware-reference.md)

## License

This project is dedicated to the public domain under **CC0 1.0 Universal**.
See [`LICENSE`](../../LICENSE).
