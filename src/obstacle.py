import RPi.GPIO as GPIO
import time

# === GPIO Setup ===
TRIG = 19
ECHO = 26
SWITCH_PIN = 16
SERVO_PIN = 18
IN3 = 7
IN4 = 8

# === Constants ===
LEFT_DUTY = 8.5
RIGHT_DUTY = 1.5
CENTER_DUTY = 5.5
SERVO_FREQ = 50
DIST_THRESHOLD = 10

# === Initialize GPIO ===
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output(TRIG, False)

GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

GPIO.setup(SERVO_PIN, GPIO.OUT)
servo = GPIO.PWM(SERVO_PIN, SERVO_FREQ)
servo.start(0)

# === Helper Functions ===
def is_switch_on():
    return GPIO.input(SWITCH_PIN) == GPIO.LOW

def measure_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start = time.time()
    timeout = start + 0.05
    while GPIO.input(ECHO) == 0 and time.time() < timeout:
        start = time.time()

    timeout = start + 0.05
    while GPIO.input(ECHO) == 1 and time.time() < timeout:
        stop = time.time()

    duration = stop - start
    distance = duration * 17000
    return distance

def steer_and_drive(duty, duration, reverse=False):
    # Set steering angle
    servo.ChangeDutyCycle(duty)
    time.sleep(0.2)  # Give the servo time to reach position
    servo.ChangeDutyCycle(0)  # Stop sending signal to avoid jitter

    # Drive in chosen direction
    if reverse:
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
        print(f"Reversing for {duration}s with duty {duty}")
    else:
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
        print(f"Forward for {duration}s with duty {duty}")

    time.sleep(duration)

    # Stop after movement
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    print("Stopped")

# === Main ===
try:
    print("Waiting for switch...")
    already_done = False

    while True:
        if is_switch_on() and not already_done:
            distance = measure_distance()
            print(f"Side distance: {distance:.1f} cm")

            if distance > DIST_THRESHOLD:
                print("➡️ Executing LEFT-sequence")
                steer_and_drive(LEFT_DUTY, 0.32)
                steer_and_drive(RIGHT_DUTY, 0.5, reverse=True)
                steer_and_drive(LEFT_DUTY, 0.35)
                steer_and_drive(RIGHT_DUTY, 0.4, reverse=True)
            else:
                print("⬅️ Executing RIGHT-sequence")
                steer_and_drive(RIGHT_DUTY, 0.25)
                steer_and_drive(LEFT_DUTY, 0.37, reverse=True)
                steer_and_drive(RIGHT_DUTY, 0.35)
                steer_and_drive(LEFT_DUTY, 0.35, reverse=True)
                steer_and_drive(RIGHT_DUTY, 0.2)

            # === Reset servo to center before driving forward ===
            print("🔄 Centering servo before driving straight")
            servo.ChangeDutyCycle(CENTER_DUTY)
            time.sleep(0.3)
            servo.ChangeDutyCycle(0)

            # === Start driving straight forward ===
            GPIO.output(IN3, GPIO.HIGH)
            GPIO.output(IN4, GPIO.LOW)
            print("⬆️ Driving straight forward")

            already_done = True

        elif not is_switch_on():
            already_done = False

        time.sleep(0.1)

except KeyboardInterrupt:
    print("🛑 Interrupted")
finally:
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    servo.ChangeDutyCycle(CENTER_DUTY)
    time.sleep(0.3)
    servo.stop()
    GPIO.cleanup()
    print("✅ Shutdown complete")
