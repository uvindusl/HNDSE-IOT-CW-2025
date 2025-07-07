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
#include <Arduino.h>




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


// below are the credentials of firestore database.
int bstate = 1;
//this is the firebase auth id key that can be used across the code
char AIDcharArray[3200];

WiFiClientSecure client;

const char* serverUrl = "https://nodemcuimg-88924602304.europe-west1.run.app";
const char* serverhost = "192.168.178.42";
const int httpsPort = 8080;
const char* path = "/nodemcu";

float lat;
float longt;
float speed;
String date;
String actime;

void setup() {
  // put your setup code here, to run once:
  pinMode(activeBuzzerPin, OUTPUT);
  pinMode(D5, INPUT_PULLUP);
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
  client.setInsecure();
  connectToWIFI();
  beep(50); delay(50);
  beep(150); delay(300); 
  sendRequestToFirebase();
  




}

void loop() {
  // put your main code here, to run repeatedly:
  
  accelo();
  if(maxacc > 5.00){
    Serial.println("Accident");
    Serial.println("max acc = ");
    Serial.println(maxacc);
    
    for(int z = 0; z < 10; z++){
      bstate = digitalRead(D5);
      if(bstate == LOW){
        break;
      }else{
        beep(200); delay(100);
        beep(200); delay(100);
        beep(200); delay(500);
      }
    }
    if(bstate == HIGH){
      getGPS();
      delay(100);
      sendAccidentData();
      
      while(true){
        checkHeartBeat();
        sendHB(simpleAvgBPM);
        bstate = digitalRead(D5);
        if(bstate == LOW){
          beep(200); delay(100);
          beep(200); delay(100);
          beep(200); delay(500);
          break;
        }

      }
      
      
    }

  }
  
  maxacc = 0;
  minacc = 0;

  delay(1000);

}

void checkHeartBeat(){
  int i = 0;
  while(i < 1200){
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
  while(i < 40){
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
  delay(150); // Adjust delay as needed
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
      lat = gps.location.lat();
      Serial.print("LONG: "); 
      Serial.println(gps.location.lng(), 6);
      longt = gps.location.lng();
      Serial.print("SPEED (km/h) = "); 
      Serial.println(gps.speed.kmph());
      speed = gps.speed.kmph(); 
      Serial.print("ALT (min)= "); 
      Serial.println(gps.altitude.meters());
      Serial.print("HDOP = "); 
      Serial.println(gps.hdop.value() / 100.0); 
      Serial.print("Satellites = "); 
      Serial.println(gps.satellites.value()); 
      Serial.print("Time in UTC: ");
      Serial.println(String(gps.date.year()) + "/" + String(gps.date.month()) + "/" + String(gps.date.day()) + "," + String(gps.time.hour()) + ":" + String(gps.time.minute()) + ":" + String(gps.time.second()));
      date = String(gps.date.year()) + "/" + String(gps.date.month()) + "/" + String(gps.date.day());
      actime = String(gps.time.hour()) + "/" + String(gps.time.minute());

      Serial.println("");
      Serial.println("these are the converted values");
      Serial.println(date);
      Serial.println(actime);
      Serial.println(speed);
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
  Serial.print("String key = ");
  Serial.println(String(AIDcharArray));
  delay(1000);
  
}
void sendAccidentData(){
  String url = "/v1/projects/" + String(projectId) + "/databases/(default)/documents/" + String(collection);
  StaticJsonDocument<512> doc;
  JsonObject fields = doc.createNestedObject("fields");

  fields["h_id"]["stringValue"] = "h0222";
  fields["lat"]["doubleValue"] = lat;
  fields["long"]["doubleValue"] = longt;
  fields["date"]["stringValue"] = date;
  fields["time"]["stringValue"] = actime;
  fields["last_speed"]["doubleValue"] = speed;
  fields["deaccel_rate"]["doubleValue"] = maxacc;
  fields["last_accel"]["doubleValue"] = maxacc;
  fields["last_angle"]["doubleValue"] = 90;
  fields["status"]["doubleValue"] = 1;

  String requestBody;
  serializeJson(doc, requestBody);

  Serial.print("Generated Firestore JSON: ");
  Serial.println(requestBody);

  

  
  if (client.connect(host, 443)) {
    client.println("POST " + url + " HTTP/1.1");
    client.println("Host: " + String(host));
    client.println("Authorization: Bearer " + String(AIDcharArray));
    client.println("Content-Type: application/json");
    client.print("Content-Length: ");
    client.println(requestBody.length());
    client.println();
    client.println(requestBody);
  } else {
    Serial.println("Connection failed");
    return;
  }

  // Read response
  while (client.connected()) {
    String line = client.readStringUntil('\n');
    Serial.println(line);
    if (line == "\r") break;
  }

  String response = client.readString();
  Serial.println("Response: " + response);
}

void sendHB(int hb){
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client; // Use WiFiClient for HTTP (unencrypted)
    HTTPClient http;   // Declare an object of class HTTPClient

    // Construct the full URL
    String serverUrl = "https://" + String(serverhost) + ":" + String(httpsPort) + String(path);
    String jsonPayload = "{\"hid\":\"h0222\",\"heartbeat\":" + String(hb) + "}";

    Serial.print("[HTTP] begin... ");
    Serial.println(serverUrl);

    // Begin HTTP connection
    http.begin(client, serverUrl); // Specify the URL and connect

    // Set HTTP header for content type
    http.addHeader("Content-Type", "application/json");

    Serial.print("[HTTP] POSTing JSON... ");
    Serial.println(jsonPayload);

    // Send the POST request with the JSON payload
    int httpResponseCode = http.POST(jsonPayload);

    // httpResponseCode will be negative on error
    if (httpResponseCode > 0) {
      Serial.print("[HTTP] POST request successful, HTTP response code: ");
      Serial.println(httpResponseCode);

      // Get the response payload
      String responsePayload = http.getString();
      Serial.print("Response payload: ");
      Serial.println(responsePayload);
    } else {
      Serial.print("[HTTP] POST request failed, error: ");
      Serial.println(httpResponseCode);
      Serial.println(http.errorToString(httpResponseCode).c_str());
    }

    http.end(); // Free resources
  } else {
    Serial.println("WiFi Disconnected. Reconnecting...");
    WiFi.begin(ssid, password); // Try to reconnect
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }
    Serial.println("\nWiFi Reconnected.");
  }

  
  delay(5000);
}



