import gpiozero
from Constants import *
from gpiozero.tones import Tone
import time
import sys
import RPi.GPIO as GPIO
import board
import neopixel

class Indication:
    def __init__(self):
        #self.red_led = gpiozero.LED(RED_PIN)
        #self.green_led = gpiozero.LED(GREEN_PIN)
        #self.blue_led = gpiozero.LED(BLUE_PIN)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(AUDIO_PIN,GPIO.OUT)
        self.buzzer = GPIO.PWM(AUDIO_PIN, 500)
        self.switch = gpiozero.Button(SWITCH_PIN)
        self.button = gpiozero.Button(BUTTON_PIN)
        self.led_strip = neopixel.NeoPixel(board.D18,NUM_OF_PIXELS,auto_write=False)
        

    def turn_off_all(self):
        self.turn_on_LED("off")

    def turn_on_LED(self, color):
        for i in range(NUM_OF_PIXELS):
            self.led_strip[i] = COLOR_DICT[color]
            self.led_strip.show()
    
    def show_connection(self, tagid):
        self.led_strip[PLAYER_LED_LIST[tagid]] = COLOR_DICT["blue"]
        self.led_strip.show()


    def wheel(self,pos):
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos*3)
            g = int(255-pos*3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255-pos*3)
            g = 0
            b = int(pos*3)
        else:
            pos -= 170
            r = 0
            g = int(pos*3)
            b = int(255-pos*3)
        return (r,g,b)


    def rainbow(self,cycles=10,wait=0.001):
        for k in range(cycles):
            for j in range(255):
                for i in range(NUM_OF_PIXELS):
                    pixel_index = (i * 256 // NUM_OF_PIXELS) + j
                    self.led_strip[i] = wheel(pixel_index & 255)
                self.led_strip.show()
                time.sleep(wait)        
    
    def get_gamemode(self):
        if self.switch.value == 1:
            return CATCH_EM_ALL
        elif self.switch.value == 0:
            return RISE_OF_THE_DEAD

    def switch_test(self):
        for i in range(100):
            print(i,'s',self.is_switch_pressed(),'b',self.is_button_pressed())
            time.sleep(1)
    
    def switch_read(self):
        return self.switch.value
    
    def is_button_pressed(self):
        return self.button.value

    def player_been_caught_sound(self):
        self.buzzer.ChangeFrequency(400)
        self.buzzer.start(90)
        time.sleep(0.05)
        self.buzzer.stop()
        for _ in range(3):
            self.buzzer.start(90)
            time.sleep(0.5)
            self.buzzer.stop()
            time.sleep(0.5)

    def wake_up_sound(self):
        for _ in range(3):
            self.buzzer.start(100)
            time.sleep(0.08)
            self.buzzer.stop()
            time.sleep(0.08)
            
    def start_game_sound(self):
        for i in range(800,500,-40):
            self.buzzer.ChangeFrequency(i)
            self.buzzer.start(10)
            time.sleep(0.08)
        for i in range(500,900,40):
            self.buzzer.ChangeFrequency(i)
            self.buzzer.start(10)
            time.sleep(0.08)
        self.buzzer.stop()

            
    def catcher_caught_sound(self, cycles=1):
        for _ in range(cycles):
            self.buzzer.ChangeFrequency(659)
            self.buzzer.start(20)
            time.sleep(0.1)
            self.buzzer.stop()
            time.sleep(0.05)
            self.buzzer.ChangeFrequency(880)
            self.buzzer.start(10)
            time.sleep(0.4)
            self.buzzer.stop()
            time.sleep(0.6)


if __name__ == "__main__":
    ind = Indication()
    ind.switch_test()
