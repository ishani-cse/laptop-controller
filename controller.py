"""Gestures ko laptop actions (mouse, scroll, volume, folder) mein badalta hai."""

import os
import platform
import subprocess
import time

import pyautogui

import config
from gesture import Gesture

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

SCREEN_W, SCREEN_H = pyautogui.size()
OS = platform.system()


# ---------------- Volume ----------------
def _init_volume():
    if OS != "Windows":
        return None
    try:
        from ctypes import POINTER, cast
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

        dev = AudioUtilities.GetSpeakers()
        if hasattr(dev, "EndpointVolume"):  # naya pycaw
            return dev.EndpointVolume
        iface = dev.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        return cast(iface, POINTER(IAudioEndpointVolume))
    except Exception as e:
        print("Volume setup fail:", e)
        return None


_volume = _init_volume()


def set_volume(level):
    level = min(max(level, 0.0), 1.0)
    if OS == "Windows" and _volume is not None:
        _volume.SetMasterVolumeLevelScalar(level, None)
    elif OS == "Darwin":
        subprocess.run(["osascript", "-e", f"set volume output volume {int(level * 100)}"])


# ---------------- Folder ----------------
def open_folder(path):
    path = os.path.expanduser(path)
    if not os.path.isdir(path):
        print("Folder nahi mila:", path)
        return
    if OS == "Windows":
        os.startfile(path)
    elif OS == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


# ---------------- Controller ----------------
class SystemController:
    def __init__(self):
        self.prev_x = None
        self.prev_y = None
        self.scroll_prev_y = None
        self.pinching = False
        self.last_gesture = None
        self.since = time.time()
        self.fired = False

    def reset(self):
        """Haath frame se hata to saara state clear."""
        self.last_gesture = None
        self.scroll_prev_y = None
        self.pinching = False

    def handle(self, gesture, lm, active=True):
        """
        active=False (paused) mein sirf FIST-hold se resume hota hai.
        Return "TOGGLE" jab pause/resume karna ho.
        """
        now = time.time()

        if gesture != self.last_gesture:
            self.last_gesture = gesture
            self.since = now
            self.fired = False
            self.scroll_prev_y = None
            if gesture != Gesture.CLICK:
                self.pinching = False

        held = now - self.since

        # Pause / Resume toggle
        if gesture == Gesture.FIST:
            if held > config.PAUSE_TOGGLE_HOLD and not self.fired:
                self.fired = True
                return "TOGGLE"
            return None

        if not active:
            return None

        tip = lm[8]

        if gesture == Gesture.MOVE:
            m = config.ACTIVE_MARGIN
            nx = min(max((tip.x - m) / (1 - 2 * m), 0), 1)
            ny = min(max((tip.y - m) / (1 - 2 * m), 0), 1)
            x, y = nx * SCREEN_W, ny * SCREEN_H
            if self.prev_x is None:
                self.prev_x, self.prev_y = pyautogui.position()
            self.prev_x += (x - self.prev_x) / config.SMOOTHING
            self.prev_y += (y - self.prev_y) / config.SMOOTHING
            pyautogui.moveTo(self.prev_x, self.prev_y)

        elif gesture == Gesture.CLICK:
            if not self.pinching:  # ek pinch = ek click
                pyautogui.click()
                self.pinching = True

        elif gesture == Gesture.SCROLL:
            if self.scroll_prev_y is not None:
                dy = self.scroll_prev_y - tip.y  # haath upar = scroll up
                if abs(dy) > config.SCROLL_DEADZONE:
                    pyautogui.scroll(int(dy * config.SCROLL_SPEED))
            self.scroll_prev_y = tip.y

        elif gesture == Gesture.DOUBLE_CLICK:
            if not self.pinching:  # ek pinch = ek double click
                pyautogui.doubleClick()
                self.pinching = True

        elif gesture == Gesture.EXPLORER:
            if held > config.EXPLORER_HOLD and not self.fired:
                self.fired = True
                open_folder(config.FOLDER_3_FINGERS)

        elif gesture == Gesture.FOLDER_2:
            if held > config.EXPLORER_HOLD and not self.fired:
                self.fired = True
                open_folder(config.FOLDER_4_FINGERS)

        elif gesture == Gesture.VOLUME:
            span = config.VOLUME_BOTTOM - config.VOLUME_TOP
            level = 1 - (lm[20].y - config.VOLUME_TOP) / span
            set_volume(level)

        return None