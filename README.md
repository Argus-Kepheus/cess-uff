# cess-uff

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
> has been removed; see `docs/technical-specification.md` §16. The
> [`tests/`](tests/README.md) scripts have since confirmed every GPIO,
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
optimization — see [`docs/technical-specification.md`](docs/technical-specification.md).
Full per-component spec sheets (board, display, LEDs, resistors,
push-button — exact Wokwi identifiers and pin names) are in
[`docs/component-specifications.md`](docs/component-specifications.md), and
the board/module identification, GPIO-to-physical-header map, reserved
pins, and a physical wiring checklist are in
[`docs/hardware-reference.md`](docs/hardware-reference.md).

## Repository structure

```text
cess-uff/
├── main.py                          # application entry point (MicroPython)
├── ssd1306.py                       # SSD1306 OLED driver
├── diagram.json                     # Wokwi circuit (components + wiring)
├── wokwi.toml                       # Wokwi simulator config (local VS Code only)
├── README.md
├── LICENSE                          # CC0 1.0 Universal
├── .gitignore
├── docs/
│   ├── technical-specification.md   # requirements + design decision log
│   ├── component-specifications.md  # per-component spec sheets (board, display, LEDs, ...)
│   └── hardware-reference.md        # board/module ID, GPIO-to-header map, wiring checklist
└── tests/                           # standalone diagnostic scripts, not part of the deliverable
    ├── README.md                    # what each test validates, and how to run it
    ├── 01_red_led_basic.py
    ├── 02_red_led_blink.py
    ├── 03_red_led_asyncio.py
    ├── 04_push_button_green_led.py
    ├── 05_oled_basic.py
    └── 06_oled_full_diagnostic.py
```

Before trying the full `main.py`, consider running the scripts in
[`tests/`](tests/README.md) — they validate each GPIO/component in
isolation, in increasing order of complexity, which makes it much faster
to localize a wiring or firmware problem than debugging the whole
application at once.

## Option A — Run it in the browser (fastest, no install)

1. Go to [wokwi.com](https://wokwi.com) and create a new **ESP32 /
   MicroPython** project.
2. Replace the generated `main.py` and add `ssd1306.py` with the files from
   this repository.
3. Open the diagram editor and import this repository's `diagram.json`
   (or rebuild the circuit visually using the pin mapping table above).
4. Click **Start Simulation**.
5. Press the on-screen button (or click and hold it) to exercise both
   button states.
6. Click **Share** to get the project link, and paste it at the top of this
   README.

`wokwi.toml` is **not** used by the online simulator — the website
auto-detects `main.py`. It only matters for Option B below.

## Option B — Run it locally with VS Code

Requirements:

- [VS Code](https://code.visualstudio.com/)
- [Wokwi for VS Code](https://marketplace.visualstudio.com/items?itemName=Wokwi.wokwi-vscode)
  extension (free personal license — activate with `F1` → **Wokwi: Request a
  new License**)
- Python 3 with `mpremote` (`pip install mpremote`)
- A MicroPython firmware `.bin` for ESP32, downloaded from
  [micropython.org/download/esp32](https://micropython.org/download/esp32)

Steps:

1. Clone this repository and open it in VS Code.
2. Place the downloaded firmware `.bin` in the project root and update the
   `firmware` path in `wokwi.toml` to match its file name (`firmware.bin` is
   excluded by `.gitignore`). When possible, install an `mpremote` release
   matching the selected MicroPython firmware release, e.g. firmware
   `1.23.0` paired with `mpremote==1.23.0`:
   ```bash
   python -m pip install "mpremote==<FIRMWARE_VERSION>"
   ```
3. Open `diagram.json` in VS Code and click the simulator's play button, or
   run **Wokwi: Start Simulator** from the command palette. This exposes the
   simulated serial port through RFC2217 on TCP port 4000.
4. While the simulator is running, in a separate terminal upload the
   project files (the simulated filesystem is not persistent between
   sessions, so repeat this after every restart):
   ```bash
   mpremote connect port:rfc2217://localhost:4000 fs cp ssd1306.py :ssd1306.py
   mpremote connect port:rfc2217://localhost:4000 fs cp main.py :main.py
   mpremote connect port:rfc2217://localhost:4000 reset
   ```
   If `mpremote` reports that it cannot enter raw REPL mode, focus the Wokwi
   REPL, press `Ctrl+A`, and retry.

> **Note:** visually editing `diagram.json` inside VS Code requires a paid
> Wokwi Hobby+/Pro plan. On the free tier, edit the circuit visually on
> wokwi.com (Option A) and copy the resulting `diagram.json` back into this
> repository, then keep using VS Code for the code itself.

## Design summary

- **Wokwi over Tinkercad:** Tinkercad Circuits only runs Arduino-style C/C++
  or block code on its boards — it cannot execute a MicroPython script, so
  it could not satisfy this assignment's source-code deliverable. Wokwi
  natively supports ESP32 + MicroPython + an SSD1306 component and produces
  a shareable simulation URL.
- **Cooperative `asyncio` tasks instead of a super loop or blocking
  delays:** each behavior (LED blink, button monitoring) is an independent
  coroutine, which keeps the code organized and scalable as more
  sensors/outputs are added, and guarantees the red LED blink is never
  delayed by an OLED I2C transfer. `time.sleep()` is never used.
  **This choice is about code organization, not about making I2C
  non-blocking** — the `ssd1306` driver's `show()` call is still a
  synchronous I2C write with no internal `await` point, so it blocks the
  CPU for its duration regardless of the concurrency model chosen.
- **Internal pull-down on the button (`Pin.PULL_DOWN`):** satisfies
  "HIGH when pressed" without an external resistor.
- **I2C, not SPI, for the OLED:** imposed by the project's own 2-pin
  specification (SCL = GPIO 25, SDA = GPIO 16), not chosen for technical
  superiority — SPI would need 4–5 lines but was never an option here.
- **Hardware `machine.I2C`, not `SoftI2C`:** an earlier revision adopted
  bit-banged `SoftI2C` as an unconfirmed, purely defensive compatibility
  choice while tracking down the wokwi.com issues reported against the
  original drafts. `tests/05_oled_basic.py` and
  `tests/06_oled_full_diagnostic.py` have since confirmed hardware `I2C`
  works fine on wokwi.com, so `main.py` reverted to it (see
  `docs/technical-specification.md`, decision log).
- **`push-button` wiring uses the documented `1.l`/`2.l` pin names:** one of
  the original drafts referenced the pushbutton's pins as `1.R`/`2.R`
  (wrong case, wrong side), which Wokwi silently fails to resolve — the
  button never registered a press. The fix is to use the pin names the
  `wokwi-pushbutton` part actually exposes.
- **OLED updates are event-driven:** the display is redrawn only once at
  startup and again on each debounced button-state change, not on every
  poll cycle, to avoid flicker and redundant I2C writes.
- **Debounce is a defensive design choice, not a simulator requirement:**
  Wokwi's `wokwi-pushbutton` behaves as an ideal, bounce-free switch in
  simulation, so it is not strictly required there. The lightweight
  software debounce is kept anyway because it is the correct behavior for
  a real, physical button in a future hardware phase.

See [`docs/technical-specification.md`](docs/technical-specification.md) for
the complete requirements, decisions, electrical design, and verification
plan.

## License

This project is dedicated to the public domain under **CC0 1.0 Universal**.
See [`LICENSE`](LICENSE).

## Official references

- Wokwi documentation: <https://docs.wokwi.com/>
- Wokwi `diagram.json` format: <https://docs.wokwi.com/diagram-format>
- Wokwi VS Code MicroPython guide: <https://docs.wokwi.com/vscode/vscode-micropython>
- Wokwi project configuration: <https://docs.wokwi.com/vscode/project-config>
- MicroPython ESP32 downloads: <https://micropython.org/download/ESP32_GENERIC/>
