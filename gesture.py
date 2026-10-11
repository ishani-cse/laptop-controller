"""Hand landmarks se gesture pehchanne ka logic."""

import math
from enum import Enum

import config


class Gesture(str, Enum):
    MOVE = "MOVE"
    CLICK = "CLICK"
    SCROLL = "SCROLL"
    DOUBLE_CLICK = "DOUBLE CLICK"
    EXPLORER = "OPEN FOLDER"
    FOLDER_2 = "OPEN FOLDER 2"
    VOLUME = "VOLUME"
    FIST = "FIST"
    IDLE = "IDLE"


def _dist(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)


def fingers_up(lm):
    """[index, middle, ring, pinky] -> True agar finger upar hai."""
    return [
        lm[8].y < lm[6].y,
        lm[12].y < lm[10].y,
        lm[16].y < lm[14].y,
        lm[20].y < lm[18].y,
    ]


def is_pinch(lm):
    # Hand size se normalize, taaki camera se doori ka farak na pade
    hand_size = _dist(lm[0], lm[9])
    if hand_size == 0:
        return False
    return _dist(lm[4], lm[8]) / hand_size < config.PINCH_THRESHOLD


def is_thumb_middle_pinch(lm):
    hand_size = _dist(lm[0], lm[9])
    if hand_size == 0:
        return False
    return _dist(lm[4], lm[12]) / hand_size < config.PINCH_THRESHOLD


def get_gesture(hand_landmarks):
    lm = hand_landmarks.landmark
    up = fingers_up(lm)

    if is_pinch(lm) and not any(up[1:]) and lm[8].y < lm[5].y:
        return Gesture.CLICK
    # Thumb + middle finger pinch (index upar, ring/pinky neeche) = double click
    if up[0] and not up[2] and not up[3] and is_thumb_middle_pinch(lm):
        return Gesture.DOUBLE_CLICK
    if up == [True, True, True, True]:
        return Gesture.FOLDER_2
    if up == [True, False, False, False]:
        return Gesture.MOVE
    if up == [True, True, False, False]:
        return Gesture.SCROLL
    if up == [True, True, True, False]:
        return Gesture.EXPLORER
    if up == [False, False, False, True]:
        return Gesture.VOLUME
    if up == [False, False, False, False]:
        return Gesture.FIST
    return Gesture.IDLE