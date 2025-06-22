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

def start():
    # Automatic driving function
    pass

def stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    pwm.changeDutyCycle(0)
    pass


GPIO.output(S0, GPIO.HIGH)
GPIO.output(S1, GPIO.HIGH)

GPIO.output(LED, GPIO.HIGH)

def set_color_filter(s2, s3):
    GPIO.output(S2, s2)
    GPIO.output(S3, s3)

def read_frequency():
    start = time.time()
    pulses = 10
    for _ in range(pulses):
        GPIO.wait_for_edge(OUT, GPIO.FALLING)
    duration = time.time() - start
    if duration == 0:
        return 0
    return pulses / duration

def read_colors():
    # Red
    set_color_filter(GPIO.LOW, GPIO.LOW)
    time.sleep(0.1)
    red = read_frequency()

    # Green
    set_color_filter(GPIO.HIGH, GPIO.HIGH)
    time.sleep(0.1)
    green = read_frequency()

    # Blue
    set_color_filter(GPIO.LOW, GPIO.HIGH)
    time.sleep(0.1)
    blue = read_frequency()

    return red, green, blue

def detect_color(red, green, blue):
    print(f"R: {red:.2f}  G: {green:.2f}  B: {blue:.2f}")

    if red < green and red < blue:
        return "Red"
    elif green < red and green < blue:
        return "Green"
    elif blue < red and blue < green:
        return "Blue"
    else:
        return "Unknown"

try:
    while True:
        red, green, blue = read_colors()
        color = detect_color(red, green, blue)
        print(f"Detected Color: {color}")
        time.sleep(1)

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