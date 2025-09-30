#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 13:44:41 2025

@author: Alayna Miller
"""

import RPi.GPIO as GPIO
from time import sleep
from BMI160_i2c import Driver

print('Trying to initialize the sensor...')
sensor = Driver(0x68) # change address if needed
print('Initialization done')

relay1 = 16
relay2 = 15

GPIO.setmode(GPIO.BCM)
GPIO.setup(relay1, GPIO.OUT)
GPIO.setup(relay2, GPIO.OUT)

# Example usage
if __name__ == "__main__":
    while True:
        data = sensor.getMotion6()
        current_value = data[2] / 16000
        
        if current_value > 0.05:
            # Fire left
            if current_value > .5: 
                GPIO.output(relay1, GPIO.LOW)
                sleep(0.1)
                GPIO.output(relay1, GPIO.HIGH)
            else:  
                GPIO.output(relay1, GPIO.LOW)
                sleep(0.01)
                GPIO.output(relay1, GPIO.HIGH)
                
        elif current_value < -0.05:
            # Fire left
            if current_value < -0.5: 
                GPIO.output(relay2, GPIO.LOW)
                sleep(0.1)
                GPIO.output(relay2, GPIO.HIGH)
            else:  
                GPIO.output(relay2, GPIO.LOW)
                sleep(0.01)
                GPIO.output(relay2, GPIO.HIGH)
            
    GPIO.output(relay1, GPIO.HIGH)
    GPIO.output(relay2, GPIO.HIGH)