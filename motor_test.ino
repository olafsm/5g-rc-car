#include <Servo.h>


// Rotary Encoder Inputs
#define CLK 4
#define DT 3
#define SW 2

Servo ESC;     // create servo object to control the ESC
Servo myservo;  // create servo object to control a servo

int potValue;  // value from the analog pin


int counter = 950;
int currentStateCLK;
int lastStateCLK;
String currentDir ="";
unsigned long lastButtonPress = 0;

int potpin = 0;  // analog pin used to connect the potentiometer
int val;    // variable to read the value from the analog pin

void setup() {
  
  // Set encoder pins as inputs
  pinMode(CLK,INPUT);
  pinMode(DT,INPUT);
  pinMode(SW, INPUT_PULLUP);

  // Setup Serial Monitor
  Serial.begin(9600);

  // Read the initial state of CLK
  lastStateCLK = digitalRead(CLK);

  // Attach the ESC on pin 9
  ESC.attach(9); // (pin, min pulse width, max pulse width in microseconds)
  ESC.write(90);

    myservo.attach(8);  // attaches the servo on pin 9 to the servo object

}

void loop() {

  val = analogRead(potpin);            // reads the value of the potentiometer (value between 0 and 1023)
  val = map(val, 0, 1023, 0, 180);     // scale it to use it with the servo (value between 0 and 180)
  myservo.write(val);                  // sets the servo position according to the scaled value
  
  // Read the current state of CLK
  currentStateCLK = digitalRead(CLK);

  // If last and current state of CLK are different, then pulse occurred
  // React to only 1 state change to avoid double count
  if (currentStateCLK != lastStateCLK  && currentStateCLK == 1){

    // If the DT state is different than the CLK state then
    // the encoder is rotating CCW so decrement
    if (digitalRead(DT) != currentStateCLK) {
      if (counter != 950){
        counter = counter -10;
      }
      currentDir ="CCW";
    } else {
      // Encoder is rotating CW so increment
      if (counter != 2500) {
        counter = counter+10;
      }
      currentDir ="CW";
    }

    Serial.print("Direction: ");
    Serial.print(currentDir);
    Serial.print(" | Counter: ");
    Serial.println(counter);
    ESC.writeMicroseconds(counter);
  }


  

  // Remember last CLK state
  lastStateCLK = currentStateCLK;

  // Read the button state
  int btnState = digitalRead(SW);



  // Put in a slight delay to help debounce the reading
  //delay(1);

  //potValue = 10;   // reads the value of the potentiometer (value between 0 and 1023)
  //potValue = map(potValue, 0, 100, 0, 180);   // scale it to use it with the servo library (value between 0 and 180)
      // Send the signal to the ESC
}
