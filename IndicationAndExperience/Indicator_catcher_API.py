"""
catcher:
1. function that lights 4-leds according to list that it receives. [1,0,0,1]
2. function that checks the reset_game button and returns True or False

"""
import RPi.GPIO as GPIO


class Indicator:
    CATCHER_PINS = [1, 2, 3, 4]
    RESET_BUTTON = 8

    def __init__(self):
        """
        determine the PIN numbers. and other settings required.
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.RESET_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # the default state for the switch is off

        # set up the LEDs as output
        for LED in self.CATCHER_PINS:
            GPIO.setup(LED, GPIO.OUT)
        pass

    def control_catcher_LED_array(self, players: list):
        """
        :param players: a 4 - LED list of binary values ex. [TRUE, FALSE, TRUE, TRUE]
        :return: NONE
        """
        for i in range(4):
            if players[i]:
                GPIO.output(self.CATCHER_PINS[i], GPIO.HIGH)
            else:
                GPIO.output(self.CATCHER_PINS[i], GPIO.LOW)
        pass

    def is_reset_button_pressed(self):
        """
        :return: TRUE / FALSE
        you can figure out what it does, right?
        """
        return GPIO.input(self.RESET_BUTTON) == GPIO.HIGH

      def turn_off_LED(self):
            """
            :param LED: RED, BLUE, GREEN or NONE
            :return: NONE
            turns that LED on and turns off the rest of them
            """
            for pin in self.PLAYER_PINS:
                GPIO.output(pin, GPIO.LOW)