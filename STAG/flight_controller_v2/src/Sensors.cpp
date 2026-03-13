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
}

void readIMU(float &roll, float &pitch, float &heading, float &vertical_accel)
{
    sensors_event_t event;
    bno.getEvent(&event);

    // Also read linear acceleration for GNC activation check
    imu::Vector<3> accel = bno.getVector(Adafruit_BNO055::VECTOR_LINEARACCEL);

    vertical_accel = accel.z();  // remove "float" to avoid shadowing

    roll = event.orientation.x;
    pitch = event.orientation.y;
    heading = event.orientation.z;
}
