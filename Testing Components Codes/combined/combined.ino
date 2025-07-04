#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"
#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClientSecure.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <SoftwareSerial.h>
#include <TinyGPS++.h>
#include <string.h>

#define RX D3
#define TX D4

#define GPS_BAUD 9600

TinyGPSPlus gps;
SoftwareSerial gpsSerial(RX, TX);


Adafruit_MPU6050 mpu;

MAX30105 particleSensor;

const byte RATE_SIZE = 6;
byte rates[RATE_SIZE];
byte rateSpot = 0;
long lastBeat = 0;

float beatsPerMinute;
int simpleAvgBPM;

float maxacc = 0;
float minacc = 0;
const int activeBuzzerPin = D7;

const char* ssid = "DiniRed";
const char* password = "123456789";

const char* firebaseApiKey = "AIzaSyDoWdEbBC0NaQP6yR7M_0QsJvjxjcRisbA";
const char* signInEndpoint = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=";

const char* userEmail = "mkdgangadara@gmail.com";
const char* userPassword = "password123";
// below are the credentials of firestore database.
const char* host = "firestore.googleapis.com";
const char* apiKey = "AIzaSyDoWdEbBC0NaQP6yR7M_0QsJvjxjcRisbA";
const char* projectId = "inclass-f6c41";
const char* collection = "test";

//this is the firebase auth id key that can be used across the code
char AIDcharArray[4000];

void setup() {
  // put your setup code here, to run once:
  pinMode(activeBuzzerPin, OUTPUT);
  Serial.begin(115200);
  Serial.println("Initializing MAX30102 heart rate sensor");

  if(!particleSensor.begin(Wire, I2C_SPEED_FAST)){
    Serial.println("MAX30102 was not found. please check wiring. halting");
    beep(100); delay(100);
    beep(100); delay(300); // Slight pause
    beep(100); delay(100);
    beep(100); delay(500);
    while (1);

  }
  Serial.println("Sensor initialized. Place your forhead");


  particleSensor.setup();
  particleSensor.setPulseAmplitudeRed(0x0A);
  particleSensor.setPulseAmplitudeGreen(0);

  Serial.println("Adafruit MPU6050 test");

  if(!mpu.begin()){
    Serial.println("Sensor init failed");
    beep(100); delay(100);
    beep(100); delay(300); // Slight pause
    beep(100); delay(100);
    beep(100); delay(500);
    beep(100); delay(500);
    beep(100); delay(500);
    while(1){
      yield();
    }
  }
  Serial.println("MPU6050 found");

  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);

  mpu.setGyroRange(MPU6050_RANGE_500_DEG);

  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  gpsSerial.begin(GPS_BAUD);

  
  beep(50); delay(50); // Beep, then short pause
  beep(50); delay(50);
  beep(50); delay(50);
  beep(150); delay(300); 

  connectToWIFI();
  sendRequestToFirebase();



}

void loop() {
  // put your main code here, to run repeatedly:
  checkHeartBeat();
  //getGPS();

}
void checkHeartBeat(){
  int i = 0;
  while(i < 10000){
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

  if (irValue < 9000){
    Serial.print("No finger/ Bad conact ?");
    simpleAvgBPM = 0;
    beatsPerMinute = 0;
    beatsPerMinute = 0;
    
  }
  Serial.println();
  i++;
  }
  
}
void accelo(){
  int i = 0;
  while(i < 40000){
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  
  if(a.acceleration.y > maxacc){
    maxacc = a.acceleration.y;
  }else{

  }
  if(a.acceleration.y < minacc){
    minacc = a.acceleration.y;
  }else{

  }

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
  delay(50); // Adjust delay as needed
  i++;
  }

}


void beep(int duration) {
  digitalWrite(activeBuzzerPin, HIGH); // Turn buzzer ON
  delay(duration);                     // Keep it on for 'duration' milliseconds
  digitalWrite(activeBuzzerPin, LOW);  // Turn buzzer OFF
}
void getGPS(){
  unsigned long start = millis();
  Serial.println("Before starting Software Serial started at 9600 baud rate");

  while (millis() - start < 1000) {
    while (gpsSerial.available() > 0) {
      gps.encode(gpsSerial.read());
    }
    if (gps.location.isUpdated()) {
      Serial.print("LAT: ");
      Serial.println(gps.location.lat(), 6);
      Serial.print("LONG: "); 
      Serial.println(gps.location.lng(), 6);
      Serial.print("SPEED (km/h) = "); 
      Serial.println(gps.speed.kmph()); 
      Serial.print("ALT (min)= "); 
      Serial.println(gps.altitude.meters());
      Serial.print("HDOP = "); 
      Serial.println(gps.hdop.value() / 100.0); 
      Serial.print("Satellites = "); 
      Serial.println(gps.satellites.value()); 
      Serial.print("Time in UTC: ");
      Serial.println(String(gps.date.year()) + "/" + String(gps.date.month()) + "/" + String(gps.date.day()) + "," + String(gps.time.hour()) + ":" + String(gps.time.minute()) + ":" + String(gps.time.second()));
      Serial.println("");
    }else{
      //Serial.println("no data recieved");
    }
  }
}
void connectToWIFI(){
  Serial.print("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}
void sendRequestToFirebase(){
  if (WiFi.status() == WL_CONNECTED) {
    // Construct the full URL including the API key
    String fullUrl = String(signInEndpoint) + String(firebaseApiKey);

    HTTPClient http;

    WiFiClientSecure client; 
    client.setInsecure();    
                             
    http.begin(client, fullUrl);


    
    http.addHeader("Content-Type", "application/json");

    
    StaticJsonDocument<200> doc; 
    doc["email"] = userEmail;
    doc["password"] = userPassword;
    doc["returnSecureToken"] = true;

    String requestBody;
    serializeJson(doc, requestBody); // Convert JSON object to a string

    Serial.println("\n--- Sending Firebase Sign-in Request ---");
    Serial.println("Target URL: " + fullUrl);
    Serial.println("Request Body: " + requestBody);

    // Send the POST request
    int httpResponseCode = http.POST(requestBody);

    if (httpResponseCode > 0) {
      //Serial.print("HTTP Response code: ");
      //Serial.println(httpResponseCode);
      String response = http.getString(); // Get the response payload (JSON containing token/user info)
      //Serial.println("Response from server:");
      Serial.println(response);

      
      StaticJsonDocument<500> responseDoc; // Adjust size if response is larger
      DeserializationError error = deserializeJson(responseDoc, response);

      if (error) {
        Serial.print(F("deserializeJson() failed: "));
        Serial.println(error.f_str());
        return;
      }

      const char* idToken = responseDoc["idToken"];
      size_t len = strlen(idToken);
      
      strcpy(AIDcharArray, idToken); 
      
      //below codes were used for testing purposes and commented because they arent doing any task in this code
      //const char* refreshToken = responseDoc["refreshToken"];
      //const char* expiresIn = responseDoc["expiresIn"]; 

      if (idToken) {
        Serial.println("idToken: " + String(idToken));
        //Serial.println("refreshToken: " + String(refreshToken));
        //Serial.println("expiresIn (seconds): " + String(expiresIn));
      } else {
        Serial.println("Failed to get idToken from response (check credentials/Firebase rules)");
      }


    } else {
      Serial.print("Error sending POST request. Error code: ");
      Serial.println(httpResponseCode);
      Serial.println(http.errorToString(httpResponseCode));
    }

    http.end(); // Close the connection
  } else {
    Serial.println("WiFi not connected. Attempting to reconnect...");
    WiFi.begin(ssid, password);
  }
  Serial.print("Converted id = ");
  Serial.println(AIDcharArray);
  delay(1000);
  
}
void sendAccidentData(){

}
