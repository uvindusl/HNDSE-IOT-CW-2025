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
String idToken = "eyJhbGciOiJSUzI1NiIsImtpZCI6Ijg3NzQ4NTAwMmYwNWJlMDI2N2VmNDU5ZjViNTEzNTMzYjVjNThjMTIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vaW5jbGFzcy1mNmM0MSIsImF1ZCI6ImluY2xhc3MtZjZjNDEiLCJhdXRoX3RpbWUiOjE3NTE2MTg1NjcsInVzZXJfaWQiOiJvQ0VFNjVkb3praHJtbXVqMml4VGNQa3ZRenoxIiwic3ViIjoib0NFRTY1ZG96a2hybW11ajJpeFRjUGt2UXp6MSIsImlhdCI6MTc1MTYxODU2NywiZXhwIjoxNzUxNjIyMTY3LCJlbWFpbCI6Im1rZGdhbmdhZGFyYUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsibWtkZ2FuZ2FkYXJhQGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.ycMcpEi__UWZxOqoHA3LqRG_NZRbl4sNUDGnLrpJbAWmudkcpbUSSVoCN89wVBzPfTjidbWFHNueDfpPEwf-VwYj7r0BLSevj4ETWqlK6wS6m0dR8JhxexkaAO6gBySv7NrY31R0ils5p4_Wf_glGGM9J7Om7aXCcRM4d1QjJ7bjUG162mpxgV_05BnQUiSdoHHuf06gJMNxXOMakb9_-vntv4CaUkCBUwMRSIPYpZ9UOfUeIkTvPLvjqnoMMk8I-D6FHi8ofKZw7q1k8h8IN__BTepBgufbo51Cd0GUrRKgRJxwpVfyHLuoLgzk_-uKC1bW4nEoFA3gTUrXspYskw"; 

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
