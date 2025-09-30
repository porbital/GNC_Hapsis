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
# D10 = Thruster L
# D11 = Thruster R
# D12 = Thruster 3
# D13 = Thruster 4
# Note: Currently just firing L/R, so wire the opposing
#       thrusters togehter. D12 and D13 should not be needed.
# GND: LEDS, IMU, Mosfets
# +--------------+

import time
import board
import digitalio
import adafruit_bno055
import sdcardio
import storage
import os
import microcontroller


# PID constants (need to tune)
Kp = 1.5
Ki = 0.01
Kd = 0.5

# Desired heading
# 0 -> North
# 90 -> East
# 180 -> South
# 270 -> West
setpoint = 0  # Point north

# PID variables
integral = 0
previous_error = 0
last_time = time.monotonic()

# Thruster Control Variables
left_thruster_on = False
right_thruster_on = False
thruster_off_time = 0  # When to turn off the thruster

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

left_thruster = digitalio.DigitalInOut(board.D10)
left_thruster.direction = digitalio.Direction.OUTPUT

right_thruster = digitalio.DigitalInOut(board.D11)
right_thruster.direction = digitalio.Direction.OUTPUT

# thruster_3 = digitalio.DigitalInOut(board.D12)
# thruster_3.direction = digitalio.Direction.OUTPUT

# thruster_4 = digitalio.DigitalInOut(board.D13)
# thruster_4.direction = digitalio.Direction.OUTPUT

# Try to run the code, if an error happens, turn on
# The RED LED

# Setup SD CARD
spi = board.SPI()
cs = board. D4  # Might need to change this
sd_card = sdcardio.SDCard(spi, digitalio.DigitalInOut(cs))
vfs = storage.VfsFat(sd_card)
storage.mount(vfs, "/sd")

log_filename = "/sd/datalog.csv"

# Initilize log file
if not log_filename in os.listdir("/sd"):
    with open(log_filename, "w") as file:
        file.write("Time,Heading,Thruster_L,Thruster_R,Delta_Time,Error,Output,Integral,Derivative,Exception\n")
        
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

    # Function to get current heading
    def get_current_heading():
        heading = sensor.euler[0]
        print(heading)
        return heading
    
    # PID Loop
    while True:
        try:
            current_time = time.monotonic()  # Store monotonic time
            current_heading = get_current_heading()
            
            # Compute with wraparound handling
            # This means 0 and 360 are treated the same.
            error = (setpoint - current_heading + 180) % 360 - 180
            
            # Compute delta T
            delta_time = current_time - last_time
            last_time = current_time
            
            # Compute Integral and Derivative
            # Uses Anti-Windup to prevent unnecessary integral accumulation
            if abs(error) > 1:
                integral += error * delta_time
            derivative = (error - previous_error) / delta_time if delta_time > 0 else 0
            previous_error = error
            
            # Compute PID output
            output = (Kp * error) + (Ki * integral) + (Kd * derivative)
            
            # Determine thruster activation
            # Scales thruster activation. Min 0.1s, Max 1s
            threshold = 1  # Deadzone
            if abs(error) > threshold:
                duration = min(abs(output) * 0.1, 1) 
               
                if output > 0 and not right_thruster_on:  # Fire right_thruster
                    right_thruster.value = True
                    right_thruster_on = True
                    thruster_off_time = current_time + duration
                
                elif output < 0 and not left_thruster_on:  # Fire left_thruster
                    left_thruster.value = True
                    left_thruster_on = True
                    thruster_off_time = current_time + duration
                
            # Check if we should turn off thrusters
            if right_thruster_on and current_time >= thruster_off_time:
                right_thruster.value = False
                right_thruster_on = False
            
            if left_thruster_on and current_time >= thruster_off_time:
                left_thruster.value = False
                left_thruster_on = False

            # Blink LED
            if current_time - last_toggle_time >= blink_interval:
                led_state = not led_state  # Toggle LED
                green_led.value = led_state
                last_toggle_time = current_time  # update toggle
            
            # Log Data to SD Card
            with open(log_filename, "a") as file:
                file.write(f"{current_time},{current_heading},{left_thruster_on},{right_thruster_on},{delta_time},{error},{output},{integral},{derivative},None\n")
        
        except Exception as e:  # Log Errors
            error_msg = str(e)
            with open(log_filename, "a") as file:
                file.write(f"{time.monotonic()},ERROR,None,None,None,None,None,None,None,{error_msg}\n")
            
            # Flash RED LED indefinitely on error
            while True:
                red_led.value = True
                time.sleep(0.25)
                red_led.value = False
                time.sleep(0.25)

except Exception as e:
    print("An error occured: ", e)
    # An error happened, flash RED LED
    while True:
        red_led.value = True
        time.sleep(0.25)
        red_led.value = False
        time.sleep(0.25)

