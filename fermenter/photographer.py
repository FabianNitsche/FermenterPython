from picamera import PiCamera
import time
from datetime import datetime

light_pin = 25

class Photographer(object):
    def __init__(self, gpio):
        self._light = gpio.add_output(light_pin, True)
        self._camera = PiCamera()
        time.sleep(2)
        self._camera.brightness = 60
        self._camera.contrast = 20

    def save_photo(self):
        self._light.set(True)
        time.sleep(2)

        filepath = "/home/pi/FermenterPython/Pictures/" + datetime.now().strftime("%Y_%m_%d__%H_%M_%S") + ".jpg"
        self._camera.capture(filepath)

        self._light.set(False)


