from photographer import Photographer
from gpio import Gpio
from userInput import UserInput
from storage import Storage

from luma.core.interface.serial import i2c
import luma.core.render
from luma.core.sprite_system import framerate_regulator
from luma.oled.device import ssd1306

import smbus2
import bme280
import bme280.const as oversampling

import datetime, threading, time, os

class Main(object):
        
    def start(self):
        regulator = framerate_regulator(fps=10)  # Unlimited = 0
        device = self.get_device()
        port = 3
        address = 0x76
        bus = smbus2.SMBus(port)
        calibration_params = bme280.load_calibration_params(bus, address)

        padding = 2
        canvas = luma.core.render.canvas(device)

        gpio = Gpio()

        storage = Storage()

        # taking photos

        with gpio:
            userInput = UserInput(gpio)
            heater = gpio.add_output(4, False)
            light = gpio.add_output(25, True)
            light.set(True)

            photographer = Photographer()
            photo_interval_seconds = 5 * 60

            def take_photo():
                next_call = time.time()
                while True:
                    photographer.save_photo()
                    next_call += photo_interval_seconds
                    time.sleep(next_call - time.time())
            
            photoThread = threading.Thread(target=take_photo)
            photoThread.daemon = True
            photoThread.start()

            storage_interval_seconds = 10
            next_store = time.time()

            try:
                while True:
                    if userInput.exit:
                        light.set(False)
                        heater.set(False)
                        os.system("sudo shutdown -h")
                        break

                    with regulator, canvas as c:
                        light.set(not photographer.light)
                        data = bme280.sample(bus, address, calibration_params, oversampling.x4)
                        currentTemp = data.temperature
                        setTemp = userInput.temperatureGoal

                        heaterOn = currentTemp < setTemp

                        if next_store < time.time():
                            try:
                                storage.write_data(data, setTemp, heaterOn)
                            except:
                                pass
                            next_store += storage_interval_seconds

                        heater.set(heaterOn)

                        c.rectangle(device.bounding_box, fill="black")

                        title_size = c.textsize(userInput.title)
                        c.text((device.width - padding - title_size[0], padding + 4), userInput.title, fill="white")

                        c.text((padding, padding + 12), "Soll: {:.1f} °C".format(setTemp), fill="white")
                        c.text((padding, padding + 20), "Ist:  {:.1f} °C".format(currentTemp), fill="white")
                        c.text((padding, padding + 28), "Heater:  {}".format("On" if heaterOn else "Off"), fill="white")

                        current_item = userInput.get_current_item()
                        current_item_size = c.textsize(current_item)
                        c.text((device.width - padding - current_item_size[0], padding + 36), current_item, fill="white")
            except KeyboardInterrupt:
                pass

    def get_device(self):
        serial = i2c(port=1, address=0x3C)
        device = ssd1306(serial)
        return device


if __name__ == "__main__":
    Main().start()

