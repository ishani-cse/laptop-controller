import cv2


def get_camera():
    cap = cv2.VideoCapture(0)

    # Chhota resolution = kam pixels = MediaPipe ko fast process karne mein help
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Buffer size kam karo taaki purane frames queue mein na ruke (latency kam)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    return cap


def get_frame(cap):

    ret, frame = cap.read()

    if not ret:
        return None

    frame = cv2.flip(frame, 1)

    return frame