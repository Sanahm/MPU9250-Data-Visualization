/* MPU9250 data acquisition
by:  Mohamed SANA 30/04/2017 adapted from Kris Winer code

 Demonstrate basic MPU-9250 functionality including parameterizing the register
 addresses, initializing the sensor, getting properly scaled accelerometer,
 gyroscope, and magnetometer data out.Sketch runs on the 3.3 V 8 MHz Pro Mini
 and the Teensy 3.1 and Mega.

 SDA and SCL should have external pull-up resistors (to 3.3V).
 10k resistors are on the EMSENSR-9250 breakout board.

 Hardware setup:
 MPU9250 Breakout --------- Arduino
 VDD ---------------------- 3.3V
 VDDI --------------------- 3.3V
 SDA ----------------------- A4
 SCL ----------------------- A5
 GND ---------------------- GND
 */

#include "quaternionFilters.h"
#include "MPU9250.h"
#include "wire.h"


#define SerialDebug true  // Set to true to get Serial output for debugging

// Pin definitions
//int intPin = 12;  // These can be changed, 2 and 3 are the Arduinos ext int pins
//int myLed  = 8;  // Set up pin 8 led for toggling

MPU9250 AGM; // Accelero Gyro Magneto

void setup()
{
  Wire.begin();
  // TWBR = 12;  // 400 kbit/sec I2C speed
  Serial.begin(19200);
  
  // Set up the interrupt pin, its set as active high, push-pull
  //pinMode(intPin, INPUT);
  //digitalWrite(intPin, LOW);
  //pinMode(myLed, OUTPUT);
  //digitalWrite(myLed, HIGH);

  // Read the WHO_AM_I register, this is a good test of communication
  byte c = AGM.readByte(MPU9250_ADDRESS, WHO_AM_I_MPU9250);
  /*Serial.print("MPU9250 "); Serial.print("I AM "); Serial.print(c, HEX);
  Serial.print(" I should be "); Serial.println(0x71, HEX);*/


  if (c == 0x73) // WHO_AM_I should always be 0x68
  {
    //Serial.println("MPU9250 is online...");

    // Start by performing self test and reporting values
    AGM.MPU9250SelfTest(AGM.SelfTest);

    // Calibrate gyro and accelerometers, load biases in bias registers
    AGM.calibrateMPU9250(AGM.gyroBias, AGM.accelBias);

    AGM.initMPU9250();
    // Initialize device for active mode read of acclerometer, gyroscope, and
    // temperature
    //Serial.println("MPU9250 initialized for active data mode....");

    // Read the WHO_AM_I register of the magnetometer, this is a good test of
    // communication
    byte d = AGM.readByte(AK8963_ADDRESS, WHO_AM_I_AK8963);
    //Serial.print("AK8963 "); Serial.print("I AM "); Serial.print(d, HEX);
    //Serial.print(" I should be "); Serial.println(0x48, HEX);


    // Get magnetometer calibration from AK8963 ROM
    AGM.initAK8963(AGM.magCalibration);
    // Initialize device for active mode read of magnetometer
    //Serial.println("AK8963 initialized for active data mode....");
    if (SerialDebug)
    {
      //  Serial.println("Calibration values: ");
    }
  } // if (c == 0x71)
  else
  {
    Serial.print("Could not connect to MPU9250: 0x");
    Serial.println(c, HEX);
    while(1) ; // Loop forever if communication doesn't happen
  }
}

void loop()
{
  // If intPin goes high, all data registers have new data
  // On interrupt, check if data ready interrupt
  if (AGM.readByte(MPU9250_ADDRESS, INT_STATUS) & 0x01)
  {  
    AGM.readAccelData(AGM.accelCount);  // Read the x/y/z adc values
    AGM.getAres();

    // Now we'll calculate the accleration value into actual g's
    // This depends on scale being set
    AGM.ax = (float)AGM.accelCount[0]*AGM.aRes; // - accelBias[0];
    AGM.ay = (float)AGM.accelCount[1]*AGM.aRes; // - accelBias[1];
    AGM.az = (float)AGM.accelCount[2]*AGM.aRes; // - accelBias[2];

    AGM.readGyroData(AGM.gyroCount);  // Read the x/y/z adc values
    AGM.getGres();

    // Calculate the gyro value into actual degrees per second
    // This depends on scale being set
    AGM.gx = (float)AGM.gyroCount[0]*AGM.gRes;
    AGM.gy = (float)AGM.gyroCount[1]*AGM.gRes;
    AGM.gz = (float)AGM.gyroCount[2]*AGM.gRes;

    AGM.readMagData(AGM.magCount);  // Read the x/y/z adc values
    AGM.getMres();
    // User environmental x-axis correction in milliGauss, should be
    // automatically calculated
    AGM.magbias[0] = +470.;
    // User environmental x-axis correction in milliGauss TODO axis??
    AGM.magbias[1] = +120.;
    // User environmental x-axis correction in milliGauss
    AGM.magbias[2] = +125.;

    // Calculate the magnetometer values in milliGauss
    // Include factory calibration per data sheet and user environmental
    // corrections
    // Get actual magnetometer value, this depends on scale being set
    AGM.mx = (float)AGM.magCount[0]*AGM.mRes*AGM.magCalibration[0] -
               AGM.magbias[0];
    AGM.my = (float)AGM.magCount[1]*AGM.mRes*AGM.magCalibration[1] -
               AGM.magbias[1];
    AGM.mz = (float)AGM.magCount[2]*AGM.mRes*AGM.magCalibration[2] -
               AGM.magbias[2];
  } // if (readByte(MPU9250_ADDRESS, INT_STATUS) & 0x01)

  // Must be called before updating quaternions!
  AGM.updateTime();

  digitalWrite(myLed, !digitalRead(myLed));  // toggle led
  AGM.delt_t = 600; //millis() - AGM.count;
  if (AGM.delt_t > 500)
  {
    if(SerialDebug)
    {
      // Print acceleration values in milligs!
  		Serial.print(1000*AGM.ax); Serial.print("\t");
  		Serial.print(1000*AGM.ay); Serial.print("\t");
  		Serial.print(1000*AGM.az); Serial.print("\t");
      /*Serial.print("X-acceleration: "); Serial.print(1000*AGM.ax);
      Serial.print(" mg ");
      Serial.print("Y-acceleration: "); Serial.print(1000*AGM.ay);
      Serial.print(" mg ");
      Serial.print("Z-acceleration: "); Serial.print(1000*AGM.az);
      Serial.println(" mg ");*/

      // Print gyro values in degree/sec
  		Serial.print(AGM.gx, 3); Serial.print("\t");
  		Serial.print(AGM.gy, 3); Serial.print("\t");
  		Serial.print(AGM.gz, 3); Serial.print("\t");
      /*Serial.print("X-gyro rate: "); Serial.print(AGM.gx, 3);
      Serial.print(" degrees/sec ");
      Serial.print("Y-gyro rate: "); Serial.print(AGM.gy, 3);
      Serial.print(" degrees/sec ");
      Serial.print("Z-gyro rate: "); Serial.print(AGM.gz, 3);
      Serial.println(" degrees/sec");*/

      // Print mag values in degree/sec
  		Serial.print(AGM.mx); Serial.print("\t");
  		Serial.print(AGM.my); Serial.print("\t");
  		Serial.print(AGM.mz); Serial.print("\n");
      /*Serial.print("X-mag field: "); Serial.print(AGM.mx);
      Serial.print(" mG ");
      Serial.print("Y-mag field: "); Serial.print(AGM.my);
      Serial.print(" mG ");
      Serial.print("Z-mag field: "); Serial.print(AGM.mz);
      Serial.println(" mG");

      AGM.tempCount = AGM.readTempData();  // Read the adc values
      // Temperature in degrees Centigrade
      AGM.temperature = ((float) AGM.tempCount) / 333.87 + 21.0;
      // Print temperature in degrees Centigrade
      Serial.print("Temperature is ");  Serial.print(AGM.temperature, 1);
      Serial.println(" degrees C");*/
    }

    //digitalWrite(myLed, !digitalRead(myLed));  // toggle led
  } 
}
