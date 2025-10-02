from time import sleep
from BMI160_i2c import Driver

print('Trying to initialize the sensor...')
sensor = Driver(0x68) # change address if needed
print('Initialization done')

while True:
  data = sensor.getMotion6()
  # fetch all gyro and acclerometer values
  print(round((data[5] / 16000),1))
  
  sleep(0.1)
