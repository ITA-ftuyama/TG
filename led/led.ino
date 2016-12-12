int incomingByte = 0;
int ledPin = 11;
 
void setup(){
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
}
 
void loop(){
  // Send data
  // incomingByte += 1;
  // Serial.println(incomingByte);
  // delay(1000);

  // Read data
  incomingByte = Serial.read();
 
  if(incomingByte == 'H') {
    digitalWrite(ledPin, HIGH);
  } else if(incomingByte == 'L') {
     digitalWrite(ledPin, LOW);
  }
  // analogWrite(ledPin, incomingByte);
  delay(100);
}
