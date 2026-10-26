// Thruster and pyro control

#ifndef ACTUATORS_H
#define ACTUATORS_H

#include <Arduino.h>
#include "Config.h"

// Initialize actuator pins
void initActuators();

// Command thrusters
void controlThrusters(float pidOutput);

// Fire pyro channels
bool firePyros(float vertical_vel);

// Disable all actuators (safety)
void disableAllActuators();

// Get thruster states (for logging)
bool getLeftThrusterState();
bool getRightThrusterState();
#endif // ACTUATORS_H