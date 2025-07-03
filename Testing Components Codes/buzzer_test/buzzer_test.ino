const int activeBuzzerPin = D2; // Connect your active buzzer to D1 (or your chosen pin)

void setup() {
  pinMode(activeBuzzerPin, OUTPUT); // Set the buzzer pin as an output
}

void loop() {
  // --- Melody Pattern 1: Short, Sharp Beeps ---
  beep(50); delay(50); // Beep, then short pause
  beep(50); delay(50);
  beep(50); delay(50);
  beep(150); delay(300); // Longer beep, longer pause

  // --- Melody Pattern 2: Call-and-Response type ---
  beep(100); delay(100);
  beep(100); delay(300); // Slight pause
  beep(100); delay(100);
  beep(100); delay(500); // Longer pause

  // --- Melody Pattern 3: Warning / Alert style ---
  beep(200); delay(100);
  beep(200); delay(100);
  beep(200); delay(500); // Pause before next cycle

  // --- Long pause before repeating the whole sequence ---
  delay(2000);
}

// Helper function to make the code cleaner and easier to read
void beep(int duration) {
  digitalWrite(activeBuzzerPin, HIGH); // Turn buzzer ON
  delay(duration);                     // Keep it on for 'duration' milliseconds
  digitalWrite(activeBuzzerPin, LOW);  // Turn buzzer OFF
}