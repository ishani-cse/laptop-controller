import time

import cv2

from camera import get_camera, get_frame
from hand_tracker import detect_hand, draw_hand
from gesture import get_gesture, Gesture
from controller import SystemController

WINDOW = "Gesture-Based Laptop Controller"

HELP = [
    "Index: Move | Pinch: Click | Thumb+Middle: Dbl Click",
    "2 Fingers: Scroll | 3/4 Fingers (hold): Folders",
    "Pinky: Volume | Fist 2s: Pause | Q: Quit",
]


def draw_hud(frame, active, gesture_label, fps):
    status = "ACTIVE" if active else "PAUSED"
    color = (0, 170, 0) if active else (0, 0, 220)

    cv2.putText(frame, f"Status: {status}", (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
    cv2.putText(frame, f"Gesture: {gesture_label}", (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(frame, f"FPS: {int(fps)}", (20, 105),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 120, 0), 2)

    h = frame.shape[0]
    for i, line in enumerate(HELP):
        cv2.putText(frame, line, (20, h - 60 + i * 22),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)


def main():
    cap = get_camera()
    controller = SystemController()
    active = True
    prev_time = 0

    while True:
        frame = get_frame(cap)
        if frame is None:
            print("Camera nahi mil raha")
            break

        results = detect_hand(frame)
        label = "NO HAND"

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            draw_hand(frame, hand)

            gesture = get_gesture(hand)
            label = gesture.value

            if controller.handle(gesture, hand.landmark, active) == "TOGGLE":
                active = not active
                print("ACTIVE" if active else "PAUSED")
        else:
            controller.reset()

        now = time.time()
        fps = 1 / (now - prev_time) if prev_time else 0
        prev_time = now

        draw_hud(frame, active, label, fps)
        cv2.imshow(WINDOW, frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("p"):
            active = not active

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()