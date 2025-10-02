import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

RELAY_PIN1 = 18
RELAY_PIN2 = 15

GPIO.setup(RELAY_PIN1, GPIO.OUT)
GPIO.setup(RELAY_PIN2, GPIO.OUT)


try:

    while True:
        print("turning on relay 1")
        GPIO.output(RELAY_PIN1, GPIO.HIGH)

        GPIO.output(RELAY_PIN2, GPIO.LOW)

        time.sleep(1)

        print("turning on relay 2")
        GPIO.output(RELAY_PIN2, GPIO.HIGH)

        GPIO.output(RELAY_PIN1, GPIO.LOW)

        time.sleep(1)

except KeyboardInterrupt:
    print("Cleaning up GPIO")
    GPIO.cleanup()
