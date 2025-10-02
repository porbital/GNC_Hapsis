from time import sleep
from BMI160_i2c import Driver

print('Trying to initialize the sensor...')
sensor = Driver(0x68) # change address if needed
print('Initialization done')


upper_bound = 1500 
lower_bound = -1500
while True:

    data = sensor.getMotion6()
    
    if (data[3] > 5000):
        print("Turn neg")

    elif (data[3] < -5000):
        print("Turn pos")
    else:
        print(".")


    sleep(0.3)
