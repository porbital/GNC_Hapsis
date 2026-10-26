#ifndef SENSORS_H
#define SENSORS_H

#include <Arduino.h>
#include "Config.h"
#include <Adafruit_Sensor.h>
#include "Adafruit_BMP3XX.h"
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

#define SEALEVELPRESSURE_HPA (1013.25)

extern float baseAlt; // Base altitude for relative measurements

// Initialize sensors
void initSensors();

// Read barometer data
void readBarometer(float &temperature, float &pressure, float &altitude);

// Read IMU data
void readIMU(float &roll, float &pitch, float &heading, float &vertical_accel);


#endif