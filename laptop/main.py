import cv2

from capture import HandCapture
from gesture_mapper import GestureMapper
from serial_link import SerialLink


def main():
    capture = HandCapture()
    mapper = GestureMapper()
    link = SerialLink()

    while True:
        frame, landmarks = capture.read_frame()
        if frame is None:
            break

        throttle, yaw = mapper.compute(landmarks)
        link.send(throttle, yaw)

        cv2.putText(
            frame,
            f"T:{throttle}  Y:{yaw}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
        )
        cv2.imshow("iDrone Control", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
