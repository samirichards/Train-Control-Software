import time
import pigpio

LED_PIN = 37

gpio = pigpio.pi
gpio.set_mode(LED_PIN, pigpio.OUTPUT)
gpio.set_pull_up_down(LED_PIN, pigpio.PUD_UP)
while(True):
    gpio.write(LED_PIN, pigpio.HIGH)
    print("Pin 37 is: " + gpio.read(LED_PIN))
    time.sleep(1)
    gpio.write(LED_PIN, pigpio.LOW)
    print("Pin 37 is: " + gpio.read(LED_PIN))
    time.sleep(1)