#ifndef CONFIG_H
#define CONFIG_H

#include <Arduino.h>

/* PIN DEFINITIONS */

// Thruster Control Pins
#define THRUSTER_LEFT  6  // Positive torque
#define THRUSTER_RIGHT 7  // Negative torque

// Pyro Control Pins
#define PYRO_DETATCH_1 8 
#define PYRO_DETATCH_2 9 
#define PYRO_POP       2 

/* TIMING */
#define LOOP_PERIOD 10 // 100Hz Loop
#define LOG_PERIOD  100 // 10Hz Logging 
#define MIN_THRUSTER_PULSE 50 // Minimum thruster pulse duration in ms
#define ABORT_FIRE_PYRO_TIME 10000 // Time after which to fire pyro if GNC fails (ms) - 10 minutes

/* PID CONFIG */
#define PID_KP 1.0
#define PID_KI 0.0
#define PID_KD 0.6

#define THRESHOLD_ON 5.0 // Control Effort needed to turn on thrusters
#define THRESHOLD_OFF 2.0 // Control Effort needed to turn off thrusters 
#define MIN_THRUSTER_PULSE 50 // Minimum thruster pulse duration in ms


/* GNC CONFIG */
#define HEADING 0 // Desired heading in degrees
#define HEADING_THRESHOLD 5 // Degrees of error allowed 
#define HEADING_HOLD_TIME 3000 // Time that GNC must be withing heading threshold to trigger pyro (ms)
#define GNC_TIME 30000 // Maximum time to stay in GNC_ACTIVE state before transitioning to PYRO_FIRED (ms) - 30 seconds


#define TARGET_ALTITUDE 250 // Altitude to trigger GNC activation (meters) 1524 meters = 5000 feet
/* 5000 feet */
#define GNC_ACTIVATION_VELOCITY 1.0 // Vertical velocity threshold to trigger GNC (m/s)


/* DESCENT & LANDING CONFIG */
#define DESCENT_VELOCITY_THRESHOLD -0.5   // Vertical velocity threshold to trigger descent state (m/s)
#define LANDING_VELOCITY_THRESHOLD  0.1 // Vertical velocity threshold to trigger landing (m/s)
#define ALTITUDE_LANDING_THRESHOLD 50 // Altitude threshold to trigger landing (meters)


/* HARDWARE IN THE LOOP SHIM*/
// MAKE SURE TO COMMENT OUT BEFORE FLIGHT
//#define HIL_MODE


#endif