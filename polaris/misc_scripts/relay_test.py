import RPi.GPIO as GPIO
import time 


relay1 = 16
relay2 = 15

GPIO.setmode(GPIO.BCM)
GPIO.setup(relay1, GPIO.OUT)
GPIO.setup(relay2, GPIO.OUT)

if __name__ == "__main__":

    while True:
        GPIO.output(relay1, GPIO.HIGH)
        GPIO.output(relay2, GPIO.HIGH)

        time.sleep(0.5)
        GPIO.output(relay1, GPIO.LOW)
        GPIO.output(relay2, GPIO.LOW)
        time.sleep(0.5)




