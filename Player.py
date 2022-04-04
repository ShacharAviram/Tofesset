
import bluetooth
from IndicationAndExperience import Indicator_player_API as Indicator
import Constants


class Player:
    def __init__(self):
        """ Creates a player """
        self.serverMACAddress = '8c:c8:4b:80:50:42'  # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
        self.port = 5
        self.s = bluetooth.BluetoothSocket()
        self.PLAYER_STATUS = 0  # Free
        self.ID = 7  # configure to each system

    def int_to_bytes(self, number: int) -> bytes:
        return number.to_bytes(length=(8 + (number + (number < 0)).bit_length()) // 8, byteorder='big', signed=True)

    def int_from_bytes(self, xbytes: bytes) -> int:
        return int.from_bytes(xbytes, 'big')

    def make_connection(self):
        for i in range(5):
            if self.s.connect_ex((self.serverMACAddress, self.port)) == 0:
                self.s.send(self.int_to_bytes(self.ID))
                return True
        return False

    def check_msg(self, data):
        msg = self.int_from_bytes(data)
        return msg

    def play(self):
        if self.s.connect_ex((self.serverMACAddress, self.port)) == 0:  # Change to make connection function.
            Indicator.turn_on_led(Constants.BLUE_PIN)
            Indicator.play_sound(Constants.CONNECTED_SOUND)
            self.s.send(self.int_to_bytes(self.ID))
            while True:
                data = self.s.recv(1024)  # TODO: check if player can get more than one msg
                if self.check_msg(data) == Constants.START:
                    self.PLAYER_STATUS = 0
                    Indicator.turn_on_led(Constants.GREEN_PIN)
                    self.s.send(self.int_to_bytes(Constants.START))
                elif self.check_msg(data) == Constants.PLAYER_CAUGHT:
                    self.PLAYER_STATUS = 1
                    Indicator.turn_on_led(Constants.RED_PIN)
                    Indicator.play_sound(Constants.CAUGHT_SOUND)
                    return_text = self.int_to_bytes(Constants.PLAYER_CAUGHT)
                    self.s.send(return_text)
            #### self.s.close()
        else:
            print('connection failed')


if __name__ == "__main__":
    player = Player()
    player.make_connection()
    #player.play()


