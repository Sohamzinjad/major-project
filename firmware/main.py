from machine import I2C, Pin
import select
import sys
import time


MCP4728_ADDR = 0x60


class MCP4728:
    def __init__(self, i2c, addr=MCP4728_ADDR):
        self.i2c = i2c
        self.addr = addr

    def write_channel(self, channel, value):
        """Write a 12-bit value to MCP4728 channel 0-3 without EEPROM."""
        value = max(0, min(4095, value))
        cmd = 0x40 | (channel << 1)
        hi = (value >> 8) & 0x0F
        lo = value & 0xFF
        self.i2c.writeto(self.addr, bytes([cmd, hi, lo]))


i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
dac = MCP4728(i2c)

IDLE_THROTTLE = 0
IDLE_YAW = 2048
FAILSAFE_TIMEOUT_MS = 500

last_msg_time = time.ticks_ms()
buf = ""

poll = select.poll()
poll.register(sys.stdin, select.POLLIN)


def apply(throttle, yaw):
    dac.write_channel(0, throttle)
    dac.write_channel(1, yaw)


def parse_line(line):
    try:
        parts = dict(part.split(":") for part in line.strip().split(","))
        throttle = int(parts["T"])
        yaw = int(parts["Y"])
        if not (0 <= throttle <= 4095 and 0 <= yaw <= 4095):
            return None
        return throttle, yaw
    except Exception:
        return None


apply(IDLE_THROTTLE, IDLE_YAW)

while True:
    if poll.poll(0):
        char = sys.stdin.read(1)
        if char == "\n":
            parsed = parse_line(buf)
            buf = ""
            if parsed:
                apply(*parsed)
                last_msg_time = time.ticks_ms()
        else:
            buf += char

    if time.ticks_diff(time.ticks_ms(), last_msg_time) > FAILSAFE_TIMEOUT_MS:
        apply(IDLE_THROTTLE, IDLE_YAW)

    time.sleep_ms(5)
