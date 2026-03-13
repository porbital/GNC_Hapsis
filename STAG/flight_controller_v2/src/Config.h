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
#define LOG_PERIOD  100 // 10Hz Logging 
#define MIN_THRUSTER_PULSE 50 // Minimum thruster pulse duration in ms

/* PID CONFIG */
#define PID_KP 1.0
#define PID_KI 0.0
#define PID_KD 0.1
#define PID_DEADZONE 0.05 // Minimum output to activate thrusters


/* GNC CONFIG */
#define HEADING 0 // Desired heading in degrees
#define HEADING_THRESHOLD 5 // Degrees of error allowed 
#define HEADING_HOLD_TIME 3000 // Time that GNC must be withing heading threshold to trigger pyro (ms)


#define TARGET_ALTITUDE 1524  // Altitude to trigger GNC activation (meters)
/* 5000 feet */
#define GNC_ACTIVATION_ACCEL 2.0 // Vertical acceleration threshold to trigger GNC (m/s^2)


#endif