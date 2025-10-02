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
#define speedCap (100000)

Adafruit_BNO055 bno = Adafruit_BNO055(55);
AccelStepper stepper = AccelStepper(motorInterfaceType, stepPin, dirPin);

// PID gains
double kP = 100000;
double kI = 0.0;
double kD = 0.0;
double setpoint = 0;

// Integral control
double inte = 0;
double integral_clipping = 3;
double windup_decay = 0.9;

// Low-pass filter
double alpha = 0.8;
double filtered_vx = 0;

// Memory
double old_error = 0;
double old_time = 0;

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
  double vx = get_ang_velocity();

  // Apply low-pass filter
  filtered_vx = alpha * filtered_vx + (1 - alpha) * vx;

  // Wrap error between [-PI, PI]
  double error = wrap_angle(x - setpoint);

  double dt = (millis() - old_time) / 1000.0;
  old_time = millis();

  // Integral update with decay
  if (abs(error) < 0.05) {  // Only decay if near setpoint
    inte *= windup_decay;
  } else {
    inte += error * dt;
  }

  // Integral clipping
  inte = constrain(inte, -integral_clipping, integral_clipping);

  double u = kP * error + kI * inte - kD * filtered_vx;  // Note: using -D*v

  double out_vel = constrain(u, -speedCap, speedCap);


  print_ang_vel(x, vx);
  print_PID(out_vel);
  drive_motor(out_vel);

  old_error = error;

  delay(100);
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

void print_ang_vel(double position, double velocity){
  Serial.print("Current Position: ");
  Serial.print(position);
  Serial.print(" rad, Current Velocity: ");
  Serial.print(velocity);
  Serial.print(" rad/s  ");
}

void print_PID(double vel){
  Serial.print("PID vel: ");
  Serial.print(vel);
  Serial.println(" m/s");
}

void drive_motor(double vel){
  stepper.setSpeed(vel);
  stepper.runSpeed();
  delay(50)
}

// Angle wrapping between [-PI, PI]
double wrap_angle(double theta) {
  while (theta > PI)  theta -= 2 * PI;
  while (theta < -PI) theta += 2 * PI;
  return theta;
}
