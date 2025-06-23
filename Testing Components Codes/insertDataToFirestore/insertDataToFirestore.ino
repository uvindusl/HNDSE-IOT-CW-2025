#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>

const char* ssid = "DiniRed";
const char* password = "123456789";

// Your Firebase project info
const char* host = "firestore.googleapis.com";
const char* apiKey = "AIzaSyDoWdEbBC0NaQP6yR7M_0QsJvjxjcRisbA";
const char* projectId = "inclass-f6c41";
const char* collection = "test";

// Your Auth Token (from Firebase Authentication)
String idToken = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjNiZjA1MzkxMzk2OTEzYTc4ZWM4MGY0MjcwMzM4NjM2NDA2MTBhZGMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vaW5jbGFzcy1mNmM0MSIsImF1ZCI6ImluY2xhc3MtZjZjNDEiLCJhdXRoX3RpbWUiOjE3NTA2NTg1ODAsInVzZXJfaWQiOiJvQ0VFNjVkb3praHJtbXVqMml4VGNQa3ZRenoxIiwic3ViIjoib0NFRTY1ZG96a2hybW11ajJpeFRjUGt2UXp6MSIsImlhdCI6MTc1MDY1ODU4MCwiZXhwIjoxNzUwNjYyMTgwLCJlbWFpbCI6Im1rZGdhbmdhZGFyYUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsibWtkZ2FuZ2FkYXJhQGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.qR4XMjH0QvQ7ruLisKz7AzUoXg9hg8gOYPWAAA2N1Bo6V_WXFnTgwmKIwKeFQ9SRpaQsL8esxFCBjkmSktZ2acSl9qef-mI-0P8uAzKv31y5NN4JV2d29Cxa-XULMHdcEtnkcevrkYcOfOs47UKtD9yLmF33Q660DAe3Ld1fJMlIvHxRmbafPJoFUtHzP45XOHnziCyvfwOxTqm2J6uMS7aF3w24VwTdYmP3S8OZ3mHLd4CF4uAdnxUf0DxcRuuIMq2a9yR4CX-JD_6JScGDmyOP8vIh_eWHwE6Q3zBL6KIn-lplvHFSGq78hyINEU7CKoyFMt1kGR24IuIzlgwycQ"; 

WiFiClientSecure client;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  // Wait for WiFi
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");

  // Allow insecure connections (for test)
  client.setInsecure();

  // Construct the document path
  String url = "/v1/projects/" + String(projectId) + "/databases/(default)/documents/" + String(collection);

  // Create JSON payload
  String payload = R"(
    {
      "fields": {
        "temperature": { "doubleValue": 2599.6 },
        "ane_pancho": { "doubleValue": 200000.00 }
      }
    }
  )";

  // Start HTTP request
  if (client.connect(host, 443)) {
    client.println("POST " + url + " HTTP/1.1");
    client.println("Host: " + String(host));
    client.println("Authorization: Bearer " + idToken);
    client.println("Content-Type: application/json");
    client.print("Content-Length: ");
    client.println(payload.length());
    client.println();
    client.println(payload);
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

void loop() {
  // Nothing here
}
