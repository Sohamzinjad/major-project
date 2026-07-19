import cv2
import mediapipe as mp


class HandCapture:
    def __init__(self, camera_index=0, max_hands=1):
        self.cap = cv2.VideoCapture(camera_index)
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.6,
        )
        self.mp_draw = mp.solutions.drawing_utils

    def read_frame(self):
        """Return `(frame, landmarks_or_none)` for the latest webcam frame."""
        ok, frame = self.cap.read()
        if not ok:
            return None, None

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)

        landmarks = None
        if result.multi_hand_landmarks:
            landmarks = result.multi_hand_landmarks[0]
            self.mp_draw.draw_landmarks(
                frame,
                landmarks,
                self.mp_hands.HAND_CONNECTIONS,
            )

        return frame, landmarks

    def release(self):
        self.cap.release()


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
