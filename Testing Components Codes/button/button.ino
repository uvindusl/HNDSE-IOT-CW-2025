void setup() {
  // put your setup code here, to run once:
  pinMode(D5, INPUT_PULLUP);
  pinMode(D2, OUTPUT);
  Serial.begin(115200);


}

void loop() {
  // put your main code here, to run repeatedly:
  int state = digitalRead(D5);

  if(state == LOW){
    Serial.println("Button pressed");
    
    
  }else{
    Serial.println("Button not pressed");
    
  }
  delay(100);

}
