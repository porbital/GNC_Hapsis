#include "Sensors.h"
#include "Wire.h"

Adafruit_BMP3XX bmp;
// Adafruit_BNO055 bno = Adafruit_BNO055();
#if defined(ARDUINO_TEENSY41) && defined(USE_WIRE2)
Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28, &Wire2);
#else
Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28, &Wire);
#endif

float baseAlt; // Base altitude for relative measurements

void initSensors()
{
#if defined(ARDUINO_ARCH_RP2040)
    Wire.setSDA(I2C_SDA_PIN);
    Wire.setSCL(I2C_SCL_PIN);
#endif
    Wire.begin();
    Wire.setClock(100000); // 100 kHz for BNO055 clock stretching
    delay(500); 
    Serial.println("Waiting for sensors to initialize...");

    Serial.printf("Scanning I2C0 (SDA=GP%d, SCL=GP%d)...\n", I2C_SDA_PIN, I2C_SCL_PIN);
    int nDevices = 0;
    for (uint8_t addr = 1; addr < 127; addr++) {
        Wire.beginTransmission(addr);
        if (Wire.endTransmission() == 0) {
            Serial.printf("  Found I2C device on I2C0 at 0x%02X\n", addr);
            nDevices++;
        }
    }
    if (nDevices == 0) {
        Serial.println("  No devices on I2C0 (GP4/GP5).");
    }

    // Also scan I2C1 on GP6 and GP7 in case user connected to GPIO 6 and 7
    Wire1.setSDA(6);
    Wire1.setSCL(7);
    Wire1.begin();
    Wire1.setClock(100000);
    Serial.println("Scanning I2C1 (SDA=GP6, SCL=GP7)...");
    int nDevices1 = 0;
    for (uint8_t addr = 1; addr < 127; addr++) {
        Wire1.beginTransmission(addr);
        if (Wire1.endTransmission() == 0) {
            Serial.printf("  Found I2C device on I2C1 at 0x%02X\n", addr);
            nDevices1++;
        }
    }
    if (nDevices1 == 0) {
        Serial.println("  No devices on I2C1 (GP6/GP7).");
    }
    // Initialize barometer
    // if (!bmp.begin_I2C(0x28))
    // {
    //     Serial.println("Could not find a valid BMP3XX sensor, check wiring!");
    //     while (1)
    //         ;
    // }
    delay(500); 
    Serial.println("Waiting for sensors to initialize...");

    // Initialize IMU (Address 0x28 or 0x29)
    bool imuConnected = false;
    while (!imuConnected)
    {
        if (bno.begin()) {
            imuConnected = true;
            Serial.println(">>> BNO055 successfully initialized! <<<");
            break;
        }

        Serial.println("No BNO055 detected! Retrying in 2 seconds...");
        Serial.printf("Checking I2C0 (GP%d/GP%d) and I2C1 (GP6/GP7):\n", I2C_SDA_PIN, I2C_SCL_PIN);
        
        int found = 0;
        for (uint8_t addr = 1; addr < 127; addr++) {
            Wire.beginTransmission(addr);
            if (Wire.endTransmission() == 0) {
                Serial.printf("  [I2C0] Found device at 0x%02X\n", addr);
                found++;
            }
        }
        for (uint8_t addr = 1; addr < 127; addr++) {
            Wire1.beginTransmission(addr);
            if (Wire1.endTransmission() == 0) {
                Serial.printf("  [I2C1] Found device at 0x%02X\n", addr);
                found++;
            }
        }
        if (found == 0) {
            Serial.println("  No I2C devices responded on any tested pins.");
        }
        delay(2000);
    }

    delay(500); 
    Serial.println("Waiting for sensors to initialize...");

    // bmp.setTemperatureOversampling(BMP3_OVERSAMPLING_8X);
    // bmp.setPressureOversampling(BMP3_OVERSAMPLING_4X);
    // bmp.setIIRFilterCoeff(BMP3_IIR_FILTER_COEFF_3);
    // bmp.setOutputDataRate(BMP3_ODR_50_HZ);

    // bmp.performReading();
    // bmp.performReading();
    // bmp.performReading();
    // baseAlt = bmp.readAltitude(SEALEVELPRESSURE_HPA);

    bno.setExtCrystalUse(true); // Better accuracy

    Serial.println("Sensors initialized");

}

// void readBarometer(float &temperature, float &pressure, float &altitude)
// {
// #ifdef HIL_MODE
//     static float lastAltitude = 0.0;
//    if (Serial.available() > 0)
//     {
//         String line = Serial.readStringUntil('\n');
//         line.trim();
        
//         // 1. Check that the string actually has data after "ALT:"
//         if (line.startsWith("ALT:") && line.length() > 4)
//         {
//             float parsedAlt = line.substring(4).toFloat();
            
//             // Rate Limiter
//             if (lastAltitude == 0.0 || abs(parsedAlt - lastAltitude) < 10.0)
//             {
//                 lastAltitude = parsedAlt;
//             }
//         }
//     }
//     altitude = lastAltitude;
//     temperature = 20.0;
//     pressure = 1013.25;
// #else
//     if (bmp.performReading())
//     {
//         temperature = bmp.temperature;
//         pressure = bmp.pressure;
//         altitude = bmp.readAltitude(SEALEVELPRESSURE_HPA) - baseAlt; // Relative altitude
//     }
//     else
//     {
//         Serial.println("Failed to perform reading from BMP3XX");
//     }
// #endif
// }

void readIMU(float &roll, float &pitch, float &heading, float &vertical_accel)
{
    sensors_event_t event;
    bno.getEvent(&event);

    // Also read linear acceleration for GNC activation check
    imu::Vector<3> accel = bno.getVector(Adafruit_BNO055::VECTOR_LINEARACCEL);

    vertical_accel = accel.z();  // remove "float" to avoid shadowing

    roll = event.orientation.y;
    pitch = event.orientation.z;
    heading = event.orientation.x;
}
