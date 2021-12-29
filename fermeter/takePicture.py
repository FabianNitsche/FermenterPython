from picamera import PiCamera
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)

#try:
GPIO.output(25, GPIO.HIGH)

camera = PiCamera()
time.sleep(2)
camera.brightness = 60
camera.contrast = 20
camera.capture("/home/pi/FermenterPython/Pictures/img.jpg")
print("Done.")
GPIO.output(25, GPIO.LOW)

#except:
#    GPIO.output(25, GPIO.LOW)
GPIO.cleanup()