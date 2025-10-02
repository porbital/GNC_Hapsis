#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <math.h>

#define PI (3.14159265358979)

// SDA to A4
// SCL to A5
// bno055 setup

Adafruit_BNO055 bno = Adafruit_BNO055(55);

void setup(void) 
{
  Serial.begin(9600);
  Serial.println("Orientation Sensor Test"); Serial.println("");
  
  /* Initialize the sensor */
  if(!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }
  
  delay(1000);
    
  bno.setExtCrystalUse(true);


}

double kP = 10;
double kI = 0;
double kD = 1.6248;
double inte = 0;

double setpoint = 0;
double dt = .01;
double integral_clipping = 3; // max integral value

void loop(void) 
{
  /* Get a new sensor event */ 
  sensors_event_t orientationData; 
  sensors_event_t angVelocityData;
  bno.getEvent(&orientationData, Adafruit_BNO055::VECTOR_EULER);
  bno.getEvent(&angVelocityData, Adafruit_BNO055::VECTOR_GYROSCOPE);
  
  // rotational position in rad
  // angular velocity in rad/s

  double x = 0;
  double vx = 0;

  x = orientationData.orientation.x;
  x = x * (PI / 180.0);
  vx = angVelocityData.gyro.x;

  Serial.print("x:");
  Serial.print(x);
  Serial.print(",");
  Serial.print("vx:");
  Serial.print(vx);

  
  double wrapped_x = fmod(x - setpoint, 2 * PI);
  if (wrapped_x > PI) {
    wrapped_x -= 2*PI;
  }
  else if (wrapped_x < -PI) {
    wrapped_x += 2*PI;
  }

  inte += wrapped_x * dt;

  // arb clipping
  
  inte = constrain(inte, -integral_clipping, integral_clipping);
  double out_torque = kP * wrapped_x + kI * inte + kD * vx;
  Serial.print(",");
  Serial.print("PID torque:");
  Serial.println(out_torque);
  
  

  delay(100);
}