import time
import pigpio
from enum import Enum

#Pin assignments
pin_pwm_IN1 = 13
pin_pwm_IN2 = 12

class Direction(Enum):
    #A end = away from motor
    #B end = towards motor
    A = 0
    B = 1
#Setup defaults
CurrentDirection = Direction.A

gpio = pigpio.pi()

gpio.set_PWM_range(pin_pwm_IN1, 255)
gpio.set_PWM_range(pin_pwm_IN2, 255)
gpio.set_PWM_frequency(pin_pwm_IN1, 600)
gpio.set_PWM_frequency(pin_pwm_IN2, 600)
gpio.set_PWM_dutycycle(pin_pwm_IN1, 204)
#gpio.set_PWM_dutycycle(pin_pwm_IN2, 128)

time.sleep(10)

gpio.set_PWM_dutycycle(pin_pwm_IN1, 0)
gpio.set_PWM_dutycycle(pin_pwm_IN2, 0)



exit