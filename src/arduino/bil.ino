#include <Wire.h>
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
#define SLAVE_ADDRESS 0x04



int number = 0;
int state = 0;
int mapped_number = 0;
Servo ESCServo;
Servo ESCMotor;

void setup() {


  Serial.begin(9600);

  // initialize i2c as slave
  Wire.begin(SLAVE_ADDRESS);

  
  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);

  ESCMotor.attach(MOTOR_PIN);
  ESCServo.attach(SERVO_PIN);
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
      mapped_number = map(number, 0,127,950,1300);
      ESCMotor.writeMicroseconds(mapped_number);
      Serial.print("Motor control: ");
      Serial.println(mapped_number);
    } else {
      mapped_number = map(number, 128,255,1000,2000);
      ESCServo.write(mapped_number);
      Serial.print("Steering control: ");
      Serial.println(mapped_number);
    }
  }
}

// callback for sending data
void sendData() {
  Wire.write(number);
}

