import time
import RPi.GPIO as GPIO

# Pins, IN1 - forward, IN2 - backward, BUTTON - start/stop, SERVO - servo control
# BUTTON = 
# IN1 = 
# IN2 = 
# SERVO = 
        
# GPIO setup
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(IN1, GPIO.OUT)
# GPIO.setup(IN2, GPIO.OUT)
# GPIO.setup(BUTTON, GPIO.IN)
# GPIO.setup(SERVO, GPIO.OUT)

# LED setup
S0 = 17
S1 = 27
S2 = 22
S3 = 23
OUT = 24
LED = 18

GPIO.setup([S0, S1, S2, S3, LED], GPIO.OUT)
GPIO.setup(OUT, GPIO.IN)
        
# Servo setup here later

# TCS3200 Setup
S0 = 17
S1 = 27
S2 = 22
S3 = 23
OUT = 24
LED = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup([S0, S1, S2, S3, LED], GPIO.OUT)
GPIO.setup(OUT, GPIO.IN)

# Set frequency scaling to 100%
GPIO.output(S0, GPIO.HIGH)
GPIO.output(S1, GPIO.HIGH)
GPIO.output(LED, GPIO.HIGH)

def set_filter(s2, s3):
    GPIO.output(S2, s2)
    GPIO.output(S3, s3)

def read_frequency():
    pulses = 10
    start = time.time()
    for _ in range(pulses):
        GPIO.wait_for_edge(OUT, GPIO.FALLING)
    duration = time.time() - start
    return pulses / duration if duration > 0 else 0

def read_colors():
    # Red
    set_filter(GPIO.LOW, GPIO.LOW)
    time.sleep(0.1)
    red = read_frequency()

    # Green
    set_filter(GPIO.HIGH, GPIO.HIGH)
    time.sleep(0.1)
    green = read_frequency()

    # Blue
    set_filter(GPIO.LOW, GPIO.HIGH)
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

except KeyboardInterrupt:
    GPIO.cleanup()