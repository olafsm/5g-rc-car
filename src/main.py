import RPi.GPIO as GPIO
from time import sleep

# Dutycycle, 5 = -90 left, 7.5 = 0 neutral, 10 = +90 right
def setAngle(angle):
    duty = angle / 18 + 3
    GPIO.output(servoPIN, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(servoPIN, False)
    pwm.ChangeDutyCycle(duty)

servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

pwm = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
pwm.start(0) # Initialization
try:
  while True:
      setAngle(0)
      sleep(1)
      setAngle(45)
      sleep(1) 
      setAngle(90)
      sleep(1)
      setAngle(135)
      sleep(1)
      setAngle(180)
    
except KeyboardInterrupt:
  pwm.stop()
  GPIO.cleanup()

