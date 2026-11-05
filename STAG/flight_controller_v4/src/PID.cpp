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

float PIDController::windupCap(float integral) { 
  // compute final integral term - prevent windup
  if (integral > I_MAX) {
    integral = I_MAX;
  } else if (integral < -1 * I_MAX) {
    integral = -1 * I_MAX;
  }
  return integral;
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
  if (deltaTime > 0.0) {
    integral += (error * deltaTime); // ZOH error approximation
    integral = windupCap(integral);
  }

  // Calculate output PD Control
  float output = (kp * error) + (ki * integral) + (kd * derivative);
  
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