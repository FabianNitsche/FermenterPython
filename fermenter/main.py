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

import datetime, threading, time, os, logging

class Main(object):
        
    def start(self):
        logging.basicConfig(filename="/home/pi/FermenterPython/Pictures/log.txt", 
                            filemode='a', 
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            level=logging.INFO)
        
        logging.info("Starting Fermenter.")

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

        heating_hysteresis = 1

        # taking photos

        with gpio:
            userInput = UserInput(gpio)
            heater = gpio.add_output(4, False)
            light = gpio.add_output(25, True)

            photographer = Photographer()
            photo_interval_seconds = 5 * 60

            # last_light_setting = photographer.light

            # def take_photo():
            #     logging.info("Starting photographer.")
            #     next_call = time.time()
            #     while True:
            #         logging.info("Calling photographer.")
            #         photographer.save_photo()
            #         next_call += photo_interval_seconds
            #         sleep_time = next_call - time.time()
            #         logging.info("Sleeping " + sleep_time)
            #         time.sleep(sleep_time)
            
            # photoThread = threading.Thread(target=take_photo)
            # photoThread.daemon = True
            # photoThread.start()

            storage_interval_seconds = 10
            next_store = time.monotonic()
            next_photo = time.monotonic()

            heaterOn = False

            try:
                while True:
                    try:
                        if userInput.exit:
                            heater.set(False)
                            light.set(False)
                            os.system("sudo shutdown -h")
                            break

                        with regulator, canvas as c:
                            # light_setting = photographer.light
                            # if light_setting != last_light_setting:
                            #     last_light_setting = light_setting
                            #     light.set(light_setting)

                            data = bme280.sample(bus, address, calibration_params, oversampling.x4)
                            currentTemp = data.temperature
                            setTemp = userInput.temperatureGoal
                            
                            if currentTemp <= 1:
                                heaterOn = False
                            else:
                                if currentTemp < setTemp - 0.5 * heating_hysteresis:
                                    heaterOn = True
                                elif currentTemp > setTemp + 0.5 * heating_hysteresis:
                                    heaterOn = False

                            # if next_store < time.monotonic():
                            #     logging.info("Writing data to db.")
                            #     storage.write_data(data, setTemp, heaterOn)
                            #     logging.info("Done writing data to db.")
                            #     next_store += storage_interval_seconds

                            heater.set(heaterOn)

                            c.rectangle(device.bounding_box, fill="black")

                            title_size = c.textsize(userInput.title)
                            c.text((device.width - padding - title_size[0], padding + 4), userInput.title, fill="white")

                            c.text((padding, padding + 12), "Soll: {:.1f} °C".format(setTemp), fill="white")
                            c.text((padding, padding + 20), "Ist:  {:.1f} °C".format(currentTemp), fill="white")
                            c.text((padding, padding + 28), "Heizer:  {}".format("An" if heaterOn else "Aus"), fill="white")

                            current_item = userInput.get_current_item()
                            current_item_size = c.textsize(current_item)
                            c.text((device.width - padding - current_item_size[0], padding + 36), current_item, fill="white")
                        
                            if next_photo < time.monotonic():
                                logging.info("Next photo is %s" % next_photo)
                                logging.info("Current time is %s" % time.monotonic())
                                next_photo = next_photo + photo_interval_seconds
                                logging.info("Next photo plus interval is %s" % next_photo)
                                logging.info("Turning lights on")
                                light.set(True)
                                photographer.save_photo()
                                light.set(False)
                                logging.info("Turning lights off")
                    except OSError:
                        logging.exception("Error but keep going:")
                        pass

            except KeyboardInterrupt:
                pass
            except Exception:
                logging.exception("Critical Error:")
                raise

    def get_device(self):
        serial = i2c(port=1, address=0x3C)
        device = ssd1306(serial)
        return device

if __name__ == "__main__":
    Main().start()
