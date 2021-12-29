from gpio import Gpio
from userInput import UserInput

from luma.core.interface.serial import i2c
import luma.core.render
from luma.core.sprite_system import framerate_regulator
from luma.oled.device import ssd1306

import smbus2
import bme280
import bme280.const as oversampling

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

        with gpio: 
            userInput = UserInput(gpio)

            heater = gpio.add_output(4, False)

            try:
                while True:
                    if userInput.exit:
                        heater.set(False)
                        os.system("sudo shutdown -h")
                        break

                    with regulator, canvas as c:
                        data = bme280.sample(bus, address, calibration_params, oversampling.x4)
                        currentTemp = data.temperature
                        setTemp = userInput.temperatureGoal

                        heaterOn = currentTemp < setTemp
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

