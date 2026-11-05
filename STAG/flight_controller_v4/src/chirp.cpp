#include <Arduino.h>
#include <"Actuators.cpp">


void setup() {
  Serial.begin(115200);
  initActuators();
}

void initChirp() {
  static unsigned long startTime = micros();
  // Convert elapsed time from microseconds to seconds.
  for (int freq = 0; freq <= F_STOP; freq++) {
    float elapsedSeconds = static_cast<float>(micros() - startTime) / 1000000.0f;
    // Calculate the current angle of the sine wave.
    float phase = TWO_PI * MOTOR_FREQUENCY_HZ * elapsedSeconds;
    // Generate the sine-wave value from -1.0 to 1.0.
    float speed_setting = sin(phase) ;

    // Map the sine-wave value to the motor PWM range of 300 to 500.
    int pwmValue = static_cast<int>(speed * 0.5f) * 1.055  + 310);
    setMotorPwm(pwmValue);

  }

}
