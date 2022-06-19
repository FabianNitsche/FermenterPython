from picamera import PiCamera
import time, logging, shutil
from datetime import datetime

class Photographer(object):
    def __init__(self):
        self._camera = PiCamera()
        time.sleep(2)
        self._camera.rotation = 180
        self._camera.brightness = 60
        self._camera.contrast = 20
        self.light = False

    def save_photo(self):
        self.light = True
        time.sleep(2)

        try:
            filepath = "/home/pi/FermenterPython/Pictures/" + datetime.now().strftime("%Y_%m_%d__%H_%M_%S") + ".jpg"
            logging.info("Taking image " + filepath)
            self._camera.capture(filepath)
            logging.info("Finished taking image.")
            shutil.copyfile(filepath, "/usr/share/apache2/icons/fermenter/fermenter.jpg")
        except Exception as e:
            logging.info(e)
            logging.warning(e)
            pass

        self.light = False


