import RPi.GPIO as GPIO
import time
from BMI160_i2c import Driver

## This PID controller controls both degree attitude and angular velocity.
## Alayna Miller 2/2/25

print('Trying to initialize the sensor...')
angvel_sensor = Driver(0x68) # change address if needed
print('Initialization done')

### INITIALIZE DEGREE DATA SENSOR HERE
degree_sensor = 0 ##this is where the sensor should be

relay1 = 15
relay2 = 16

### DEGREE SENSOR TEMP
deg_setpoint = 0


GPIO.setmode(GPIO.BCM)
GPIO.setup(relay1, GPIO.OUT)
GPIO.setup(relay2, GPIO.OUT)

GPIO.output(relay1, GPIO.HIGH)
GPIO.output(relay2, GPIO.HIGH)

class PID:
    def __init__(self, Kp, Ki, Kd, deg_setpoint, angvel_setpoint):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.angvel_setpoint = angvel_setpoint
        self.deg_setpoint = deg_setpoint
        self.prev_error = 0
        self.integral = 0

    def update(self, angvel_current, deg_current):
        angvel_error = self.angvel_setpoint - angvel_current
        deg_error = self.deg_setpoint - deg_current
        self.integral += angvel_error # this line doesnt consider degree error bc not f(t)
        angvel_derivative = angvel_error - self.angvel_prev_error
        # this line doesnt consider degree error bc not f(t)
        output = self.Kp * deg_error + self.Ki * self.integral + self.Kd * angvel_derivative 
        
        self.angvel_prev_error = angvel_error
        self.deg_prev_error = deg_error
        return output

# Example usage
if __name__ == "__main__":
    pid = PID(1, 0.0, 0.4, 15, 0)  # Example PID parameters and setpoint
    while True:
        angvel_data = angvel_sensor.getMotion6()
        degree_data = degree_sensor.getMotion()
        
        angvel_current = angvel_data[1] / 16000
        degree_current = degree_data[1] ## adjust this !!!!!!!!!!!
        
        control_signal = pid.update(angvel_current, degree_current)

        GPIO.output(relay1, GPIO.HIGH)
        GPIO.output(relay2, GPIO.HIGH)

        if control_signal > 0.05:
            # Fire left
            GPIO.output(relay1, GPIO.LOW)
            print("firing left")
            time.sleep(0.1)
            GPIO.output(relay1, GPIO.HIGH)

        elif control_signal < -0.05:
            # Fire right 
            GPIO.output(relay2, GPIO.LOW)
            print("firing right")
            time.sleep(0.1)
            GPIO.output(relay2, GPIO.HIGH)




