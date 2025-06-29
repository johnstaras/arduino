import RPi.GPIO as GPIO

def pulse_detected(channel):
    print("Pulse detected!")

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(17, GPIO.FALLING, callback=pulse_detected, bouncetime=10)

print("OK. Waiting...")
try:
    while True:
        pass
except KeyboardInterrupt:
    GPIO.cleanup()
