import time
import pigpio

LED_PIN = 26

gpio = pigpio.pi()
gpio.set_mode(LED_PIN, pigpio.OUTPUT)
gpio.set_pull_up_down(LED_PIN, pigpio.PUD_UP)
while(True):
    gpio.write(LED_PIN, pigpio.HIGH)
    print("Pin 26 is: " + str(gpio.read(LED_PIN)))
    time.sleep(1)
    gpio.write(LED_PIN, pigpio.LOW)
    print("Pin 26 is: " + str(gpio.read(LED_PIN)))
    time.sleep(1)