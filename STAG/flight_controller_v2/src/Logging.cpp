#include "Logging.h"

// SD card configuration
SdFat sd;
SdFile logFile;

void initLogging() {
  SPI.begin(SCK_PIN, MISO_PIN, MOSI_PIN, CS_PIN);
  SdSpiConfig config(CS_PIN, DEDICATED_SPI, SD_SCK_MHZ(4));

  if (!sd.begin(config)) {
    Serial.println("SD card initialization failed!");
    return;
  }

  // Find the next available filename
  char filename[32];
  int i = 1;
  do {
    snprintf(filename, sizeof(filename), "flight_log_%d.csv", i++);
  } while (sd.exists(filename));

  if (!logFile.open(filename, FILE_WRITE)) {
    Serial.println("Failed to open log file!");
    return;
  }

  Serial.print("Logging to: ");
  Serial.println(filename);


  // Write CSV header
  logFile.println("Timestamp,Temperature,Pressure,Altitude,Roll,Pitch,Heading,VerticalAccel,LeftThruster,RightThruster,MissionState");
  logFile.flush();
}

void logData(
    unsigned long timestamp,
    float temperature, float pressure, float altitude,
    float roll, float pitch, float heading, float vertical_accel,
    bool leftThruster, bool rightThruster,
    MissionState state
) {
  if (!logFile) {
    Serial.println("Log file not open!");
    return;
  }

  // Format data as CSV
  String logEntry = String(timestamp) + "," +
                    String(temperature) + "," +
                    String(pressure) + "," +
                    String(altitude) + "," +
                    String(roll) + "," +
                    String(pitch) + "," +
                    String(heading) + "," +
                    String(vertical_accel) + "," +
                    String(leftThruster ? "1" : "0") + "," +
                    String(rightThruster ? "1" : "0") + "," +
                    String(stateToString(state));
  Serial.print("Logging: ");
  Serial.println(logEntry); // Also print to Serial for real-time monitoring
  logFile.println(logEntry);
  logFile.flush();
}

