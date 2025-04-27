import time
import RPi.GPIO as GPIO

# Pins, IN1 - forward, IN2 - backward, BUTTON - start/stop, SERVO - servo control
BUTTON = 17
IN1 = 27
IN2 = 22
SERVO = 5
        
# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(BUTTON, GPIO.IN)
GPIO.setup(SERVO, GPIO.OUT)
        
# Servo setup here later
pwm = GPIO.PWM(SERVO, 50) 
p.start(0)

def start():
    # Automatic driving function
    pass

def stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    pwm.changeDutyCycle(0)
    pass

# Button setup
try:
    while True:
       if GPIO.input(BUTTON) == GPIO.HIGH:
           start()
           while GPIO.input(BUTTON) == GPIO.HIGH:  
               time.sleep(0.1)
       else:
           stop()
       time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()