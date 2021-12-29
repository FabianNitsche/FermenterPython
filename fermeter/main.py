from gpio import Gpio, GpioOutput
from luma.core.interface.serial import i2c
import luma.core.render
from luma.core.sprite_system import framerate_regulator
from luma.oled.device import ssd1306

import smbus2
import bme280
import bme280.const as oversampling

class Main(object):
    def __init__(self):
        self.tempGoal = 30
        
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
            def increment_temp(channel):
                self.tempGoal += 1
            def decrement_temp(channel):
                self.tempGoal -= 1

            gpio.add_input(23, increment_temp)
            gpio.add_input(24, decrement_temp)

            heater = gpio.add_output(4, False)

            try:
                while True:
                    with regulator, canvas as c:
                        data = bme280.sample(bus, address, calibration_params, oversampling.x4)
                        currentTemp = data.temperature

                        heaterOn = currentTemp < self.tempGoal
                        heater.set(heaterOn)

                        c.rectangle(device.bounding_box, fill="black")
                        c.text((padding, padding + 4), "Soll: {:.1f} °C".format(self.tempGoal), fill="white")
                        c.text((padding, padding + 12), "Ist:  {:.1f} °C".format(currentTemp), fill="white")
                        c.text((padding, padding + 20), "Heater:  {}".format("On" if heaterOn else "Off"), fill="white")
            except KeyboardInterrupt:
                pass

    def get_device(self):
        serial = i2c(port=1, address=0x3C)
        device = ssd1306(serial)
        return device


if __name__ == "__main__":
    Main().start()

