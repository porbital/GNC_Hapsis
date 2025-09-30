# Control Program for the 9-21 GNC Test.

# Tests include:
# Test 1 (Equality test) - Open both nozzles and record acceleration to see if thrust is equal (specifically data[6])
# Test 2 (Left thrust test) - Open left valve for 1 second and record what happens. 
# Test 3 (Right thrust test)  - Open right valve for 1 second and record what happens
# Test 4 (Full use) - open one valve and let it use all air in tank, measure time and accel data
# Extra test - Test PID and try to tune

import time
import RPi.GPIO as GPIO
from BMI160_i2c import Driver
from datetime import datetime

# Initialize the sensor
print('Trying to initialize the sensor...')
sensor = Driver(0x69) # change address if needed
print('Initialization done')
# BEGIN CONSTANTS -------------------------------
# Define the runtime of each test (in seconds)
test1_runtime = 5
test2_runtime = 5
test3_runtime = 5
test4_runtime = 180
# Define the polling rate of the sensor (in seconds)
polling_rate = 0.05
# Initialize the relays
relay1 = 16 # assuming left
relay2 = 15 # assuming right
# END CONSTANTS --------------------------------
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay1, GPIO.OUT)
GPIO.setup(relay2, GPIO.OUT)
#--------------------------------
# 
# Test Functions
# 
#--------------------------------
# Test 1 - Equality test
# Open both nozzles and record acceleration to see if thrust is equal (specifically data[6])
# Will write data to test_data/both.csv
# Format: nozzle 1 state, nozzle 2 state, time, data[6]
def test1():
    # Create test file
    current_time4 = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"test_data/equality_{current_time4}.csv"
    file = open(file_name, "w")
    # Write a header to the file
    file.write("Nozzle 1 state,Nozzle 2 state,Time,Gyro X,Gyro Y,Gyro Z,Accel X,Accel Y,Accel Z\n")
    # Fire both nozzles for 5 seconds and record data
    start_time = time.time()
    
    GPIO.output(relay1, GPIO.LOW)
    GPIO.output(relay2, GPIO.LOW)
    
    while time.time() - start_time < test1_runtime:
        data = sensor.getMotion6()
        file.write(f"{GPIO.input(relay1)},{GPIO.input(relay2)},{round(time.time()-start_time,2)},{data[0]},{data[1]},{data[2]},{data[3]},{data[4]},{data[5]}\n")
        # write the same file.write but have it add columns for data[0] to data[5]
        time.sleep(0.1)
    # Close the file
    GPIO.output(relay1, GPIO.HIGH)
    GPIO.output(relay2, GPIO.HIGH)
    file.close()
# Test 2 - Left thrust test
# Open left valve for 1 second and record what happens.
# Will write data to test_data/left.csv
# Format: nozzle 1 state, time, data[6]
def test2():
    # Create test file
    current_time4 = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"test_data/left_{current_time4}.csv"
    file = open(file_name, "w")
    # Write a header to the file
    file.write("Nozzle 1 state,Nozzle 2 state,Time,Gyro X,Gyro Y,Gyro Z,Accel X,Accel Y,Accel Z\n")
    # Power relay 1 for 1 second and record data
    start_time = time.time()
    
    GPIO.output(relay1, GPIO.LOW)
    
    while time.time() - start_time < test2_runtime:
        data = sensor.getMotion6()
        file.write(f"{GPIO.input(relay1)},{GPIO.input(relay2)},{round(time.time()-start_time,2)},{data[0]},{data[1]},{data[2]},{data[3]},{data[4]},{data[5]}\n")
        time.sleep(0.1)
    # Close the file
    GPIO.output(relay1, GPIO.HIGH)
    file.close()
    
# Test 3 - Right thrust test
# Open left valve for 1 second and record what happens.
# Will write data to test_data/right.csv
# Format: nozzle 1 state, time, data[6]
    
def test3():
    # Create test file
    current_time4 = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"test_data/right_{current_time4}.csv"
    file = open(file_name, "w")
    
    # Write a header to the file
    file.write("Nozzle 1 state,Nozzle 2 state,Time,Gyro X,Gyro Y,Gyro Z,Accel X,Accel Y,Accel Z\n")
    # Power relay 2 for 1 second and record data
    start_time = time.time()
    
    GPIO.output(relay2, GPIO.LOW)
    
    while time.time() - start_time < test3_runtime:
        data = sensor.getMotion6()
        file.write(f"{GPIO.input(relay1)},{GPIO.input(relay2)},{round(time.time()-start_time,2)},{data[0]},{data[1]},{data[2]},{data[3]},{data[4]},{data[5]}\n")
        time.sleep(0.1)
    # Close the file
    GPIO.output(relay2, GPIO.HIGH)
    file.close()
# Test 4 - Open nozzle until empty test
# Open right valve until air runs out and record what happens.
# Will write data to test_data/open_nozzle.csv
# Format: nozzle 1 state, time, data[6]
def test4():
    # Create test file
    current_time4 = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"test_data/open_nozzle_{current_time4}.csv"
    file = open(file_name, "w")
    # Write a header to the file
    file.write("Nozzle 1 state,Nozzle 2 state,Time,Gyro X,Gyro Y,Gyro Z,Accel X,Accel Y,Accel Z\n")
    # Power relay 2 until air nozzle runs out and record data for 3 minutes
    start_time = time.time()
    GPIO.output(relay2, GPIO.LOW)
    while True:
        current_time = time.time()
        data = sensor.getMotion6()
        file.write(f"{GPIO.input(relay1)},{GPIO.input(relay2)}, {round(time.time()-start_time,2)},{data[0]},{data[1]},{data[2]},{data[3]},{data[4]},{data[5]}\n")
        if current_time - start_time >= test4_runtime: 
            GPIO.output(relay2, GPIO.HIGH)
            break
    # Close the file
    GPIO.output(relay2, GPIO.HIGH)
    file.close()
#--------------------------------
# Main control Loop
#--------------------------------
if __name__ == "__main__":
    print(r"""\ 
            ______  _______  ______        __    _____          __           __
           / ___/ |/ / ___/ /_  __/__ ___ / /_  / ___/__  ___  / /________  / /
          / (_ /    / /__    / / / -_|_-</ __/ / /__/ _ \/ _ \/ __/ __/ _ \/ / 
          \___/_/|_/\___/   /_/  \__/___/\__/__\___/\___/_//_/\__/_/  \___/_/  
         | | / /__ _______ (_)__  ___    <  // _ \                           
         | |/ / -_) __(_-</ / _ \/ _ \   / // // /                           
         |___/\__/_/ /___/_/\___/_//_/  /_(_)___/                            
                                                                     """)
    test_selected = input("Please select a test to run:\n 1. Equality test\n 2. Left thrust test\n 3. Right thrust test\n 4. Open nozzle until empty test\n")
    if test_selected == "1":
        print("Running Equality test")
        test1()
        print("Test complete")
    elif test_selected == "2":
        print("Running Left thrust test")
        test2()
        print("Test complete")
    elif test_selected == "3":
        print("Running Right thrust test")
        test3()
        print("Test complete")
    elif test_selected == "4":
        print("Running Open nozzle until empty test")
        test4()
        print("Test complete")
    elif test_selected == "5":
        GPIO.output(relay2, GPIO.HIGH)
        GPIO.output(relay1, GPIO.HIGH)
