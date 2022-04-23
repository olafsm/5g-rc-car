#include <Servo.h>

#define SERVO_PIN 9
#define MOTOR_PIN 8
/*
    Raspberry pi & Arduino PINOUTS
    http://christianto.tjahyadi.com/wp-content/uploads/2014/11/nano.jpg
    https://www.the-diy-life.com/wp-content/uploads/2021/05/Raspberry-Pi-4-Pinout.png
    SDA: GPIO2 -> A4
    SCL: GPIO3 -> A5
*/
int number = 0;
int state = 0;
int mapped_number = 0;
Servo ESCServo;
Servo ESCMotor;

void setup() {

  pinMode(13 , OUTPUT);
  Serial.begin(115200);

  ESCMotor.attach(MOTOR_PIN);
  ESCServo.attach(SERVO_PIN);
  Serial.println("Ready!");
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    int number = data.toInt();
    digitalWrite(13, HIGH);
    if (number <= 127) {
      mapped_number = map(number, 0,127,950,1300);
      ESCMotor.writeMicroseconds(mapped_number);
      Serial.print("Motor control: ");
      Serial.println(mapped_number);
    } else {
      Serial.print("Steering control: ");
      Serial.println(number);
      mapped_number = map(number, 128,255,1000,2000);
      ESCServo.write(mapped_number);
    }
    digitalWrite(13, LOW);
  }
}
