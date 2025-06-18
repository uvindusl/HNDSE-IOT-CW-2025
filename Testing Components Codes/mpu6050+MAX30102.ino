#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"

#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_MPU6050 mpu;

MAX30105 particleSensor;

const byte RATE_SIZE = 6;
byte rates[RATE_SIZE];
byte rateSpot = 0;
long lastBeat = 0;

float beatsPerMinute;
int simpleAvgBPM;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println("Initializing MAX30102 heart rate sensor");

  if(!particleSensor.begin(Wire, I2C_SPEED_FAST)){
    Serial.println("MAX30102 was not found. please check wiring. halting");
    while (1);

  }
  Serial.println("Sensor initialized. Place your index finger on it");


  particleSensor.setup();
  particleSensor.setPulseAmplitudeRed(0x0A);
  particleSensor.setPulseAmplitudeGreen(0);

  Serial.println("Adafruit MPU6050 test");

  if(!mpu.begin()){
    Serial.println("Sensor init failed");
    while(1){
      yield();
    }
  }
  Serial.println("MPU6050 found");

  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);

  mpu.setGyroRange(MPU6050_RANGE_500_DEG);

  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);






}

void loop() {
  // put your main code here, to run repeatedly:
  checkHeartBeat();
  delay(20);

  accelo();
  delay(30);

}

void checkHeartBeat(){
  int i = 0;
  while(i < 1000){
    long irValue = particleSensor.getIR();

  if(checkForBeat(irValue) == true){
    long delta = millis() - lastBeat;
    lastBeat = millis();

    beatsPerMinute = 60 / (delta / 1000.0);

    if(beatsPerMinute < 200 && beatsPerMinute > 40){
      rates[rateSpot++] = (byte)beatsPerMinute;
      rateSpot %= RATE_SIZE;

      simpleAvgBPM = 0;
      for(byte x = 0; x < RATE_SIZE; x++){
        simpleAvgBPM += rates[x];
      }
      simpleAvgBPM /= RATE_SIZE;

      
    }
  }
  Serial.print("IR=");
  Serial.print(irValue);
  Serial.print("| BPM=");
  Serial.print(beatsPerMinute);
  Serial.print("| Simple Avg BPM=");
  Serial.print(simpleAvgBPM);

  if (irValue < 5000){
    Serial.print("No finger/ Bad conact ?");
    simpleAvgBPM = 0;
    beatsPerMinute = 0;
    
  }
  Serial.println();
  i++;
  }
  
}
void accelo(){
  int i = 0;
  while(i < 1000){
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  /* Print out the values */
  Serial.print("Acceleration X: ");
  Serial.print(a.acceleration.x);
  Serial.print(" m/s^2, Y: ");
  Serial.print(a.acceleration.y);
  Serial.print(" m/s^2, Z: ");
  Serial.print(a.acceleration.z);
  Serial.println(" m/s^2");

  Serial.print("Rotation X: ");
  Serial.print(g.gyro.x);
  Serial.print(" rad/s, Y: ");
  Serial.print(g.gyro.y);
  Serial.print(" rad/s, Z: ");
  Serial.print(g.gyro.z);
  Serial.println(" rad/s");

  Serial.print("Temperature: ");
  Serial.print(temp.temperature);
  Serial.println(" C");

  Serial.println("");
  delay(100); // Adjust delay as needed
  i++;
  }

}
