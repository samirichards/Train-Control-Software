import time
import pigpio
from enum import Enum

#Pin assignments
pin_IN1 = 6
pin_IN2 = 5
pin_pwm_D1 = 13
pin_pwm_D2 = 12
pin_INV = 19
pin_EN = 26
pin_SLEW = 22
pin_SF = 17

class Direction(Enum):
    #A end = away from motor
    #B end = towards motor
    A = 0
    B = 1
#Setup defaults
CurrentDirection = Direction.A

gpio = pigpio.pi()

def setupPins():
    gpio.set_mode(pin_IN1, pigpio.OUTPUT)
    gpio.set_mode(pin_IN2, pigpio.OUTPUT)

    gpio.set_mode(pin_pwm_D1, pigpio.OUTPUT)
    gpio.set_mode(pin_pwm_D2, pigpio.OUTPUT)
    gpio.set_PWM_range(pin_pwm_D1, 255)
    gpio.set_PWM_range(pin_pwm_D2, 255)
    gpio.set_PWM_frequency(pin_pwm_D1, 16000)
    gpio.set_PWM_frequency(pin_pwm_D2, 16000)

    gpio.set_mode(pin_INV, pigpio.OUTPUT)
    gpio.set_mode(pin_EN, pigpio.OUTPUT)
    gpio.set_mode(pin_SLEW, pigpio.OUTPUT)
    gpio.set_mode(pin_SF, pigpio.INPUT)
    gpio.set_pull_up_down(pin_SF, pigpio.PUD_UP)

    gpio.write(pin_IN1, pigpio.LOW)
    gpio.write(pin_IN2, pigpio.LOW)
    gpio.write(pin_INV, pigpio.LOW)
    gpio.write(pin_EN, pigpio.HIGH)
    gpio.write(pin_SLEW, pigpio.HIGH)

    SetDirection(Direction.A)

def GetDirection():
    if gpio.read(pin_INV) == pigpio.LOW:
        return Direction.A
    else:
        return Direction.B

def SetDirection(dir):
    if dir == Direction.A:
        gpio.write(pin_INV, pigpio.LOW)
    else:
        gpio.write(pin_INV, pigpio.HIGH)

def GetStatus():
    return gpio.read(pin_SF)

def SetThrottle(throttlePercent):
    if throttlePercent <= 0:
        gpio.write(pin_EN, pigpio.LOW)
        gpio.hardware_PWM(pin_pwm_D1, 0, 0)
        gpio.hardware_PWM(pin_pwm_D2, 0, 0)
        gpio.write(pin_IN1, pigpio.LOW)
        gpio.write(pin_IN2, pigpio.LOW)
        return
    else:
        gpio.write(pin_EN, pigpio.HIGH)

    #dutyCycle = int(throttlePercent / 100.0 * 255)
    dutyCycle = int(throttlePercent * 10000)
    if CurrentDirection == Direction.A:
        gpio.write(pin_IN1, pigpio.HIGH)
        gpio.write(pin_IN2, pigpio.LOW)
        gpio.hardware_PWM(pin_pwm_D1, 16000, dutyCycle)
        gpio.hardware_PWM(pin_pwm_D2, 16000, 0)
    else:
        gpio.write(pin_IN1, pigpio.LOW)
        gpio.write(pin_IN2, pigpio.HIGH)
        gpio.hardware_PWM(pin_pwm_D1, 16000, 0)
        gpio.hardware_PWM(pin_pwm_D2, 16000, dutyCycle)

print("Status pin is initally: " + str(GetStatus()))
#setupPins()
#This function needs to work

gpio.set_mode(pin_IN1, pigpio.OUTPUT)
gpio.set_mode(pin_IN2, pigpio.OUTPUT)
gpio.set_mode(pin_pwm_D1, pigpio.OUTPUT)
gpio.set_mode(pin_pwm_D2, pigpio.OUTPUT)


print("Status pin is currently: " + str(GetStatus()))
time.sleep(0.1)
SetThrottle(100)
print(str(gpio.read(pin_EN)))
time.sleep(3)
SetThrottle(0)
print("Status pin is now: " + str(GetStatus()))
exit
