import RPi.GPIO as GPIO
import time
from datetime import datetime

# -----------------------------
# Configuration
# -----------------------------
HALL_SENSOR_PIN = 17  # GPIO17 (pin 11)
CIRCUMFERENCE = 0.5   # meters (wheel circumference)
LOG_DATA = False      # Set to True to log speed data
LOG_FILE = "bike_speed_log.csv"
MEASUREMENT_INTERVAL = 1  # seconds

# -----------------------------
# GPIO Setup
# -----------------------------
GPIO.setmode(GPIO.BCM)
GPIO.setup(HALL_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# -----------------------------
# Logging Setup
# -----------------------------
if LOG_DATA:
    with open(LOG_FILE, 'w') as f:
        f.write("timestamp,speed_mps,speed_kph\n")

# -----------------------------
# Main Loop
# -----------------------------
try:
    print("Starting speedometer... Press Ctrl+C to stop.")
    last_state = GPIO.input(HALL_SENSOR_PIN)

    while True:
        pulse_count = 0
        start_time = time.time()

        while (time.time() - start_time) < MEASUREMENT_INTERVAL:
            current_state = GPIO.input(HALL_SENSOR_PIN)
            if last_state == GPIO.HIGH and current_state == GPIO.LOW:
                pulse_count += 1
                time.sleep(0.01)  # basic debounce
            last_state = current_state
            time.sleep(0.001)

        elapsed_time = time.time() - start_time

        # Speed calculations
        revolutions = pulse_count
        distance_m = revolutions * CIRCUMFERENCE
        speed_mps = distance_m / elapsed_time
        speed_kph = speed_mps * 3.6

        print(f"Speed: {speed_mps:.2f} m/s | {speed_kph:.2f} km/h")

        if LOG_DATA:
            with open(LOG_FILE, 'a') as f:
                timestamp = datetime.now().isoformat()
                f.write(f"{timestamp},{speed_mps:.2f},{speed_kph:.2f}\n")

except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()
