#include "Config.h"
#include "PID.h"
#include "Actuators.h"
#include "Logging.h"
#include "Sensors.h"
#include "MissionState.h"
#include "MissionWebServer.h"

PIDController pid(PID_KP, PID_KD, PID_KI);


unsigned long lastLoopTime = 0;
unsigned long lastLogTime = 0;
const int LED_PIN = LED_BUILTIN;

// TEMPORARY: Thruster states for logging
bool leftThrusterOn = false;
bool rightThrusterOn = false;


// Function prototypes
void checkLiftoff();
void checkGNCActivation(float altitude, float acceleration);
void checkPyroTrigger();
void checkLanding();

void setup() {
  Serial.begin(115200);
  delay(5000);
  Serial.println("=== Hapsis Payload System ===");

  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  initSensors();
  initActuators();
  initLogging();

  initWebServer();


  pid.setSetpoint(HEADING);

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

    // Read sensor data
    float temperature, pressure, altitude;
    float roll, pitch, heading, vertical_accel;
    readBarometer(temperature, pressure, altitude);
    readIMU(roll, pitch, heading, vertical_accel);

    // Log data
    if (currentTime >= lastLogTime + LOG_PERIOD) {
      logData(currentTime, temperature, pressure,
         altitude, roll, pitch, heading, vertical_accel,
          leftThrusterOn, rightThrusterOn, currentState);
      lastLogTime = currentTime;
    }


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
        checkGNCActivation(altitude, vertical_accel);
        break;

      case GNC_ACTIVE:
        if (currentTime - gncStartTime >= 15000) {
          transitionToState(PYRO_FIRED);
        }
        // Start PID controller
        // float pidOutput = pid.compute(currentHeading, deltaT);
        // controlThrusters(pidOutput);

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

// If altitude > threshold and vertical acceleration > threshold, transition to GNC_ACTIVE
void checkGNCActivation(float altitude, float acceleration) {
  if (altitude > TARGET_ALTITUDE && acceleration > GNC_ACTIVATION_ACCEL) {
    transitionToState(GNC_ACTIVE);
    gncStartTime = millis();
  }
}

void checkPyroTrigger() {
  // Based on heading error and hold time
  // if (headingReached(currentHeading, HEADING)) {
  //   firePyros();
  //   transitionToState(PYRO_FIRED);
  // }
}

void checkLanding() {
  // Based on altitude and acceleration thresholds
}