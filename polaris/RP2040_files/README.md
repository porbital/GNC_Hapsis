# Setup Procedure for Adalogger and IMU

### CircuitPython
 
Our code is written in CircuitPython.

Magnetometer data is pulled BNO055 Adafruit IMU.

In order to use this properly, ensure that the following libraries
are installed.

`adafruit_bno055.py`

`adafruit_bus_device`

`adafruit_register`

**Steps to setup**

Ensure drivers are in the `\lib` directory of the microcontroller.

Copy the `heading_data` code into the Circuitpython `main.py` file

Run!
