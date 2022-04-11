import gpiozero
from Constants import *

red_led = gpiozero.LED(RED_PIN)
green_led = gpiozero.LED(GREEN_PIN)
blue_led = gpiozero.LED(BLUE_PIN)


def turn_off_all():
    green_led.off()
    red_led.off()
    blue_led.off()


def turn_on_led(PIN_COLOR):
    turn_off_all()
    led = gpiozero.LED(PIN_COLOR)
    led.on()

