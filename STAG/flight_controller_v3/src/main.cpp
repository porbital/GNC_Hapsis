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



// Function prototypes
void checkLiftoff();
void checkGNCActivation(float altitude, float acceleration);
void checkPyroTrigger();
void checkDescent(float altitude);
void checkLanding(float altitude, float vertical_vel);
float getVerticalVelocity(float altitude);

void setup() {
  Serial.begin(115200);
  delay(10000);
  Serial.println("=== Hapsis Payload System ===");

  initSensors();
  initActuators();
  initLogging();

  initWebServer();


  pid.setSetpoint(HEADING);

  // Ensure ground state on startup
  transitionToState(GROUND);
}

void loop() {

  handleWebServer();

  unsigned long currentTime = millis();

  // Consistent 100Hz loop for state management and control
  // Non-blocking
  if (currentTime >= lastLoopTime + LOOP_PERIOD) {
    unsigned long deltaMs = currentTime - lastLoopTime;
    lastLoopTime = currentTime;
    float deltaT = deltaMs / 1000.0; 

    // Read sensor data
    float temperature, pressure, altitude;
    float roll, pitch, heading, vertical_accel, vertical_vel;
    
    readBarometer(temperature, pressure, altitude);
    readIMU(roll, pitch, heading, vertical_accel);

    // Estimate vertical velocity
    vertical_vel = getVerticalVelocity(altitude);

    // Update web server data
    setWebAltitude(altitude);
    setWebVerticalVelocity(vertical_vel);

    // Log data
    if (currentTime >= lastLogTime + LOG_PERIOD) {
      logData(currentTime, temperature, pressure,
         altitude, roll, pitch, heading, vertical_accel, vertical_vel,
          getLeftThrusterState(), getRightThrusterState(), currentState);
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

        // If time since launch > MAX_ASCENT_TIME, turn on GNC as backup
        if (currentTime - stateStartTime >= ABORT_FIRE_PYRO_TIME) {
          gncStartTime = millis();
          transitionToState(GNC_ACTIVE);
        }

        checkGNCActivation(altitude, vertical_vel);
        break;

      case GNC_ACTIVE:
      {
        if (currentTime - gncStartTime >= GNC_TIME) { // Give GNC 30 seconds 
          disableAllActuators(); // Ensure thrusters are off
          transitionToState(PYRO_FIRED);
        }
        // Start PID controller
        float pidOutput = pid.compute(heading, deltaT);

        // Print PID output and heading, pitch, roll for debugging
        Serial.println("PID Output: " + String(pidOutput) + " | Heading: " + String(heading) + " | Pitch: " + String(pitch) + " | Roll: " + String(roll));
        controlThrusters(pidOutput);

        // checkPyroTrigger();
        break;
      }

      case PYRO_FIRED:
        if (firePyros(vertical_vel)) {
          // Pyro sequence completed successfully
          transitionToState(DESCENT);
        }
        break;
      case DESCENT:
         checkLanding(altitude, vertical_vel);
         break;
      case LANDED:
        break;
    }
  }
}
  


void checkLiftoff() {
  // Based on altitude and acceleration thresholds 
}

// If altitude > threshold and vertical velocity > threshold, transition to GNC_ACTIVE
void checkGNCActivation(float altitude, float verticalVelocity) {
  if (altitude > TARGET_ALTITUDE && verticalVelocity > GNC_ACTIVATION_VELOCITY) {
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

// If vertical velocity < threshold, transition to DESCENT
void checkDescent(float vertical_vel) {
  if (vertical_vel < DESCENT_VELOCITY_THRESHOLD)  {
    transitionToState(DESCENT);
  }

}

// If altitude < threshold and vertical velocity < threshold, transition to LANDED
// Slight bufffer on velocity to account for noise (velocity +- 0.5 m/s)
void checkLanding(float altitude, float vertical_vel) {
  if (altitude < ALTITUDE_LANDING_THRESHOLD && 
      abs(vertical_vel) < LANDING_VELOCITY_THRESHOLD) {
    transitionToState(LANDED);
  }
}

float getVerticalVelocity(float altitude) {
  // Implement a simple velocity estimator based on altitude changes
  static float lastAltitude = 0;
  static unsigned long lastTime = 0;
  static float filteredVelocity = 0;
  static bool firstRun = true;

  unsigned long currentTime = millis();

  if (lastTime > 0) {
    float deltaT = (currentTime - lastTime) / 1000.0; // Convert ms to seconds
    
    // Ensure deltaT is positive to avoid division by zero or negative velocity
    if (deltaT > 0) {
      float rawVelocity = (altitude - lastAltitude) / deltaT; // m/s
      
      // EMA Low Pass Filter with tau = 0.05
      float tau = 0.75;
      float alpha = deltaT / (tau + deltaT);
      
      if (firstRun) {
        filteredVelocity = rawVelocity;
        firstRun = false;
      } else {
        filteredVelocity = (alpha * rawVelocity) + ((1.0 - alpha) * filteredVelocity);
      }
    }
  }

  lastAltitude = altitude;
  lastTime = currentTime;

  return filteredVelocity;
}