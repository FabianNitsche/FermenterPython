from photographer import Photographer
from gpio import Gpio
import logging

logging.basicConfig(filename="/home/pi/FermenterPython/Pictures/log.txt", 
                    filemode='a', 
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
        
gpio = Gpio()
with gpio:
    light = gpio.add_output(25, True)

    photographer = Photographer()

    logging.info("Calling photographer.")
    light.set(True)
    photographer.save_photo()
    light.set(False)