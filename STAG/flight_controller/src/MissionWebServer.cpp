// MissionWebServer.cpp - Simple web server for mission control

/* Transparency: This document specifically is written largely with AI. It's just a simple html page */

#include <WiFi.h>
#include <WebServer.h>
#include "MissionWebServer.h"
#include "MissionState.h"

// Access Point credentials
const char* ap_ssid = "Hapsis_Avionics";
const char* ap_password = "orbital";

WebServer server(80);

const char* htmlPage = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Polaris GNC</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      text-align: center;
      margin-top: 30px;
      background: #f0f0f0;
    }
    .container {
      display: inline-block;
      background: white;
      padding: 30px;
      border-radius: 10px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.1);
      max-width: 500px;
    }
    h1 { color: #333; margin-bottom: 10px; }
    .button {
      padding: 12px 25px;
      font-size: 16px;
      margin: 8px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      transition: all 0.3s;
    }
    .arm    { background: #FF9800; color: white; }
    .arm:hover { background: #e68900; }
    .launch { background: #4CAF50; color: white; }
    .launch:hover:not(:disabled) { background: #45a049; }
    .launch:disabled { background: #aaa; cursor: not-allowed; }
    .abort  { background: #f44336; color: white; }
    .abort:hover { background: #da190b; }
    #status {
      margin-top: 20px;
      font-size: 24px;
      font-weight: bold;
      color: #333;
      padding: 15px;
      background: #e8f5e9;
      border-radius: 8px;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Hapsis Launch Dashboard</h1>
    <h2>Higher, Faster, Further</h2>
    <div id="status">State: LOADING</div>
    <br>
    <button class="button arm"    id="btnArm"    onclick="sendCommand('/ARM')">ARM</button>
    <button class="button launch" id="btnLaunch" onclick="sendCommand('/LAUNCH')" disabled>LAUNCH</button>
    <button class="button abort"  id="btnAbort"  onclick="sendCommand('/ABORT')">ABORT</button>
  </div>

  <script>
    function updateStatus() {
      fetch('/status')
        .then(r => r.text())
        .then(data => {
          document.getElementById('status').innerText = 'State: ' + data;
          // Only enable LAUNCH when in ARMED state
          document.getElementById('btnLaunch').disabled = (data !== 'ARMED');
          // Disable ARM button if already armed or beyond
          const preArm = (data === 'GROUND');
          document.getElementById('btnArm').disabled = !preArm;
        })
        .catch(err => console.error(err));
    }

    function sendCommand(path) {
      fetch(path)
        .then(r => r.text())
        .then(() => updateStatus())
        .catch(err => console.error(err));
    }

    updateStatus();
    setInterval(updateStatus, 1000);
  </script>
</body>
</html>
)rawliteral";

// --- Route handlers ---

void handleRoot() {
  server.send(200, "text/html", htmlPage);
}

void handleArm() {
  if (currentState == GROUND) {
    transitionToState(ARMED);
    server.send(200, "text/plain", "ARMED");
  } else {
    server.send(403, "text/plain", "NOT_GROUND");
  }
}

void handleLaunch() {
  if (currentState == ARMED) {
    transitionToState(ASCENT);
    server.send(200, "text/plain", "ASCENT");
  } else {
    server.send(403, "text/plain", "NOT_ARMED");
  }
}

void handleAbort() {
  transitionToState(GROUND);
  server.send(200, "text/plain", "GROUND");
}

void handleStatus() {
  server.send(200, "text/plain", stateToString(currentState));
}

void handleNotFound() {
  server.send(404, "text/plain", "Not found");
}

// --- Public functions ---

void initWebServer() {
  Serial.println("Setting up Access Point...");
  WiFi.softAP(ap_ssid, ap_password);

  IPAddress IP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(IP);

  server.on("/",       handleRoot);
  server.on("/ARM",    handleArm);
  server.on("/LAUNCH", handleLaunch);
  server.on("/ABORT",  handleAbort);
  server.on("/status", handleStatus);
  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("HTTP server started");
  Serial.println("Connect to WiFi: " + String(ap_ssid));
  Serial.println("Visit: http://" + IP.toString());
}

void handleWebServer() {
  server.handleClient();
}