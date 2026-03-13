#ifndef LOGGING_H
#define LOGGING_H

#include <Arduino.h>
#include "Config.h"
#include <SPI.h>
#include <SdFat.h>
#include "MissionState.h"

#define CS_PIN 10
#define SCK_PIN 13
#define MISO_PIN 12
#define MOSI_PIN 11

// Initialize SD card and file for logging
void initLogging();

// Log data to SD card
void logData(
    unsigned long timestamp,
    float temperature, float pressure, float altitude,
    float roll, float pitch, float heading, float vertical_accel,
    bool leftThruster, bool rightThruster,
    MissionState state
);

#endif