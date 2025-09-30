# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Purdue Orbital GNC -- Polaris Program

# PINOUT DIAGRAM
# +------------+
# SCL = SCL on IMU
# SDA = SDA on IMU
# 3.3v = VIN on IMU
#
# D5 = RED LED
# D6 = GREEN LED
# D9 = YELLOW LED
#
# D10 = Thruster 1
# D11 = Thruster 2
# D12 = Thruster 3
# D13 = Thruster 4
#
# GND: LEDS, IMU, Mosfets
# +--------------+

import time
import board
import digitalio
import adafruit_bno055


# Setup LEDs to display status
# RED = FAILURE
# GREEN Blinking = Alive and Running
# YELLOW Blinking = Waiting for Avionics Send

red_led = digitalio.DigitalInOut(board.D5)  # Change PIN if needed
red_led.direction = digitalio.Direction.OUTPUT

green_led = digitalio.DigitalInOut(board.D6)
green_led.direction = digitalio.Direction.OUTPUT

yellow_led = digitalio.DigitalInOut(board.D9)
yellow_led.direction = digitalio.Direction.OUTPUT

# Setup PINS for Mosfets

thruster_1 = digitalio.DigitalInOut(board.D10)
thruster_1.direction = digitalio.Direction.OUTPUT

thruster_2 = digitalio.DigitalInOut(board.D11)
thruster_2.direction = digitalio.Direction.OUTPUT

thruster_3 = digitalio.DigitalInOut(board.D12)
thruster_3.direction = digitalio.Direction.OUTPUT

thruster_4 = digitalio.DigitalInOut(board.D13)
thruster_4.direction = digitalio.Direction.OUTPUT

# Try to run the code, if an error happens, turn on
# The RED LED

try:

    # Uncomment this to test the error detection
    # 1 / 0 # This will cause a ZeroDivisionError

    # Setup Monotonic Timer (will not interfere
    # with clock speed of IMU)
    led_state = False
    last_toggle_time = time.monotonic()
    blink_interval = 0.5  # LED Blink rate (sec)

    i2c = board.I2C()  # uses board.SCL and board.SDA

    sensor = adafruit_bno055.BNO055_I2C(i2c)  # connects to sensor

    last_val = 0xFFFF

    def temperature():
        global last_val  # pylint: disable=global-statement
        result = sensor.temperature
        if abs(result - last_val) == 128:
            result = sensor.temperature
            if abs(result - last_val) == 128:
                return 0b00111111 & result
        last_val = result
        return result

    while True:
        # print("Euler angle: {}".format(sensor.euler))
        # print("Quaternion: {}".format(sensor.quaternion))
        # print("Linear acceleration (m/s^2): {}".format(sensor.linear_acceleration))
        # print("Gravity (m/s^2): {}".format(sensor.gravity))

        heading = sensor.euler[0]
        print(heading)

        time.sleep(0.1)

        # Blink LED
        current_time = time.monotonic()
        if current_time - last_toggle_time >= blink_interval:
            led_state = not led_state  # Toggle LED
            green_led.value = led_state
            last_toggle_time = current_time  # update toggle

except Exception as e:
    print("An error occured: ", e)

    # An error happened, flash RED LED
    while True:
        red_led.value = True
        time.sleep(0.25)
        red_led.value = False
        time.sleep(0.25)

