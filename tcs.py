import time
import pigpio
from enum import Enum
import atexit
import math
import random
from picamera import PiCamera

#Pin assignments
pin_pwm_IN1 = 13
pin_pwm_IN2 = 12
pwm_range = 255

class Direction(Enum):
    #A end = Non Motor End
    #B end = Motor End
    A = 0
    B = 1
#Setup defaults
CurrentDirection = Direction.A

gpio = pigpio.pi()

#Lower pwm frequencies at lower throttle values for a higher torque
#Higher pwm frequencies at higher throttle values for better efficiency
def GeneratePWMFrequency(throttle):
    return 5 / (20 * math.pi * throttle / 1000)

def setupPins():
    gpio.set_mode(pin_pwm_IN1, pigpio.OUTPUT)
    gpio.set_mode(pin_pwm_IN2, pigpio.OUTPUT)
    gpio.set_PWM_range(pin_pwm_IN2, pwm_range)
    gpio.set_PWM_range(pin_pwm_IN2, pwm_range)
    SetDirection(Direction.A)

#This function serves no real purpose, other than to make the motor resonate and produce a high pitched noise
def MakeNoise(duration):
    frequency = random.randrange(1000, 2000)
    print("Making a noise at " + str(frequency) + "Hz")
    gpio.set_PWM_frequency(pin_pwm_IN1, frequency)
    gpio.set_PWM_frequency(pin_pwm_IN2, 0)
    gpio.set_PWM_dutycycle(pin_pwm_IN1, 64)
    gpio.set_PWM_dutycycle(pin_pwm_IN2, 0)
    time.sleep(duration)
    gpio.set_PWM_dutycycle(pin_pwm_IN1, 0)
    gpio.set_PWM_dutycycle(pin_pwm_IN2, 0)
    return

def SetDirection(dir):
    global CurrentDirection
    CurrentDirection = dir
    return CurrentDirection

#Set motor throttle as a percentage of maximum possible speed given the current voltage
def SetThrottle(throttlePercent):
    if throttlePercent <= 0:
        gpio.set_PWM_dutycycle(pin_pwm_IN1, 0)
        gpio.set_PWM_dutycycle(pin_pwm_IN2, 0)
        return
    dutyCycle = int(throttlePercent * pwm_range)
    print("Direction = " + str(CurrentDirection.value))
    if CurrentDirection == Direction.A:
        gpio.set_PWM_frequency(pin_pwm_IN1, round(GeneratePWMFrequency(1.1-throttlePercent)))
        gpio.set_PWM_frequency(pin_pwm_IN2, 0)
        gpio.set_PWM_dutycycle(pin_pwm_IN1, dutyCycle)
        gpio.set_PWM_dutycycle(pin_pwm_IN2, 0)
    else:
        gpio.set_PWM_frequency(pin_pwm_IN1, 0)
        gpio.set_PWM_frequency(pin_pwm_IN2, round(GeneratePWMFrequency(1.1-throttlePercent)))
        gpio.set_PWM_dutycycle(pin_pwm_IN1, 0)
        gpio.set_PWM_dutycycle(pin_pwm_IN2, dutyCycle)
    print("    PWM frequency at " + str(round(GeneratePWMFrequency(1.1-throttlePercent))))


def Cleanup():
    SetThrottle(0)
    gpio.stop

def PrintInfo():
    print("Train Control Software Version Alpha 0.1")
    print("Written by Sami Richards for his Honours Project")
    print("####################")
    return

def main():
    MakeNoise(5)
    return

if __name__ == '__main__':
    setupPins()
    PrintInfo()
    main()
    Cleanup()

atexit.register(Cleanup)