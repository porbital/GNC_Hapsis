#include "PID.h"

PIDController::PIDController(float kp, float kd, float ki) 
  : kp(kp), kd(kd), ki(ki), setpoint(0.0), 
    lastError(0.0), lastDerivative(0.0), lastOutput(0.0), integral(0.0) {
}

void PIDController::setGains(float kp, float kd, float ki) {
  this->kp = kp;
  this->kd = kd;
  this->ki = ki;
}

void PIDController::setSetpoint(float setpoint) {
  this->setpoint = setpoint;
}

float PIDController::wrapAngle(float angle) {
  // Wrap angle to -180 to +180 range
  while (angle > 180.0) {
    angle -= 360.0;
  } 
  while (angle < -180.0) {
    angle += 360.0;
  } 
  return angle;
}

float PIDController::compute(float currentValue, float deltaTime) {
  // Calculate error with wraparound handling
  float error = wrapAngle(setpoint - currentValue);
  
  // Calculate derivative
  float derivative = 0.0;
  if (deltaTime > 0.0) {
    derivative = (error - lastError) / deltaTime;
  }
  
  // Calculate integral 
  integral += error * deltaTime;
  // Anti-windup (double check this)
  integral = constrain(integral, -100.0, 100.0);  // Anti-windup
  
  // Calculate output
  float output = (kp * error) + (kd * derivative) + (ki * integral);
  
  // Store for next iteration and logging
  lastError = error;
  lastDerivative = derivative;
  lastOutput = output;
  
  return output;
}

void PIDController::reset() {
  lastError = 0.0;
  lastDerivative = 0.0;
  lastOutput = 0.0;
  integral = 0.0;
}