// MissionWebServer.h - Simple web interface
#ifndef MISSION_WEB_SERVER_H
#define MISSION_WEB_SERVER_H

#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>

// Initialize WiFi AP and web server
void initWebServer();

// Handle web server requests (call in loop)
void handleWebServer();

void setWebAltitude(float alt);
void setWebVerticalVelocity(float vvel);

#endif // MISSION_WEB_SERVER_H