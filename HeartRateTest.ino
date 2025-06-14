#include <Wire.h>
#include "MAX30105.h" // Make sure this library is installed
#include "heartRate.h" // Make sure this library is installed

MAX30105 particleSensor;

// --- Configuration for improved accuracy ---
const byte RATE_SIZE = 8; // Increased for more averaging. Experiment with 8, 10, 16 for your needs.
byte rates[RATE_SIZE];    // Array of heart rates
byte rateSpot = 0;
long lastBeat = 0;        // Time at which the last beat occurred

float beatsPerMinute;
int simpleAvgBPM; // Renamed to differentiate from EMA
float emaAvgBPM = 0;      // Exponential Moving Average (EMA) for BPM
const float EMA_ALPHA = 0.1; // Smoothing factor for EMA.
                             // Smaller value (e.g., 0.05) = more smoothing, less responsive.
                             // Larger value (e.g., 0.2) = less smoothing, more responsive.
                             // Experiment to find the best balance.

void setup() {
  Serial.begin(115200);
  Serial.println("Initializing MAX30105 Heart Rate Sensor...");

  // Initialize sensor
  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println("MAX30102 was not found. Please check wiring/power. Halting.");
    while (1); // Halt if sensor not found
  }
  Serial.println("Sensor initialized. Place your index finger on the sensor with steady pressure.");
  Serial.println("Minimize ambient light for best results.");

  // Configure sensor with default settings
  particleSensor.setup();
  // Lower the red LED amplitude slightly to indicate sensor is running, but not too bright
  particleSensor.setPulseAmplitudeRed(0x0A);
  // Turn off Green LED as it's not typically used for simple HR measurement with this setup
  particleSensor.setPulseAmplitudeGreen(0);
}

void loop() {
  long irValue = particleSensor.getIR(); // Get the IR (Infrared) sensor reading

  // Check if a beat is detected
  if (checkForBeat(irValue) == true) {
    long delta = millis() - lastBeat; // Time since the last beat
    lastBeat = millis();              // Update last beat time

    // Calculate instantaneous Beats Per Minute (BPM)
    beatsPerMinute = 60 / (delta / 1000.0);

    // Filter out unrealistic BPM values (e.g., noise, very fast/slow movements)
    if (beatsPerMinute < 200 && beatsPerMinute > 40) { // Adjusted range for more realistic human HR
      // --- Simple Moving Average Calculation ---
      rates[rateSpot++] = (byte)beatsPerMinute; // Store this reading in the array
      rateSpot %= RATE_SIZE;                  // Wrap variable around array size

      simpleAvgBPM = 0; // Reset for new calculation
      for (byte x = 0; x < RATE_SIZE; x++) {
        simpleAvgBPM += rates[x]; // Sum all stored rates
      }
      simpleAvgBPM /= RATE_SIZE; // Calculate the average

      // --- Exponential Moving Average (EMA) Calculation ---
      if (emaAvgBPM == 0) { // Initialize EMA with the first valid BPM reading
        emaAvgBPM = beatsPerMinute;
      } else {
        // EMA formula: EMA_new = (ALPHA * current_value) + ((1 - ALPHA) * EMA_old)
        emaAvgBPM = (EMA_ALPHA * beatsPerMinute) + ((1 - EMA_ALPHA) * emaAvgBPM);
      }
    }
  }

  // --- Serial Output for monitoring ---
  Serial.print("IR=");
  Serial.print(irValue);
  Serial.print(", BPM=");
  Serial.print(beatsPerMinute);
  Serial.print(", Simple Avg BPM=");
  Serial.print(simpleAvgBPM); // Output the simple average
  Serial.print(", EMA Avg BPM=");
  Serial.print((int)emaAvgBPM); // Output the EMA (cast to int for cleaner display)

  // Provide feedback if no finger is detected (IR value too low)
  if (irValue < 5000) { // Adjusted threshold. You might need to calibrate this based on your sensor and setup.
    Serial.print(" No finger/Bad contact?");
    simpleAvgBPM = 0; // Reset averages when no finger to avoid stale readings
    emaAvgBPM = 0;
    // You might also want to clear 'rates' array here or reset 'rateSpot'
    // For simplicity, we'll just reset the averages that are displayed.
  }

  Serial.println();

  // A small delay can be added here if the serial output is too fast, but usually not needed.
  // delay(10);
}