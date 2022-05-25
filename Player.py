import time
import bluetooth
import socket

from Indicator import Indication
from Constants import *


class Player:
    def __init__(self):
        """ Creates a player """
        self.serverMACAddress = SERVER_MAC  # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
        self.port = COMMUNICATION_PORT
        self.s = bluetooth.BluetoothSocket()
        self.Indicator = Indication()
        self.PLAYER_STATUS = None  # Free
        self.ID = ID_1  # configure to each system
        self.connected_flag = False
        self.game_mode = None

    def int_to_bytes(self, number: int) -> bytes:
        """
        Returns int into bytes
        :param number: The message in int form
        :return: The message in byte form
        """
        return number.to_bytes(length=(8 + (number + (number < 0)).bit_length()) // 8, byteorder='big', signed=True)


    def int_from_bytes(self, xbytes: bytes) -> int:
        """
        Returns int into bytes
        :param xbytes: The message in byte form
        :return: The message in int form
        """
        return int.from_bytes(xbytes, 'big')


    def make_connection(self):
        """
        Creates a connection for each player system
        :return: None
        """
        for i in range(20):
            try:
                self.s.connect((self.serverMACAddress, self.port))
            except:
                time.sleep(0.5)
                continue
            self.s.send(self.int_to_bytes(self.ID))
            print("before")
            data = self.check_msg(self.s.recv(1024))
            print("after")
            if data in PLAYER_STATUSES:
                self.PLAYER_STATUS = data
            self.Indicator.turn_on_LED("blue")
            self.connected_flag = True
            time.sleep(0.5)
            return True
        print('unable to connect, turn off and back on')
        while True:
            self.Indicator.turn_off_all()
            time.sleep(0.5)
            self.Indicator.turn_on_LED("red")
            time.sleep(0.5)

    def check_msg(self, data):
        """
        Transforms message in bytes to int
        :param data: message in bytes
        :return: message in int
        """
        msg = self.int_from_bytes(data)
        return msg


    def caught_in_rise_of_the_dead(self):
        """
        waits KNOCKOUTTIME before getting back to the game. if the server sends message to start new game, we can handle it.
        """

        self.s.settimeout(0.1)  # so we can wait for messages inside a running loop
        if KNOCK_OUT_TIME < 5:
            blinking_time = 0
        else:
            blinking_time = 5


        for i in range(KNOCK_OUT_TIME-blinking_time):
            time.sleep(1)
            try:
                data = self.check_msg(self.s.recv(1024))  # TODO: check if player can get more than one msg
                if data in GAME_MODES:

                    self.game_mode = data
                    self.set_me_free()
                    self.s.settimeout(None)
                    return
            except Exception as e:
                pass

        for i in range(blinking_time):
            self.Indicator.turn_on_LED("orange")
            time.sleep(1)
            try:
                data = self.check_msg(self.s.recv(1024))  # TODO: check if player can get more than one msg
                if data in GAME_MODES:
                    self.game_mode = data
                    self.set_me_free()

                    self.s.settimeout(None)  # get back to game with no timeout
                    return
            except socket.timeout:
                pass
            except Exception as e:
                print(e)

        self.s.settimeout(None)
        self.set_me_free()
        time.sleep(0.2)
        self.s.send(self.int_to_bytes(PLAYER_FREE))  # make the server know that Im free


    def check_connection_to_server(self):
        """
        Checks if player is still connected and updates flag as required
        :return: None
        """
        try:
            self.s.getpeername()
            self.connected_flag = True
        except:
            self.connected_flag = False
            
    def set_me_free(self):
        self.PLAYER_STATUS = PLAYER_FREE
        self.Indicator.turn_on_LED("green")
        self.Indicator.start_game_sound()

    def play(self):
        """
        Main player loop
        :return: None
        """
        try:
            while self.connected_flag:

                # At the beginning of each loop we'll check if we are still connected.
                self.check_connection_to_server()
                data = self.check_msg(self.s.recv(1024))  # TODO: check if player can get more than one msg
                if data in GAME_MODES:
                    self.game_mode = data
                    print(self.game_mode)
                    self.set_me_free()
                    
                elif data == SERVER_DOWN:
                    time.sleep(15)
                    raise Exception("Server is down")
                        
                elif data == PLAYER_CAUGHT and self.PLAYER_STATUS == PLAYER_FREE:
                    self.PLAYER_STATUS = PLAYER_CAUGHT
                    self.Indicator.turn_on_LED("red")
                    self.Indicator.player_been_caught_sound()
                    print("CAUGHT")

                    if self.game_mode == RISE_OF_THE_DEAD:
                        self.caught_in_rise_of_the_dead()
        except Exception as e:
            print("Error raised: ", e) #logging
            self.connected_flag = False
            self.s.close()
            print("trying to reconnect")
            self.make_connection()

    def show_its_on(self):  
        """
        turn on blue led, wait 0.3 s and turn off
        """
        self.Indicator.turn_on_LED("yellow")
        self.Indicator.wake_up_sound()



if __name__ == "__main__":
    try:
        player = Player()
        player.show_its_on()
        player.make_connection()
        player.play()
    except KeyboardInterrupt:
        player.Indicator.turn_off_all()
    except Exception as e:
        print("oops", e)  # TODO: print to logsfile + light red led
