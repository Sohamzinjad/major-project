# iDrone Gesture Drone

Initial scaffold for a gesture-controlled drone interface:

- `laptop/` contains webcam capture, hand landmark extraction, gesture mapping, and serial output.
- `firmware/` contains Raspberry Pi Pico MicroPython firmware that receives laptop commands and drives an MCP4728 DAC.

## Setup

1. Create and activate a Python 3.10+ virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Verify the webcam:

```bash
python laptop/test_webcam.py
```

4. Run hand tracking:

```bash
python laptop/capture.py
```

5. Run the full laptop pipeline once the Pico is connected:

```bash
python laptop/main.py
```

## Firmware

Flash MicroPython to the Pico, then copy `firmware/main.py` onto the board with Thonny or `mpremote`.

## Safety

- Keep propellers off during bench testing.
- Confirm idle state produces safe low throttle before connecting to the remote or drone.
- Test both laptop-side and firmware-side failsafes before any flight attempt.
