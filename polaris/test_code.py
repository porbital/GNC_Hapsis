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


#+------------------------ NOTES! IMPORTANT! ---------------------+#
# Thrusters 1 and 3 impart NEGATIVE torque on the launch structure #
# Thrusters 2 and 4 impart POSITIVE torque on the launch structure #
#+----------------------------------------------------------------+#

import time
import board # type: ignore
import digitalio
import adafruit_bno055
import busio

import adafruit_sdcard
import storage


# PID constants (Based on Simulation)
Kp = 0.56
Kd = 0.45

# Define filter time constant (Adjustable)
tau = 0.1 # Tune this value based on noise level

# Desired heading
# 0 -> North
# 90 -> East
# 180 -> South
# 270 -> West
setpoint = 0  # (Degrees) Point north

# PID variables
previous_error = 0
last_time = time.monotonic()
filtered_derivative = 0

# Thruster Control Variables
positive_thruster_on = False
negative_thruster_on = False
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

positive_thruster = digitalio.DigitalInOut(board.D12)
positive_thruster.direction = digitalio.Direction.OUTPUT

negative_thruster = digitalio.DigitalInOut(board.D13)
negative_thruster.direction = digitalio.Direction.OUTPUT

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

while (go_countdown < 5):
    yellow_led.value = True
    time.sleep(0.25)
    yellow_led.value = False
    time.sleep(0.25)
    go_countdown += 1


try:

    # Connect to the card and mount the filesystem.
    cs = digitalio.DigitalInOut(board.SD_CS)
    sd_spi = busio.SPI(board.SD_CLK, board.SD_MOSI, board.SD_MISO)
    sdcard = adafruit_sdcard.SDCard(sd_spi, cs)
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")
    
    current_time = time.localtime()
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
        #print(heading)
        return heading

    # Init log file
    with open(filename, "w") as file:
        file.write("Time,Angular Position,R Solenoid,L Solenoid,Angular Vel X,Angular Vel Y,Angular Vel Z,PID Error,P,D\n")
    
    
    # PID Loop
    while True:
               
        try:
            current_time = time.monotonic()  # Store monotonic time
            current_heading = get_current_heading()
            
            ## For data logging
            gyro_x, gyro_y, gyro_z = sensor.gyro or (999,999,999)
            
            # Compute with wraparound handling
            # This means 0 and 360 are treated the same.
            error = (setpoint - current_heading + 180) % 360 - 180
                
            # Compute delta T
            delta_time = current_time - last_time
            last_time = current_time

            # Compute Derivative
            derivative = (error - previous_error) / delta_time if delta_time > 0 else 0

            # Low-Pass filter coefficient
            alpha = delta_time / (tau + delta_time)

            # Apply low pass filter
            filtered_derivative = alpha * derivative + (1 - alpha) * filtered_derivative

            previous_error = error

            # Compute PID output
            output = (Kp * error) + (Kd * filtered_derivative)

            # Alayna, is this what you want?
            # output = (Kp * error) + ((Kd * derivative) / derivative)

            # Determine thruster activation
            ## TODO: We should never need duration
            threshold = 1  # Deadzone
            
            if abs(output) > threshold:
                if output > 0:  # Fire right thruster
                    print("Right Firing")
                    if not negative_thruster_on:
                        negative_thruster.value = True
                        negative_thruster_on = True
                        positive_thruster.value = False
                        positive_thruster_on = False

                elif output < 0:  # Fire left thruster
                    print("Left Firing")
                    if not positive_thruster_on:
                        positive_thruster.value = True
                        positive_thruster_on = True
                        negative_thruster.value = False
                        negative_thruster_on = False


            # Blink LED
            if current_time - last_toggle_time >= blink_interval:
                led_state = not led_state  # Toggle LED
                green_led.value = led_state
                last_toggle_time = current_time  # update toggle

            # Log Data to SD Card
            with open(filename, "a") as file:
                file.write(
                    f"{delta_time},{current_heading},{int(negative_thruster_on)},{int(positive_thruster_on)},{gyro_x},{gyro_y},{gyro_z},{output},{error},{derivative}\n"
                )
            
            print(error)
        except Exception as e:  # Log Errors
            print("An error occured: ", e)
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


