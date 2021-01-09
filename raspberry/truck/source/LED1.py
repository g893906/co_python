import RPi.GPIO as GPIO
 
LED_PIN = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
 
try:
    print('按下 Ctrl-C 可停止程式')
    GPIO.output(LED_PIN, GPIO.LOW)
    while True:
        next
except KeyboardInterrupt:
    print('關閉程式')
finally:
    GPIO.cleanup()
