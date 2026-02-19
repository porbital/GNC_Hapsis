// Actuators -- Thruster and pyro control

#include "Actuators.h"

static bool leftThrusterOn = false;
static bool rightThrusterOn = false;
static unsigned long thrusterOnTime = 0;

void initActuators() {
  // Configure thruster pins
  pinMode(THRUSTER_LEFT, OUTPUT);
  pinMode(THRUSTER_RIGHT, OUTPUT);
  
  // Configure pyro pins
  pinMode(PYRO_DETATCH_1, OUTPUT);
  pinMode(PYRO_DETATCH_2, OUTPUT);
  pinMode(PYRO_POP, OUTPUT);
  
  // Ensure all outputs are off
  disableAllActuators();
  
  Serial.println("Thrusters and Pyro initialized");
}

void controlThrusters(float pidOutput) {
  // Apply deadzone
  // If output is within deadzone, turn off thrusters
  if (abs(pidOutput) < PID_DEADZONE) {
    digitalWrite(THRUSTER_LEFT, LOW);
    digitalWrite(THRUSTER_RIGHT, LOW);
    leftThrusterOn = false;
    rightThrusterOn = false;
    return;
  }
  
  // Determine which thruster to fire
  if (pidOutput > 0) {
    // Fire LEFT thruster (positive torque)
    if (!leftThrusterOn) {
      digitalWrite(THRUSTER_LEFT, HIGH);
      digitalWrite(THRUSTER_RIGHT, LOW);
      leftThrusterOn = true;
      rightThrusterOn = false;
      thrusterOnTime = millis();
    }
  } else {
    // Fire RIGHT thruster (negative torque)
    if (!rightThrusterOn) {
      digitalWrite(THRUSTER_LEFT, LOW);
      digitalWrite(THRUSTER_RIGHT, HIGH);
      leftThrusterOn = false;
      rightThrusterOn = true;
      thrusterOnTime = millis();
    }
  }
  
  // Enforce minimum pulse duration
  if ((leftThrusterOn || rightThrusterOn) && 
      (millis() - thrusterOnTime < MIN_THRUSTER_PULSE)) {
    // Keep thruster on for minimum duration
    return;
  }
}

void firePyros() {
  Serial.println("FIRING PYRO CHARGES!");
  
  // Fire both pyro channels
  // TODO: change this to fire sequentially, implement continuity.
  digitalWrite(PYRO_DETATCH_1, HIGH);
  digitalWrite(PYRO_DETATCH_2, HIGH);
  digitalWrite(PYRO_POP, HIGH);
 
  // TODO: add non-blocking timing to turn off after 1 second, and implement continuity checks


  
  // Turn off pyro channels
  digitalWrite(PYRO_DETATCH_1, LOW);
  digitalWrite(PYRO_DETATCH_2, LOW);
  digitalWrite(PYRO_POP, LOW);
  
  Serial.println("Pyro firing complete");
}

void disableAllActuators() {
  digitalWrite(THRUSTER_LEFT, LOW);
  digitalWrite(THRUSTER_RIGHT, LOW);
  digitalWrite(PYRO_DETATCH_1, LOW);
  digitalWrite(PYRO_DETATCH_2, LOW);
  digitalWrite(PYRO_POP, LOW);
  
  leftThrusterOn = false;
  rightThrusterOn = false;
}

bool getLeftThrusterState() {
  return leftThrusterOn;
}

bool getRightThrusterState() {
  return rightThrusterOn;
}