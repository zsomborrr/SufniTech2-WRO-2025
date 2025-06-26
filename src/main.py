import RPi.GPIO as GPIO
import time

# GPIO Pins
TRIG_FRONT = 5
ECHO_FRONT = 6
TRIG_LEFT = 19
ECHO_LEFT = 26
IN3 = 7
IN4 = 8
SERVO_PIN = 18
SWITCH_PIN = 16

# Constants
BASE_DUTY = 4.75
RIGHT_TURN_DUTY = 1.5
LEFT_TURN_DUTY = 8.5
TURN_DURATION = 2.0
STEER_RESET_DELAY = 0.2
SERVO_FREQ = 50
MAX_DISTANCE = 300
LOOP_DELAY = 0.1

# Decision thresholds 
FRONT_OBSTACLE_THRESHOLD = 50
LEFT_CLEAR_THRESHOLD = 40

SLIGHT_LEFT_THRESHOLD = 30
SLIGHT_RIGHT_THRESHOLD = 15
SLIGHT_LEFT_DUTY = 7.0
SLIGHT_RIGHT_DUTY = 3.0
SLIGHT_TURN_DURATION = 0.3

# Setup 
GPIO.setmode(GPIO.BCM)
GPIO.setup([TRIG_FRONT, TRIG_LEFT], GPIO.OUT)
GPIO.setup([ECHO_FRONT, ECHO_LEFT], GPIO.IN)
GPIO.output(TRIG_FRONT, False)
GPIO.output(TRIG_LEFT, False)
GPIO.setup([IN3, IN4], GPIO.OUT)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

servo = GPIO.PWM(SERVO_PIN, SERVO_FREQ)
servo.start(BASE_DUTY)
time.sleep(0.3)
servo.ChangeDutyCycle(0)

# Control Functions 
def motor_forward():
  GPIO.output(IN3, GPIO.HIGH)
  GPIO.output(IN4, GPIO.LOW)

def motor_stop():
  GPIO.output(IN3, GPIO.LOW)
  GPIO.output(IN4, GPIO.LOW)

def steer(duty, duration):
  servo.ChangeDutyCycle(duty)
  time.sleep(duration)
  servo.ChangeDutyCycle(BASE_DUTY)
  time.sleep(STEER_RESET_DELAY)

def measure_distance(trig_pin, echo_pin):
  GPIO.output(trig_pin, True)
  time.sleep(0.00001)
  GPIO.output(trig_pin, False)

  start_time = time.time()
  timeout = start_time + 0.05
  while GPIO.input(echo_pin) == 0 and time.time() < timeout:
    start_time = time.time()
  if time.time() >= timeout:
    return None

  end_time = time.time()
  timeout = end_time + 0.05
  while GPIO.input(echo_pin) == 1 and time.time() < timeout:
    end_time = time.time()
  if time.time() >= timeout:
    return None

  duration = end_time - start_time
  distance = duration * 17000
  return distance if distance <= MAX_DISTANCE else None

def is_switch_on():
  return GPIO.input(SWITCH_PIN) == GPIO.LOW # LOW = switch ON

# Main Loop 
try:
  print("🟢 Ready. Toggle switch ON to start.")
  robot_active = False
  last_switch_state = is_switch_on()

  while True:
    switch_state = is_switch_on()
    if switch_state != last_switch_state:
      last_switch_state = switch_state
      robot_active = switch_state
      if robot_active:
        print("🔛 Switch ON — Robot active.")
        servo.ChangeDutyCycle(BASE_DUTY)
        time.sleep(0.3)
        servo.ChangeDutyCycle(0)
      else:
        print("🔘 Switch OFF — Robot stopped.")
        motor_stop()
        servo.ChangeDutyCycle(BASE_DUTY)
        time.sleep(0.3)
        servo.ChangeDutyCycle(0)

    if robot_active:
      dist_front = measure_distance(TRIG_FRONT, ECHO_FRONT)
      dist_left = measure_distance(TRIG_LEFT, ECHO_LEFT)

      front_str = f"{dist_front:.1f} cm" if dist_front else "--"
      left_str = f"{dist_left:.1f} cm" if dist_left else "--"
      print(f"📏 Front: {front_str} | Left: {left_str}")

      if dist_front and dist_front < FRONT_OBSTACLE_THRESHOLD:
        if dist_left and dist_left > LEFT_CLEAR_THRESHOLD:
          print("⬅️ Turning LEFT")
          steer(LEFT_TURN_DUTY, TURN_DURATION)
        else:
          print("➡️ Turning RIGHT")
          steer(RIGHT_TURN_DUTY, TURN_DURATION)
      else:
        motor_forward()
        if dist_left:
          if dist_left < SLIGHT_RIGHT_THRESHOLD:
            print("↘️ Slight RIGHT correction")
            steer(SLIGHT_RIGHT_DUTY, SLIGHT_TURN_DURATION)
          elif dist_left > SLIGHT_LEFT_THRESHOLD:
            print("↙️ Slight LEFT correction")
            steer(SLIGHT_LEFT_DUTY, SLIGHT_TURN_DURATION)
        else:
          print("⬆️ Moving FORWARD")

    else:
      print("🕹️ Waiting for switch ON...")
      time.sleep(0.5)

    time.sleep(LOOP_DELAY)

except KeyboardInterrupt:
  print("🛑 Stopping...")
  servo.ChangeDutyCycle(BASE_DUTY)
  time.sleep(0.3)
  servo.stop()
  motor_stop()
  GPIO.cleanup()
  print("✅ Shutdown complete.")
