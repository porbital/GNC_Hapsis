#ifndef PID_CONTROLLER_H
#define PID_CONTROLLER_H

#include <Arduino.h>
#include "Config.h"

class PIDController {
public:
  PIDController(float kp, float kd, float ki);
  
  // Set PID gains
  void setGains(float kp, float kd, float ki);
  
  // Set setpoint (desired heading)
  void setSetpoint(float setpoint);
  
  // Compute PID output
  float compute(float currentValue, float deltaTime);
  
  // Reset PID state
  void reset();
  
  // Get last error and derivative 
  float getLastError() { return lastError; }
  float getLastDerivative() { return lastDerivative; }
  float getLastOutput() { return lastOutput; }
  
private:
  float kp, kd, ki;
  float setpoint;
  float lastError;
  float lastDerivative;
  float lastOutput;
  float integral;
  
  // Wrap angle error to -180 to +180
  float wrapAngle(float angle);
};

#endif // PID_CONTROLLER_H