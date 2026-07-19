# iDrone Gesture Drone

Initial scaffold for a gesture-controlled drone interface:

- `laptop/` contains webcam capture, hand landmark extraction, gesture mapping, and serial output.
- `firmware/` contains Raspberry Pi Pico MicroPython firmware that receives laptop commands and drives an MCP4728 DAC.

## Setup

1. Create and activate a Python 3.9-3.12 virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

If you create the environment with Python `3.13+`, MediaPipe's legacy hand-tracking API used by this project may be missing. On your machine, `/usr/bin/python3` is `Python 3.9.6`, which is suitable.

Recreate the virtualenv like this if you accidentally used Python `3.14`:

```bash
cd /Users/sohamzinjad/major\ project
deactivate 2>/dev/null || true
rm -rf venv
/usr/bin/python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install --no-compile -r requirements.txt
```

`--no-compile` avoids an install-time bytecode compilation failure triggered by a bad test file shipped inside the current `mediapipe` wheel on this environment. It does not affect normal use of the package.

3. Verify the webcam:

```bash
python laptop/test_webcam.py
```

4. Run hand tracking:

```bash
mkdir -p models
curl -L -o models/hand_landmarker.task \
  https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task
python laptop/capture.py
```

The installed `mediapipe` wheel on this machine exposes the newer Tasks API, not the old `mp.solutions.hands` API. This project now uses `HandLandmarker`, which requires the local model file above.

5. Run the full laptop pipeline once the Pico is connected:

```bash
python laptop/main.py
```

## macOS camera permission

If `python laptop/test_webcam.py` prints errors like `not authorized to capture video` or `camera failed to properly initialize`, macOS has blocked Terminal or your IDE from using the camera.

Fix it in:

- `System Settings -> Privacy & Security -> Camera`
- Enable camera access for the app that launched Python, usually `Terminal`, `iTerm`, `Warp`, `VS Code`, or `Thonny`

Then fully quit and reopen that app before running the script again.

If the prompt never appeared, reset the permission once and retry:

```bash
tccutil reset Camera com.apple.Terminal
```

If you are using a different app, replace `com.apple.Terminal` with that app's bundle ID.

## Firmware

Flash MicroPython to the Pico, then copy `firmware/main.py` onto the board with Thonny or `mpremote`.

## Safety

- Keep propellers off during bench testing.
- Confirm idle state produces safe low throttle before connecting to the remote or drone.
- Test both laptop-side and firmware-side failsafes before any flight attempt.
# major-project
