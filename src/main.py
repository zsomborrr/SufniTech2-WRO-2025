import time
import RPi.GPIO as GPIO
import keyboard

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
        
# Servo setup here later
    pass

# TCS3200 setup
S0 = 17
S1 = 27
S2 = 22
S3 = 23
OUT = 24
LED = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup([S0, S1, S2, S3, LED], GPIO.OUT)
GPIO.setup(OUT, GPIO.IN)

GPIO.output(S0, GPIO.HIGH)
GPIO.output(S1, GPIO.HIGH)
GPIO.output(LED, GPIO.HIGH)

def set_filter(s2, s3):
    GPIO.output(S2, s2)
    GPIO.output(S3, s3)

def read_frequency():
    pulses = 10
    start = time.time()
    count = 0
    for _ in range(pulses):
        result = GPIO.wait_for_edge(OUT, GPIO.FALLING, timeout=1000)
        if result is None:
            print("Timeout waiting for pulse.")
            break
        count += 1
    duration = time.time() - start
    return count / duration if duration > 0 else 0

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

def detect_color(r, g, b):
    print(f"R: {r:.2f} G: {g:.2f} B: {b:.2f}")
    if r < g and r < b:
        return "Red"
    elif g < r and g < b:
        return "Green"
    elif b < r and b < g:
        return "Blue"
    else:
        return "Unknown"

print("Press 'q' to quit.")

try:
    while True:
        if keyboard.is_pressed('q'):
            print("Exit key pressed. Stopping...")
            break

        r, g, b = read_colors()
        color = detect_color(r, g, b)
        print(f"Detected Color: {color}")
        time.sleep(1)

finally:
    GPIO.cleanup()