#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <math.h>
#include "AccelStepper.h"

#define PI (3.14159265358979)
#define dirPin 2
#define stepPin 3
#define motorInterfaceType 1
#define speedCap (500)

Adafruit_BNO055 bno = Adafruit_BNO055(55);
AccelStepper stepper = AccelStepper(motorInterfaceType, stepPin, dirPin);

// PID gains
double kP = -2000;
double kI = -200.0;
double kD = -50.0;
double setpoint = 0;

// Integral control
double inte = 0;
double integral_clipping = 3;
double windup_decay = 0.9;


// Memory
double old_error = 0;
double old_time = 0;
double old_position = 0; 

void setup(void) 
{
  Serial.begin(9600);
  Serial.println("Orientation Sensor Test\n");

  while (!bno.begin()) {
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
  }

  delay(1000);
  bno.setExtCrystalUse(true);

  old_time = millis();

  stepper.setMaxSpeed(speedCap);
  stepper.setAcceleration(50000);
  stepper.moveTo(200);  // Set target position
  stepper.runToPosition();  // Move to target position
}

void loop(void) 
{
  double x = get_ang_position();

  // Wrap error between [-PI, PI]
  double error = wrap_angle(x - setpoint);

  double dt = (millis() - old_time) / 1000.0;
  old_time = millis();
  double vx = (x - old_position)/dt;
  old_position = x;

  // Integral update with decay
  if (abs(error) < 0.2) {  // Only decay if near setpoint
    inte *= windup_decay;
  } else {
    inte += error * dt;
  }

  // Integral clipping
  inte = constrain(inte, -integral_clipping, integral_clipping);

  double u = kP * error + kI * inte - kD * vx;  // Note: using -D*v

  double out_vel = constrain(u, -speedCap, speedCap);

  print_ang_vel(error, x, vx);
  print_PID(out_vel);
  drive_motor(out_vel);

  old_error = error;

}

double get_ang_velocity(void){
  sensors_event_t angVelocityData; 
  bno.getEvent(&angVelocityData, Adafruit_BNO055::VECTOR_EULER);
  return angVelocityData.gyro.x;
}

double get_ang_position(void){
  sensors_event_t orientationData; 
  bno.getEvent(&orientationData, Adafruit_BNO055::VECTOR_EULER);
  double x = orientationData.orientation.x;
  return x * (PI / 180.0); // convert degrees to radians
}

void print_ang_vel(double error, double position, double velocity){
  Serial.print("Current Position: ");
  Serial.print(position);
  Serial.print(" rad, Current Error: ");
  Serial.print(error);
  Serial.print(" rad, Current Velocity: ");
  Serial.print(velocity);
  Serial.print(" rad/s  ");
}

void print_PID(double vel){
  Serial.print("PID vel: ");
  Serial.print(vel);
  Serial.println(" ");
}

void drive_motor(double vel) {
  stepper.setSpeed(vel); // speed in steps per second

  unsigned long time_rn = millis();
  while (millis() - time_rn < 100) { // run for 100 ms
    stepper.runSpeed(); // this runs the motor at constant speed
  }
}


// Angle wrapping between [-PI, PI]
double wrap_angle(double theta) {
  while (theta > PI)  theta -= 2 * PI;
  while (theta < -PI) theta += 2 * PI;
  return theta;
}
