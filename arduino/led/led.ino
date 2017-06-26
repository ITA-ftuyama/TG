int incomingByte = 0;
int ledPin = 13;
String inString;
int number;
 
void setup(){
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  analogWrite(ledPin, 0);
}

void send_numbers(){
  // Send data
  // incomingByte += 1;
  // Serial.println(incomingByte);
  // delay(1000);
}
 
void loop(){

    // Read data
    int inChar = Serial.read();
    if (isDigit(inChar)) {
      inString += (char)inChar;
    } else if (inChar == 'x') {
      analogWrite(ledPin, 0);
    } else if (inChar == '\n') {
      int number = inString.toInt();
      number = number / 10;
      analogWrite(ledPin, number);
      inString = "";
    }

    delay(10);
}
