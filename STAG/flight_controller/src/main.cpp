#include "Config.h"
#include "PID.h"
#include "Actuators.h"
#include "MissionState.h"
#include "MissionWebServer.h"

unsigned long lastLoopTime = 0;
unsigned long lastLogTime = 0;
const int LED_PIN = LED_BUILTIN;

// Function prototypes
void checkLiftoff();
void checkGNCActivation();
void checkPyroTrigger();
void checkLanding();

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("=== Polaris Payload System ===");

  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  initWebServer();
  // Ensure ground state on startup
  transitionToState(GROUND);
}

void loop() {

  unsigned long currentTime = millis();

  handleWebServer();

  // Consistent 100Hz loop for state management and control
  // Non-blocking
  if (currentTime >= lastLoopTime + LOOP_PERIOD) {
    unsigned long deltaMs = currentTime - lastLoopTime;
    lastLoopTime = currentTime;
    float deltaT = deltaMs / 1000.0; 

    // State machine
    switch(currentState) {
      case GROUND:
      // Wait for ARM command via web or serial
        if (Serial.available() > 0) {
          String command = Serial.readStringUntil('\n');
          command.trim();
          if (command.equalsIgnoreCase("ARM")) {
            transitionToState(ARMED);
          }
        }
        break;

      case ARMED:
        // Wait for LAUNCH command via web or serial
        if (Serial.available() > 0) {
          String command = Serial.readStringUntil('\n');
          command.trim();
          if (command.equalsIgnoreCase("LAUNCH")) {
            transitionToState(ASCENT);
          } else if (command.equalsIgnoreCase("ABORT")) {
            transitionToState(GROUND);
          }
        }
        break;

      case ASCENT:
        if (currentTime - stateStartTime >= 10000) {
          transitionToState(GNC_ACTIVE);
        }
        // checkGNCActivation();
        break;

      case GNC_ACTIVE:
        if (currentTime - gncStartTime >= 15000) {
          transitionToState(PYRO_FIRED);
        }
        // checkPyroTrigger();
        break;

      case PYRO_FIRED:
        if (currentTime - stateStartTime >= 5000) {
          transitionToState(LANDED);
        }
        // checkLanding();
        break;

      case LANDED:
        break;
    }
  }
}

void checkLiftoff() {
  // Based on altitude and acceleration thresholds 
}

void checkGNCActivation() {
  // Based on altitude and time thresholds
}

void checkPyroTrigger() {
  // Based on altitude and time thresholds
}

void checkLanding() {
  // Based on altitude and acceleration thresholds
}