#include <Wire.h>
#include <Servo.h>

#define SERVO_PIN 9
#define MOTOR_PIN 10
/*
    Raspberry pi & Arduino PINOUTS
    http://christianto.tjahyadi.com/wp-content/uploads/2014/11/nano.jpg
    https://www.the-diy-life.com/wp-content/uploads/2021/05/Raspberry-Pi-4-Pinout.png
    SDA: GPIO2 -> A4
    SCL: GPIO3 -> A5
*/
#define SLAVE_ADDRESS 0x04

#define CLK 4
#define DT 3
#define SW 2


int number = 0;
int state = 0;

Servo ESCServo;
Servo ESCMotor;

void setup() {

  lastStateCLK = digitalRead(CLK);

  pinMode(13, OUTPUT);
  Serial.begin(9600);

  // initialize i2c as slave
  Wire.begin(SLAVE_ADDRESS);

  
  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);

  ESCServo.attach(SERVO_PIN);
  ESCMotor.attach(MOTOR_PIN);
  
  Serial.println("Ready!");
}

void loop() {
  delay(100);
}

// callback for received data
void receiveData(int byteCount) {

  while (Wire.available()) {
    number = Wire.read();

    // 0-127 for motor control, 128-255 for servo steering
    if (number <= 127) {
      mapped_number = map(number, 0,127,950,1150)
      ESCMotor.writeMicroseconds(mapped_number);
      Serial.print("Motor control: ");
    } else {
      mapped_number = map(number(128,255,1000,2000)
      ESCServo.write(mapped_number);
      Serial.print("Steering control: ");
    }
      Serial.println(mapped_number)
  }
}

// callback for sending data
void sendData() {
  Wire.write(number);
}

