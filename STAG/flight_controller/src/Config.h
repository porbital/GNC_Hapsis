#ifndef CONFIG_H
#define CONFIG_H

#include <Arduino.h>

/* PIN DEFINITIONS */
//todo: update these pin numbers based on actual wiring

// Thruster Control Pins
#define THRUSTER_LEFT  10  // Positive torque
#define THRUSTER_RIGHT 11  // Negative torque

// Pyro Control Pins
#define PYRO_DETATCH_1 12
#define PYRO_DETATCH_2 13
#define PYRO_POP       14

/* TIMING */
#define LOOP_PERIOD 10 // 100Hz Loop
#define LOG_PERIOD 1000 // Log every 1 second
#define MIN_THRUSTER_PULSE 50 // Minimum thruster pulse duration in ms

/* PID CONFIG */
#define PID_KP 1.0
#define PID_KI 0.0
#define PID_KD 0.1
#define PID_DEADZONE 0.05 // Minimum output to activate thrusters



#endif