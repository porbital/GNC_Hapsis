#include "MissionState.h"

volatile MissionState currentState = GROUND;
volatile MissionState previousState = GROUND;

unsigned long stateStartTime = 0;
unsigned long gncStartTime = 0;

const char* stateToString(MissionState state) {
    switch (state) {
        case GROUND: return "GROUND";
        case ARMED: return "ARMED";
        case ASCENT: return "ASCENT";
        case GNC_ACTIVE: return "GNC_ACTIVE";
        case PYRO_FIRED: return "PYRO_FIRED";
        case LANDED: return "LANDED";
    }
}

void transitionToState(MissionState newState) {
    previousState = currentState;
    currentState = newState;
    stateStartTime = millis();
    
    // If we just entered GNC_ACTIVE, record the start time
    if (newState == GNC_ACTIVE) {
        gncStartTime = millis();
    }

    // New state? Log it.
    Serial.println("EVENT: Transitioned to state " + String(stateToString(newState)));
}