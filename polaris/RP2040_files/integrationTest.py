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

import adafruit_sdcardio
import storage


# PID constants (Based on Simulation)
Kp = 0.9
Ki = 0.0
Kd = 0.45

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

red_led = digitalio.DigitalInOut(board.D9)  # Change PIN if needed
red_led.direction = digitalio.Direction.OUTPUT

green_led = digitalio.DigitalInOut(board.D6)
green_led.direction = digitalio.Direction.OUTPUT

yellow_led = digitalio.DigitalInOut(board.D5)
yellow_led.direction = digitalio.Direction.OUTPUT

# Setup PINS for Mosfets

left_thruster = digitalio.DigitalInOut(board.D13)
left_thruster.direction = digitalio.Direction.OUTPUT

right_thruster = digitalio.DigitalInOut(board.D12)
right_thruster.direction = digitalio.Direction.OUTPUT

# thruster_3 = digitalio.DigitalInOut(board.D12)
# thruster_3.direction = digitalio.Direction.OUTPUT

# thruster_4 = digitalio.DigitalInOut(board.D13)
# thruster_4.direction = digitalio.Direction.OUTPUT

# Try to run the code, if an error happens, turn on
# The RED LED



#########
# Run the countdown and flash orange
#########
go_countdown = 0

while (go_countdown < 20):
    yellow_led.value = True
    time.sleep(0.25)
    yellow_led.value = False
    time.sleep(0.25)
    go_countdown += 1


try:
    # while (True):
    #   right_thruster.value = True
    #  left_thruster.value = False
    # print("on")
    # time.sleep(2)
    # right_thruster.value = False
    # left_thruster.value = True
    # print("off")
    # time.sleep(2)

    # Uncomment this to test the error detection
    # 1 / 0 # This will cause a ZeroDivisionError

    # Connect to the card and mount the filesystem.
    cs = digitalio.DigitalInOut(board.SD_CS)
    sd_spi = busio.SPI(board.SD_CLK, board.SD_MOSI, board.SD_MISO)
    sdcard = adafruit_sdcard.SDCard(sd_spi, cs)
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")
    
    filename = "/sd/log_{:04d}{:02d}{:02d}_{:02d}{:02d}{:02d}.csv".format(
    current_time.tm_year, current_time.tm_mon, current_time.tm_mday,
    current_time.tm_hour, current_time.tm_min, current_time.tm_sec)
    
    
    
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

    # Init log file
    with open(filename, "w") as file:
        file.write("Time,Angular Position,R Solenoid,L Solenoid,Angular Vel X,Angular Vel Y,Angular Vel Z,PID Error,P,I,D\n")
    
    
    # PID Loop
    while True:
        
        #while True:
            # Testing For which solenoids are firing
         #   print("Firing Left")
          #  left_thruster.value = True
           # time.sleep(5)
         #   left_thruster.value = False
         #   print("Firing Right")
         #   right_thruster.value = True
          #  time.sleep(5)
         #   right_thruster.value = False
        
        try:
            current_time = time.monotonic()  # Store monotonic time
            current_heading = get_current_heading()
            
            gyro_x, gyro_y, gyro_z = sensor.gyro or (0,0,0)
            
            # Compute with wraparound handling
            # This means 0 and 360 are treated the same.
            error = (setpoint - current_heading + 180) % 360 - 180

            # Compute delta T
            delta_time = current_time - last_time
            last_time = current_time

            # Compute Integral and Derivative
            if abs(error) > 1:
                integral += error * delta_time
            derivative = (error - previous_error) / delta_time if delta_time > 0 else 0
            previous_error = error

            # Compute PID output
            output = (Kp * error) + (Ki * integral) + (Kd * derivative)

            # Determine thruster activation
            threshold = 5  # Deadzone
            duration = 0.5  # How long the thrusters fire for
            if abs(error) > threshold:
                if output > 0 and not right_thruster_on:  # Fire right thruster
                    left_thruster.value = False  # Ensure left is off
                    left_thruster_on = False
                    right_thruster.value = True
                    right_thruster_on = True
                    thruster_off_time = current_time + duration

                elif output < 0 and not left_thruster_on:  # Fire left thruster
                    right_thruster.value = False  # Ensure right is off
                    right_thruster_on = False
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
                file.write(
                    f"{delta_time},{current_heading},{int(right_thruster_on)},{int(left_thruster_on)},{gyro_x},{gyro_y},{gyro_z},{output},{error},{integral},{derivative}\n"
                )

        except Exception:  # Log Errors
            # error_msg = str(e)
            # with open(log_filename, "a") as file:
            #    file.write(
            #        f"{time.monotonic()},ERROR,None,None,None,None,None,None,None,{error_msg}\n"
            #   )

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

