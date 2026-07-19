import time

import serial
import serial.tools.list_ports


class SerialLink:
    def __init__(self, port=None, baud=115200):
        self.baud = baud
        self.port = port or self._autodetect()
        self.ser = None
        self._connect()

    def _autodetect(self):
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            if "USB" in port.description or "Pico" in port.description:
                return port.device

        raise RuntimeError(
            "No Pico found. Pass port= explicitly, for example '/dev/ttyACM0'."
        )

    def _connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baud, timeout=0.1)
            time.sleep(2)
        except Exception as exc:
            print(f"[serial_link] connect failed: {exc}")
            self.ser = None

    def send(self, throttle, yaw):
        if self.ser is None or not self.ser.is_open:
            self._connect()
            return False

        try:
            message = f"T:{throttle},Y:{yaw}\n"
            self.ser.write(message.encode())
            return True
        except Exception as exc:
            print(f"[serial_link] send failed: {exc}")
            self.ser = None
            return False
