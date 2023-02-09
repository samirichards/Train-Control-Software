import pigpio
from enum import Enum
import time
from dual_mc33926_rpi import motors, MAX_SPEED

#Pin assignments
pin_IN1 = 6
pin_IN2 = 5
pin_pwm_D1 = 13
pin_pwm_D2 = 12
pin_INV = 19
pin_EN = 26
pin_SLEW = 22

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
    gpio.set_mode(pin_INV, pigpio.OUTPUT)
    gpio.set_mode(pin_EN, pigpio.OUTPUT)
    gpio.set_mode(pin_SLEW, pigpio.OUTPUT)

    gpio.write(pin_IN1, pigpio.LOW)
    gpio.write(pin_IN2, pigpio.LOW)
    gpio.write(pin_pwm_D1, pigpio.LOW)
    gpio.write(pin_pwm_D2, pigpio.LOW)
    gpio.write(pin_INV, pigpio.LOW)
    gpio.write(pin_EN, pigpio.LOW)
    gpio.write(pin_SLEW, pigpio.LOW)

    SetDirection(Direction.A)

    motors.motor1.__init__(pin_pwm_D1, pin_IN1, pin_EN)

def GetDirection():
    if gpio.read(pin_INV) == pigpio.LOW:
        return Direction.A
    else:
        return Direction.B

def SetDirection(dir):
    if dir == Direction.A:
        gpio.write(pin_INV, pigpio.LOW)
    else:
        gpio.write(pin_IN1, pigpio.HIGH)


setupPins()
motors.motor1.setSpeed(100)
time.sleep(1)
motors.motor1.setSpeed(0)
exit
