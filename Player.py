import time
import bluetooth
from IndicationAndExperience.Indicator_player_API import Indicator
from Constants import *


class Player:
    def __init__(self):
        """ Creates a player """
        self.serverMACAddress = SERVER_MAC  # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
        self.port = COMMUNICATION_PORT
        self.s = bluetooth.BluetoothSocket()
        self.PLAYER_STATUS = None  # Free
        self.ID = ID_1  # configure to each system
        self.Indicator = Indicator()
        self.connected_flag = False
        self.game_mode = None

    def int_to_bytes(self, number: int) -> bytes:
        return number.to_bytes(length=(8 + (number + (number < 0)).bit_length()) // 8, byteorder='big', signed=True)

    def int_from_bytes(self, xbytes: bytes) -> int:
        return int.from_bytes(xbytes, 'big')

    def make_connection(self):
        for i in range(5):
            if self.s.connect_ex((self.serverMACAddress, self.port)) == 0:
                self.s.send(self.int_to_bytes(self.ID))
                data = self.int_from_bytes(self.s.recv(1024)) #Confirmation message from server = game_mode
                if data in GAME_MODES:
                    self.game_mode = data
                else:
                    raise ConnectionError
                self.Indicator.turn_on_LED(BLUE_PIN)
                self.Indicator.play_sound(CONNECTED_SOUND)
                self.connected_flag = True
                return True
            time.sleep(0.5)
        raise ConnectionError

    def check_msg(self, data):
        msg = self.int_from_bytes(data)
        return msg

    def play(self):
        while True:
            data = self.check_msg(self.s.recv(1024))  # TODO: check if player can get more than one msg
            if data == START:
                self.PLAYER_STATUS = PLAYER_FREE
                self.Indicator.turn_on_LED(GREEN_PIN)
                # self.s.send(self.int_to_bytes(START)) #Why do we need that?
            elif data == PLAYER_CAUGHT and self.PLAYER_STATUS == PLAYER_FREE:
                self.PLAYER_STATUS = PLAYER_CAUGHT
                self.Indicator.turn_on_LED(RED_PIN)
                self.Indicator.play_sound(CAUGHT_SOUND)
                if self.game_mode == RISE_OF_THE_DEAD:
                    time.sleep(KNOCK_OUT_TIME-5)
                    for i in range(10):
                        self.Indicator.turn_off_LED()
                        time.sleep(0.5)
                        self.Indicator.turn_on_LED(RED_PIN)
                    self.PLAYER_STATUS = PLAYER_FREE
                    self.s.send(self.int_to_bytes(PLAYER_FREE))

        #### self.s.close()

def show_its_on(): #todo
    """
    turn on blue led, wait 0.3 s and turn off
     (requires to make turn off led function)
    """
    pass

if __name__ == "__main__":
    show_its_on()
    try:
        player = Player()
        player.make_connection()
        player.play()
    except Exception as e: pass #todo: print to logsfile + light red led

