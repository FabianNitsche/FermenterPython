from picamera import PiCamera
import time
from datetime import datetime

class Photographer(object):
    def __init__(self):
        self._camera = PiCamera()
        time.sleep(2)
        self._camera.brightness = 60
        self._camera.contrast = 20
        self.light = False

    def save_photo(self):
        self.light = True
        time.sleep(2)

        filepath = "/home/pi/FermenterPython/Pictures/" + datetime.now().strftime("%Y_%m_%d__%H_%M_%S") + ".jpg"
        self._camera.capture(filepath)

        self.light = False


