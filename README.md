# Hand Gesture Laptop Controller

Control your laptop with hand gestures in real time: move the cursor, click, scroll and change the volume without touching the mouse or keyboard.

Built with **Python, OpenCV and MediaPipe**.

<!-- Add a screenshot or demo GIF here, e.g. ![Demo](demo.gif) -->

## Features

- Cursor movement with the index finger
- Click and double click using pinch gestures
- Scrolling with two fingers
- Volume control with the pinky finger
- Folder shortcuts (hold 3 or 4 fingers)
- Pause / resume with a fist
- Live on-screen display of status, current gesture and FPS

## Gestures

| Gesture | Action |
|---|---|
| Index finger up | Move cursor |
| Thumb + index pinch | Click |
| Thumb + middle pinch (index up) | Double click |
| Index + middle fingers up | Scroll (hand up = scroll up, hand down = scroll down) |
| Index + middle + ring fingers up (hold 1 s) | Open Home folder |
| All four fingers up (hold 1 s) | Open Downloads folder |
| Only pinky up | Volume (pinky higher = louder, lower = quieter) |
| Fist (hold 2 s) | Pause / resume control |

Keyboard: `P` pause/resume, `Q` quit.

## How it works

1. **OpenCV** reads frames from the webcam (640x480) and mirrors them.
2. **MediaPipe Hands** detects one hand and returns 21 hand landmarks per frame.
3. The gesture logic checks which fingers are up (fingertip above its joint) and measures distances between landmarks. The pinch distance is divided by hand size, so it works at different distances from the camera.
4. The detected gesture is converted to a system action: **PyAutoGUI** for mouse and scroll, **pycaw** for volume on Windows (AppleScript on macOS).
5. Cursor movement uses the middle part of the camera frame mapped to the full screen, and exponential smoothing to reduce jitter.

## Project structure

```
.
├── main.py          # main loop, HUD, keyboard controls
├── camera.py        # webcam setup and frame capture
├── hand_tracker.py  # MediaPipe hand detection and drawing
├── gesture.py       # landmarks -> gesture recognition
├── controller.py    # gesture -> mouse / scroll / volume / folder actions
└── config.py        # all tunable settings
```

## Installation

Developed with Python 3.11 and a normal laptop webcam.

```bash
git clone https://github.com/ishani-cse/laptop-controller.git
cd laptop-controller
pip install opencv-python mediapipe pyautogui pycaw comtypes
python main.py
```

`pycaw` and `comtypes` are only needed for volume control on Windows.

## Configuration

Edit `config.py` to tune the behaviour:

| Setting | What it does |
|---|---|
| `SMOOTHING` | Higher = smoother but slower cursor, lower = faster but shakier |
| `ACTIVE_MARGIN` | Size of the camera area that maps to the full screen |
| `PINCH_THRESHOLD` | How close thumb and finger must be to count as a pinch |
| `SCROLL_SPEED`, `SCROLL_DEADZONE` | Scroll sensitivity and the ignored small movement |
| `VOLUME_TOP`, `VOLUME_BOTTOM` | Pinky height range mapped to 100% and 0% volume |
| `FOLDER_3_FINGERS`, `FOLDER_4_FINGERS` | Folders opened by the 3-finger and 4-finger gestures |

## Tips for best results

- Use good lighting and a plain background.
- Keep your palm facing the camera with the hand upright.
- Use one hand only (the program tracks a single hand).

## Limitations

- Finger detection depends on the hand being upright; a tilted hand can be misread.
- The cursor does not move while pinching, so drag and drop is not supported.
- Volume control works on Windows and macOS only.
- Accuracy drops in poor lighting.

## Future improvements

- Drag and drop
- Gesture stability check across a few frames
- Per-user calibration
- Linux volume support

## Tech stack

Python, OpenCV, MediaPipe, PyAutoGUI, pycaw
