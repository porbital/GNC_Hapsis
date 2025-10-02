from time import sleep
from BMI160_i2c import Driver

print('Trying to initialize the sensor...')
sensor = Driver(0x68) # change address if needed
print('Initialization done')

arr_y = []
dt = 0.1 # Delta time

# ADD VARIABLE NUM_SET AND I TO NUMSTEP + 1

i = 0

while True:

    data = sensor.getMotion6()


    arr_y.append(data[3])

    # Calculate accel change over time
    
    if i > 21:
        val = (arr_y[i] - arr_y[i-19]) / (20 * dt) 

	arr_y.popleft()

        print(val)


    i += 1

    sleep(dt)
