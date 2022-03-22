"""
player:
1. function that controls the NOT_CAUGHT led - recieve ON or OFF
2. function that controls the CAUGHT led - recieve ON or OFF
3. function that controls the Speaker - receive CAUGHT or NOT_CAUGHT (to know which sound to play)
"""
import RPi.GPIO as GPIO
import playsound


class Indicator:
    RED_PIN = 5
    GREEN_PIN = 6
    BLUE_PIN = 7
    PLAYER_PINS = RED_PIN, GREEN_PIN, BLUE_PIN
    CAUGHT_SOUND = 9
    CONNECTED_SOUND = 10

    def __init__(self):
        """
        determine the PIN numbers. and other settings required.
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # set up the LEDs as output

        for LED in self.PLAYER_PINS:
            GPIO.setup(LED, GPIO.OUT)

    def turn_on_LED(self, LED: int):
        """
        :param LED: RED, BLUE, GREEN or NONE
        :return: NONE
        turns that LED on and turns off the rest of them
        """
        for pin in self.PLAYER_PINS:
            if pin != LED:
                GPIO.output(pin, GPIO.LOW)

        if LED in self.PLAYER_PINS:
            GPIO.output(LED, GPIO.HIGH)

    def play_sound(self, sound: str):
        """
        :param sound: what sound needs to be played: CAUGHT or CONNECTED
        :return: NONE
        """
        playsound.playsound(sound)

        pass
