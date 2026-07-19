import os
import sys
from pathlib import Path

import cv2
import numpy as np


def _configure_runtime():
    major, minor = sys.version_info[:2]
    if (major, minor) >= (3, 13):
        raise RuntimeError(
            "This project's MediaPipe hand-tracking path requires Python 3.9-3.12. "
            f"You are using Python {major}.{minor}. Recreate the virtualenv with "
            "`/usr/bin/python3 -m venv venv`, then reinstall requirements."
        )

    os.environ.setdefault(
        "MPLCONFIGDIR",
        str(Path(__file__).resolve().parent.parent / ".mplconfig"),
    )


HAND_CONNECTIONS = (
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 4),
    (0, 5),
    (5, 6),
    (6, 7),
    (7, 8),
    (5, 9),
    (9, 10),
    (10, 11),
    (11, 12),
    (9, 13),
    (13, 14),
    (14, 15),
    (15, 16),
    (13, 17),
    (17, 18),
    (18, 19),
    (19, 20),
    (0, 17),
)


def _resolve_model_path():
    root = Path(__file__).resolve().parent.parent
    candidates = (
        root / "models" / "hand_landmarker.task",
        root / "hand_landmarker.task",
    )
    for candidate in candidates:
        if candidate.exists():
            return candidate

    raise FileNotFoundError(
        "Missing hand landmarker model. Download `hand_landmarker.task` and place "
        "it in `/Users/sohamzinjad/major project/models/hand_landmarker.task`."
    )


def _draw_landmarks(frame, landmarks):
    height, width, _ = frame.shape

    for start, end in HAND_CONNECTIONS:
        p1 = landmarks[start]
        p2 = landmarks[end]
        x1, y1 = int(p1.x * width), int(p1.y * height)
        x2, y2 = int(p2.x * width), int(p2.y * height)
        cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)

    for point in landmarks:
        x = int(point.x * width)
        y = int(point.y * height)
        cv2.circle(frame, (x, y), 4, (0, 255, 0), -1)


class HandCapture:
    def __init__(self, camera_index=0, max_hands=1):
        _configure_runtime()
        import mediapipe as mp
        from mediapipe.tasks import python
        from mediapipe.tasks.python import vision

        self.cap = cv2.VideoCapture(camera_index)
        self.mp = mp
        self.model_path = _resolve_model_path()
        base_options = python.BaseOptions(model_asset_path=str(self.model_path))
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=max_hands,
            min_hand_detection_confidence=0.7,
            min_tracking_confidence=0.6,
        )
        self.hands = vision.HandLandmarker.create_from_options(options)

    def read_frame(self):
        """Return `(frame, landmarks_or_none)` for the latest webcam frame."""
        ok, frame = self.cap.read()
        if not ok:
            return None, None

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = self.mp.Image(image_format=self.mp.ImageFormat.SRGB, data=rgb)
        result = self.hands.detect(image)

        landmarks = None
        if result.hand_landmarks:
            landmarks = result.hand_landmarks[0]
            _draw_landmarks(frame, landmarks)

        return frame, landmarks

    def release(self):
        self.cap.release()
        self.hands.close()


def main():
    capture = HandCapture()

    while True:
        frame, landmarks = capture.read_frame()
        if frame is None:
            break

        if landmarks:
            tip = landmarks.landmark[8]
            height, width, _ = frame.shape
            text = f"Index tip: ({int(tip.x * width)}, {int(tip.y * height)})"
            cv2.putText(
                frame,
                text,
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
            )

        cv2.imshow("Hand Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
