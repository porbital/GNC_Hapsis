// Actuators -- Thruster and pyro control

#include "Actuators.h"

static bool leftThrusterOn = false;
static bool rightThrusterOn = false;
static bool pyroFiring = false;
static unsigned long pyroStartTime = 0;
static unsigned long thrusterOnTime = 0;
unsigned long headingHoldStartTime = 0;
static int pyroSequenceStep = 0;

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

bool headingReached(float currentHeading, float targetHeading) {
  // Check if current heading is within a certain threshold of target
  // AND is holding there for 3 seconds

  if (abs(currentHeading - targetHeading) < HEADING_THRESHOLD) {
    if (headingHoldStartTime == 0) {
      headingHoldStartTime = millis();
    } else if (millis() - headingHoldStartTime >= HEADING_HOLD_TIME) {
      return true; // Heading reached and held
    }
  } else {
    headingHoldStartTime = 0; // Reset timer if we deviate
  }
  return false;
  // NEED TO CHANGE
}

void controlThrusters(float controlEffort) {
  unsigned long currentTime = millis();

  // If a thruster is currently on AND the minimum pulse time hasn't elapsed, 
  // return immediately.
  if ((leftThrusterOn || rightThrusterOn) && 
      (currentTime - thrusterOnTime < MIN_THRUSTER_PULSE)) {
    return;
  }
  
  // Turn ON when effort exceeds the high threshold.
  if (controlEffort > THRESHOLD_ON) {
    // Fire LEFT thruster (positive torque)
    if (!leftThrusterOn) {
      digitalWrite(THRUSTER_LEFT, HIGH);
      digitalWrite(THRUSTER_RIGHT, LOW);
      leftThrusterOn = true;
      rightThrusterOn = false;
      thrusterOnTime = currentTime;
    }
  } 
  else if (controlEffort < -THRESHOLD_ON) {
    // Fire RIGHT thruster (negative torque)
    if (!rightThrusterOn) {
      digitalWrite(THRUSTER_LEFT, LOW);
      digitalWrite(THRUSTER_RIGHT, HIGH);
      leftThrusterOn = false;
      rightThrusterOn = true;
      thrusterOnTime = currentTime;
    }
  } 
  // Turn OFF only when effort drops below the low threshold.
  else if (abs(controlEffort) < THRESHOLD_OFF) {
    if (leftThrusterOn || rightThrusterOn) {
      digitalWrite(THRUSTER_LEFT, LOW);
      digitalWrite(THRUSTER_RIGHT, LOW);
      leftThrusterOn = false;
      rightThrusterOn = false;
    }
  }
  
}


/*
  Event Order:
  -> Fire PYRO_DETACH_2 (middle charge)
  -> Wait 5 seconds
  -> Is velocity negative? If yes, transition to DESCENT
  -> If not, Fire PYRO_DETACH_1
  -> Wait 5 seconds
  -> Is velocity negative? If yes, transition to DESCENT
  -> If not, Fire PYRO_POP
  -> Wait 5 seconds
  -> Is velocity negative? If yes, transition to DESCENT
*/
bool firePyros(float vertical_vel) {
  unsigned long currentTime = millis();

  if (!pyroFiring) {
    Serial.println("FIRING PYRO 2");
    digitalWrite(PYRO_DETATCH_2, HIGH);
    pyroFiring = true;
    pyroStartTime = currentTime;
    pyroSequenceStep = 1;
  }

  if (pyroSequenceStep == 1 && (currentTime - pyroStartTime >= 5000)) {
    digitalWrite(PYRO_DETATCH_2, LOW);
    if (vertical_vel < -1) {
      pyroSequenceStep = 4;
    } else {
      Serial.println("FIRING PYRO 1!");
      digitalWrite(PYRO_DETATCH_1, HIGH);
      pyroStartTime = currentTime;
      pyroSequenceStep = 2;
    }
  }
else if (pyroSequenceStep == 2 && (currentTime - pyroStartTime >= 5000)) {
    digitalWrite(PYRO_DETATCH_1, LOW);
    if (vertical_vel < -1) {
      pyroSequenceStep = 4;
    } else {
      Serial.println("FIRING PYRO 3!");
      digitalWrite(PYRO_POP, HIGH);
      pyroStartTime = currentTime;
      pyroSequenceStep = 3;
    }
  }
  else if (pyroSequenceStep == 3 && (currentTime - pyroStartTime >= 5000)) {
    digitalWrite(PYRO_POP, LOW);
    pyroSequenceStep = 4; 
  }

  if (pyroSequenceStep == 4) {
    disableAllActuators();
    pyroFiring = false;
    pyroSequenceStep = 0;
    Serial.println("Pyro sequence complete, actuators disabled, transitioning to DESCENT");
    return true; // One of the pyros worked, so return true to trigger state transition
  }

  return false;
   
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

bool isPyroFiring() {
  return pyroFiring;
}

bool getLeftThrusterState() {
  return leftThrusterOn;
}

bool getRightThrusterState() {
  return rightThrusterOn;
}