import RPi.GPIO as GPIO
import time
from BMI160_i2c import Driver
print('Trying to initialize the sensor...')
sensor = Driver(0x69) # change address if needed
print('Initialization done')
relay1 = 15
relay2 = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay1, GPIO.OUT)
GPIO.setup(relay2, GPIO.OUT)

# Example usage
if __name__ == "__main__":
    try:
        current_time4 = 4 
        file_name = f"11-11-test/PID_boiled_{current_time4}.csv"
        file = open(file_name, "w")
        # Write a header to the file
        file.write("Nozzle 1 state,Nozzle 2 state,Time,Vel Y\n")
        start_time = time.time()
        while True:
            data = sensor.getMotion6()
            current_value = data[1] / 16000
            current_time = time.time()
            data = sensor.getMotion6()
            file.write(f"{GPIO.input(relay1)},{GPIO.input(relay2)}, {round(time.time()-start_time,2)},{data[1]}\n")

            if current_value > 0.05:
                # Fire left
                GPIO.output(relay2, GPIO.LOW)
                time.sleep(0.1)
                GPIO.output(relay2, GPIO.HIGH)
            elif current_value < -0.05:
                # Fire left
                GPIO.output(relay1, GPIO.LOW)
                time.sleep(0.1)
                GPIO.output(relay1, GPIO.HIGH)

        GPIO.output(relay1, GPIO.HIGH)
        GPIO.output(relay2, GPIO.HIGH)
    except KeyboardInterrupt:
        GPIO.cleanup()
        file.close()
        print('Test aborted, cleaning up GPIO and closing file') 
