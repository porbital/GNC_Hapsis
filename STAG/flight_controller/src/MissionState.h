#ifndef MISSION_STATE_H
#define MISSION_STATE_H

#include <Arduino.h>

// Enum to store mission state
enum MissionState {
    GROUND,     // On the ground, pre-launch
    ARMED,      // Armed and Ready
    ASCENT,     // Payload is ascending
    GNC_ACTIVE, // GNC Turned On
    PYRO_FIRED, // Pyros Fired
    LANDED      // Payload has landed
};

// Convert mission state to a string for data loggin
const char* stateToString(MissionState state);

// Mission State Variable
extern volatile MissionState currentState;
extern volatile MissionState previousState;

// Switch States
void transitionToState(MissionState newState);

// Timing
extern unsigned long stateStartTime;
extern unsigned long gncStartTime;

#endif