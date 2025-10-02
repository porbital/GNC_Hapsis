import RPi.GPIO as GPIO
from time import sleep
from BMI160_i2c import Driver

print('Trying to initialize the sensor...')
sensor = Driver(0x68) # change address if needed
print('Initialization done')

relay1 = 16
relay2 = 15

GPIO.setmode(GPIO.BCM)
GPIO.setup(relay1, GPIO.OUT)
GPIO.setup(relay2, GPIO.OUT)

class PID:
    def __init__(self, Kp, Ki, Kd, setpoint):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.prev_error = 0
        self.integral = 0

    def update(self, current_value):
        error = self.setpoint - current_value
        self.integral += error
        derivative = error - self.prev_error
        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        self.prev_error = error
        return output

# Example usage
if __name__ == "__main__":
    pid = PID(0.25, 0.01, 0.05, 0)  # Example PID parameters and setpoint
    
    while True:
        data = sensor.getMotion6()
        # Old version
        # current_value = data[4] / 16000
        current_value = round((data[5] / 16000),1)

        print("Current IMU Data: ",current_value)
        control_signal = pid.update(current_value)
        print("PID Value: ", control_signal)

        GPIO.output(relay1, GPIO.LOW)
        GPIO.output(relay2, GPIO.LOW)

        if control_signal > 0.2:
            # Fire left
            print("Turning left maybe")
            GPIO.output(relay1, GPIO.HIGH)
            sleep(0.1)
            GPIO.output(relay1, GPIO.LOW)

        elif control_signal < -0.2:
            # Fire right 
            print("Turning right maybe")
            GPIO.output(relay2, GPIO.HIGH)
            sleep(0.1)
            GPIO.output(relay2, GPIO.LOW)



        sleep(0.01)



