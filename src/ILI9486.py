import time
import itertools
import RPi.GPIO as GPIO

class ILI9486:
    def __init__(self, spi, dc, rst, flip=True):
        self.spi = spi
        self.dc = dc
        self.rst = rst
        self.size = (480, 320)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.dc, GPIO.OUT)
        GPIO.output(self.dc, GPIO.HIGH)
        GPIO.setup(self.rst, GPIO.OUT)
        GPIO.output(self.rst, GPIO.HIGH)

        self.reset()

        self.command(0xF1); self.data([0x36, 0x04, 0x00, 0x3c, 0x0f, 0x8f], size=1)
        self.command(0xF2); self.data([0x18, 0xa3, 0x12, 0x02, 0xb2, 0x12, 0xff, 0x10, 0x00], size=1)
        self.command(0xF8); self.data([0x21, 0x04], size=1)
        self.command(0xF9); self.data([0x00, 0x08], size=1)
        self.command(0x36); self.data([0x08], size=1)
        self.command(0xB4); self.data([0x00], size=1)
        self.command(0xC1); self.data([0x41], size=1)
        self.command(0xC5); self.data([0x00, 0x91, 0x80, 0x00], size=1)
        self.command(0xE0); self.data([0x0f, 0x1f, 0x1c, 0x0c, 0x0f, 0x08, 0x48, 0x98, 0x37, 0x0a, 0x13, 0x04, 0x11, 0x0d, 0x00], size=1)
        self.command(0xE1); self.data([0x0f, 0x32, 0x2e, 0x0b, 0x0d, 0x05, 0x47, 0x75, 0x37, 0x06, 0x10, 0x03, 0x24, 0x20, 0x00], size=1)
        self.command(0x3a); self.data([0x66], size=1)
        self.command(0x11)
        self.command(0x36); self.data([0x28], size=1)
        self.command(0xFf)
        self.command(0x29)
        self.command(0x2A); self.data([0, 0, self.size[0] >> 8, self.size[0] & 0xFF], size=1)
        self.command(0x2B); self.data([0, 0, self.size[1] >> 8, self.size[1] & 0xFF], size=1)

    def data(self, data, size=4096):
        GPIO.output(self.dc, GPIO.HIGH)
        for start in range(0, len(data), size):
            end = min(start + size, len(data))
            self.spi.writebytes(data[start:end])

    def command(self, data):
        GPIO.output(self.dc, GPIO.LOW)
        self.spi.writebytes([data])

    def reset(self):
        GPIO.output(self.rst, GPIO.HIGH)
        time.sleep(.02)
        GPIO.output(self.rst, GPIO.LOW)
        time.sleep(.02)
        GPIO.output(self.rst, GPIO.HIGH)
        time.sleep(.120)

    def display(self, image):
        if image.size != self.size:
            raise Exception("Image size doesn't match screen size")
        self.command(0x2C)
        self.data(list(itertools.chain.from_iterable(image.getdata())))