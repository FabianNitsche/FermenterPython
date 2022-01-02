import RPi.GPIO as GPIO

class Gpio(object):
    def __init__(self):
        self.ports = []
        self.setting_output = False

    def __enter__(self):
        GPIO.setmode(GPIO.BCM)
        return self

    def __exit__(self, *args):
        GPIO.cleanup()

    def add_input(self, pin, callback):
        print("setting up input %s" % pin)
        if pin in self.ports:
            raise Exception("Input " + pin + " is already defined.")
        self.ports.append(pin)
        GpioInput(self, pin, callback)

    def add_output(self, pin, onIsHigh):
        print("setting up output %s" % pin)
        if pin in self.ports:
            raise Exception("Output " + pin + " is already defined.")
        self.ports.append(pin)
        GPIO.setup(pin, GPIO.OUT)
        return GpioOutput(self, pin, onIsHigh)


class GpioOutput(object):
    def __init__(self, gpio, pin, onIsHigh):
        self._gpio = gpio
        self.pin = pin
        self._on = GPIO.HIGH if onIsHigh else GPIO.LOW
        self._off = GPIO.LOW if onIsHigh else GPIO.HIGH
    
    def set(self, on):
        self._gpio.setting_output = True
        if on:
            GPIO.output(self.pin, self._on)
        else:
            GPIO.output(self.pin, self._off)
        self._gpio.setting_output = True

class GpioInput(object):
    def __init__(self, gpio, pin, callback):
        self._callback = callback
        self._gpio = gpio
        GPIO.setup(pin, GPIO.IN)
        GPIO.add_event_detect(pin, GPIO.RISING, bouncetime=200, callback=self._callback)

    def call_callback(self, channel):
        if not self._gpio.setting_output:
            self._callback(channel)

