import RPi.GPIO as GPIO

class Gpio(object):
    def __init__(self):
        self.ports = []

    def __enter__(self):
        GPIO.setmode(GPIO.BCM)
        return self

    def __exit__(self, *args):
        GPIO.cleanup()

    def add_input(self, pin, callback):
        if pin in self.ports:
            raise Exception("Input " + pin + " is already defined.")
        self.ports.append(pin)
        GPIO.setup(pin, GPIO.IN)
        GPIO.add_event_detect(pin, GPIO.RISING, bouncetime=200, callback=callback)

    def add_output(self, pin, onIsHigh):
        if pin in self.ports:
            raise Exception("Input " + pin + " is already defined.")
        self.ports.append(pin)
        GPIO.setup(pin, GPIO.OUT)
        return GpioOutput(pin, onIsHigh)


class GpioOutput(object):
    def __init__(self, pin, onIsHigh):
        self.pin = pin
        self._on = onIsHigh if GPIO.HIGH else GPIO.LOW
        self._off = onIsHigh if GPIO.LOW else GPIO.HIGH
    
    def set(self, on):
        if on:
            GPIO.output(self.pin, self._on)
        else:
            GPIO.output(self.pin, self._off)
