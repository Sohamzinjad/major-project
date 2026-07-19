import math
from collections import deque


class GestureMapper:
    def __init__(self, smoothing_window=5, deadband=50):
        self.throttle_hist = deque(maxlen=smoothing_window)
        self.yaw_hist = deque(maxlen=smoothing_window)
        self.deadband = deadband
        self.last_throttle = 0
        self.last_yaw = 2048

    @staticmethod
    def _dist(point1, point2):
        return math.hypot(point1.x - point2.x, point1.y - point2.y)

    def compute(self, landmarks):
        """Map hand landmarks to `(throttle, yaw)` in the 0-4095 DAC range."""
        if landmarks is None:
            return 0, 2048

        lm = landmarks.landmark

        raw_dist = self._dist(lm[4], lm[8])
        min_dist = 0.03
        max_dist = 0.25
        norm = (raw_dist - min_dist) / (max_dist - min_dist)
        norm = max(0.0, min(1.0, norm))
        throttle_raw = int(norm * 4095)

        dx = lm[9].x - lm[0].x
        dy = lm[9].y - lm[0].y
        angle = math.degrees(math.atan2(dx, -dy))
        angle = max(-45, min(45, angle))
        yaw_raw = int(((angle + 45) / 90) * 4095)

        self.throttle_hist.append(throttle_raw)
        self.yaw_hist.append(yaw_raw)
        throttle = int(sum(self.throttle_hist) / len(self.throttle_hist))
        yaw = int(sum(self.yaw_hist) / len(self.yaw_hist))

        if abs(throttle - self.last_throttle) < self.deadband:
            throttle = self.last_throttle
        if abs(yaw - self.last_yaw) < self.deadband:
            yaw = self.last_yaw

        self.last_throttle = throttle
        self.last_yaw = yaw
        return throttle, yaw
