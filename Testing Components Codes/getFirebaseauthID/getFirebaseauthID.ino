#include <ArduinoJson.h> // For easily creating JSON payload
#ifdef ESP8266
  #include <ESP8266WiFi.h>
  #include <ESP8266HTTPClient.h>
  #include <WiFiClientSecure.h> // For HTTPS on ESP8266
#else // ESP32
  #include <WiFi.h>
  #include <HTTPClient.h>
  // WiFiClientSecure is part of the WiFi.h for ESP32 and usually works implicitly
#endif


const char* ssid = "DiniRed";         // Replace with your WiFi SSID
const char* password = "123456789"; // Replace with your WiFi password


const char* firebaseApiKey = "AIzaSyDoWdEbBC0NaQP6yR7M_0QsJvjxjcRisbA"; // Replace with YOUR Firebase Web API Key


const char* signInEndpoint = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=";


const char* userEmail = "mkdgangadara@gmail.com"; // Replace with your Firebase test email
const char* userPassword = "password123";         // Replace with your Firebase test password

void setup() {
  Serial.begin(115200);
  delay(10);

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

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    // Construct the full URL including the API key
    String fullUrl = String(signInEndpoint) + String(firebaseApiKey);

    HTTPClient http;
#ifdef ESP8266
    WiFiClientSecure client; 
    client.setInsecure();    
                             
    http.begin(client, fullUrl);
#else // ESP32
    http.begin(fullUrl); 
#endif

    
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
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
      String response = http.getString(); // Get the response payload (JSON containing token/user info)
      Serial.println("Response from server:");
      Serial.println(response);

      
      StaticJsonDocument<500> responseDoc; // Adjust size if response is larger
      DeserializationError error = deserializeJson(responseDoc, response);

      if (error) {
        Serial.print(F("deserializeJson() failed: "));
        Serial.println(error.f_str());
        return;
      }

      const char* idToken = responseDoc["idToken"];
      const char* refreshToken = responseDoc["refreshToken"];
      const char* expiresIn = responseDoc["expiresIn"]; 

      if (idToken) {
        Serial.println("idToken: " + String(idToken));
        Serial.println("refreshToken: " + String(refreshToken));
        Serial.println("expiresIn (seconds): " + String(expiresIn));
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

  delay(100000); // Send request every 10 seconds
}