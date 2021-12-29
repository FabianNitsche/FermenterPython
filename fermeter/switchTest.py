import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(24, GPIO.IN)
GPIO.setup(23, GPIO.IN)
GPIO.setup(25, GPIO.OUT)

# Endlosschleife
try:
    while True:
        if GPIO.input(24) == 0 and GPIO.input(23) == 0:
            # Ausschalten
            print("low")
            GPIO.output(25, GPIO.LOW)
        else:
            # Einschalten
            print("high")
            GPIO.output(25, GPIO.HIGH)
except:
    GPIO.cleanup()