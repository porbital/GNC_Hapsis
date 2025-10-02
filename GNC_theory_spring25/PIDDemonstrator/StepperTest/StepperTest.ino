#include "AccelStepper.h"

// Define stepper motor connections and motor interface type. Motor interface type must be set to 1 when using a driver:
#define dirPin 2
#define stepPin 3
#define motorInterfaceType 1

#define speedCap (1000)

// Create a new instance of the AccelStepper class:
AccelStepper stepper = AccelStepper(motorInterfaceType, stepPin, dirPin);

void setup() {
  // Set the maximum speed and acceleration:
  stepper.setMaxSpeed(1000);
  stepper.setAcceleration(50000);
}

float speed = 0;

/*
 * Func to set torque of motor, increases set speed until cap
 * by torque amt
 */

void setTorque(float torque) {
  if ((speed + torque <= speedCap) && (speed + torque >= 0)) {
    speed += torque;
  }
}

void loop() {
  setTorque(-.01);
  stepper.setSpeed(speed);
  stepper.runSpeed();
}