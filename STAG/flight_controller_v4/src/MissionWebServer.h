// MissionWebServer.h - Simple web interface
#ifndef MISSION_WEB_SERVER_H
#define MISSION_WEB_SERVER_H

#include <Arduino.h>

#if defined(ARDUINO_ARCH_ESP32)
#include <WiFi.h>
#include <WebServer.h>

// Initialize WiFi AP and web server
void initWebServer();

// Handle web server requests (call in loop)
void handleWebServer();

void setWebAltitude(float alt);
void setWebVerticalVelocity(float vvel);

#else
// Non-ESP32 targets (e.g. STM32) do not have on-board WiFi web server
inline void initWebServer() {}
inline void handleWebServer() {}
inline void setWebAltitude(float) {}
inline void setWebVerticalVelocity(float) {}
#endif

#endif // MISSION_WEB_SERVER_H