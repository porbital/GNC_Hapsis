#include "Sensors.h"

Adafruit_BMP3XX bmp;
Adafruit_BNO055 bno = Adafruit_BNO055();

float baseAlt; // Base altitude for relative measurements

void initSensors()
{
    Wire.begin();
    delay(500); 
    Serial.println("Waiting for sensors to initialize...");
    // Initialize barometer
    if (!bmp.begin_I2C(0x77))
    {
        Serial.println("Could not find a valid BMP3XX sensor, check wiring!");
        while (1)
            ;
    }
    delay(500); 
    Serial.println("Waiting for sensors to initialize...");

    // Initialize IMU
    if (!bno.begin())
    {
        Serial.println("No BNO055 detected, check wiring!");
        while (1)
            ;
    }

    delay(500); 
    Serial.println("Waiting for sensors to initialize...");

    bmp.setTemperatureOversampling(BMP3_OVERSAMPLING_8X);
    bmp.setPressureOversampling(BMP3_OVERSAMPLING_4X);
    bmp.setIIRFilterCoeff(BMP3_IIR_FILTER_COEFF_3);
    bmp.setOutputDataRate(BMP3_ODR_50_HZ);

    bmp.performReading();
    bmp.performReading();
    bmp.performReading();
    baseAlt = bmp.readAltitude(SEALEVELPRESSURE_HPA);

    bno.setExtCrystalUse(true); // Better accuracy

    Serial.println("Sensors initialized");

}

void readBarometer(float &temperature, float &pressure, float &altitude)
{
#ifdef HIL_MODE
    static float lastAltitude = 0.0;
   if (Serial.available() > 0)
    {
        String line = Serial.readStringUntil('\n');
        line.trim();
        
        // 1. Check that the string actually has data after "ALT:"
        if (line.startsWith("ALT:") && line.length() > 4)
        {
            float parsedAlt = line.substring(4).toFloat();
            
            // Rate Limiter
            if (lastAltitude == 0.0 || abs(parsedAlt - lastAltitude) < 10.0)
            {
                lastAltitude = parsedAlt;
            }
        }
    }
    altitude = lastAltitude;
    temperature = 20.0;
    pressure = 1013.25;
#else
    if (bmp.performReading())
    {
        temperature = bmp.temperature;
        pressure = bmp.pressure;
        altitude = bmp.readAltitude(SEALEVELPRESSURE_HPA) - baseAlt; // Relative altitude
    }
    else
    {
        Serial.println("Failed to perform reading from BMP3XX");
    }
#endif
}

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
