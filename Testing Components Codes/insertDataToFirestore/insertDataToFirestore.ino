#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>

const char* ssid = "DiniRed";
const char* password = "123456789";

// Your Firebase project info


// Your Auth Token (from Firebase Authentication)


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
