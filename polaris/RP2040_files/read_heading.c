# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
# import busio
import adafruit_bno055


i2c = board.I2C()  # uses board.SCL and board.SDA

# i2c = busio.I2C(board.SCL, board.SDA)

# while not i2c.try_lock():
#    pass
# print("Scanning I2C bus...")


# devices = i2c.scan()

# if devices:
#    print("I2C devices found: ", [hex(device) for device in devices])
# else:
#    print("NO i2c devices found.")

# i2c.unlock()
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on 
sensor = adafruit_bno055.BNO055_I2C(i2c)

# If you are going to use UART uncomment these lines
# uart = board.UART()
# sensor = adafruit_bno055.BNO055_UART(uart)

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
    #print("Euler angle: {}".format(sensor.euler))
    heading = sensor.euler[0]
    #print_heading(heading)
    print(heading)
   # print("Quaternion: {}".format(sensor.quaternion))
    #print("Linear acceleration (m/s^2): {}".format(sensor.linear_acceleration))
   # print("Gravity (m/s^2): {}".format(sensor.gravity))
   # print()

    time.sleep(0.1)

