import socket
import bluetooth
import time
import ImageProcessor
from Constants import *
from IndicationAndExperience.Indicator_catcher_API import Indicator



hostMACAddress = SERVER_MAC  # The MAC address of a Bluetooth adapter on the server.
port = COMMUNICATION_PORT
backlog = 4  # number of devices we can connect to (can be changed)
size = 1024



class Catcher:
    def __init__(self):
        self.s = bluetooth.BluetoothSocket()
        self.s.bind((hostMACAddress, port))
        self.s.listen(backlog)

        # Current player status data structure
        self.database = dict()
        # connection list of players (client1, client2, client3, client4)
        self.player_list = [False, False, False, False]
        self.Indicator = Indicator()
        self.Image_processor = ImageProcessor.TagReader()

    def get_player_address(self, player_name):
        """
        :param player_name: the name of the player
        :param dictionary: database of players in game
        :return: mac addresses of given player
        """
        return self.database[player_name][0]


    def set_database(self, player_name, status):
        """
        :param player_dictionary: The dictionary we want to update
        :param player_name: The name of the player
        :param status: The new status we want to set
        :return: None
        """
        self.database[player_name][1] = status


    def is_caught(self):
        """
        check if any player is caught, if so:
        1. change player status in database
        2. send message to client
        3. wait for eco from client, else, (after 3 seconds) turn to IndicationAndExperience
        :return: None
        """
        # check if a player is considered caught, send message and wait for validation
        for returned_data in self.Image_processor.return_data():
            player_is_caught = returned_data[0]
            if player_is_caught:
                self.set_database(returned_data[1], PLAYER_CAUGHT)  # set player status as caught
                # send message to client and find relevant id address
                caught_player_mac_address = self.get_player_address(returned_data[1])
                caught_player_mac_address.send(self.int_to_bytes(PLAYER_CAUGHT))
                # try to send message for at most 3 whole seconds
                iteration = 0
                while not(client.recv(1024)) and iteration <= 9:
                    iteration += 1
                    print('waiting for validation')
                    client.send(self.int_to_bytes(PLAYER_CAUGHT))
                    print('sent another message')
                    time.sleep(0.3)
                # do we want to do something if message wasn't received?
                if iteration == 10:
                    # do something in IndicationAndExperience...?
                    pass
            else:
                pass


    def configure_connections(self):
        """
        1. set up in order for the game to function properly
        2. connection set up
        3. calls reset_game() in end
        :return: None
        """
        print("started configuration")
        # connect players - maximum four with break option
        while len(self.database) <= 4 and not(self.Indicator.is_reset_button_pressed()):
            try:
                client_mac, client_port = self.s.accept()
                name = client_mac.recv(1024)     # receive name from player
                print(self.int_from_bytes(name))
                self.database[name] = [client_mac, 0]     # mac address and starting status
                self.player_list[len(self.database)-1] = True  # "len(database)-1" index in list
                self.check_game_button()
            except bluetooth.BluetoothError:
                break
        # send each player a 'start' message
        else:
            for player in self.database:
                player_address = self.get_player_address(player)
                player_address.send(START)
        # reset player's status
        self.reset_game(self.database)

    def check_game_button(self):
        """
        :param player_dict: dictionary with player info
        check if reset_game_button was pressed, if so, reset all player's status
        :return: True or None
        """
        if self.Indicator.is_reset_button_pressed() is True:
            self.reset_game(self.database)
            return True


    def reset_game(self, player_dict):
        """
        :param player_dict: dictionary with player info
        be called (1) after configure_connections or (2) after the game if reset button pressed.
        1. initialize lights in catcher
        2. resets the database status for players
        :return: returns the database dictionary with reset status
        """
        for player in player_dict:
            self.set_database(player, PLAYER_FREE)


    def int_from_bytes(self, binary_data):
        """
        :param binary_data: data in binary format
        :return: given data in int form
        """
        return int.from_bytes(binary_data, byteorder='big', signed=True)


    def int_to_bytes(self, number: int) -> bytes:
        """
        :param number: int data
        :return: given int data in binary format
        """
        return number.to_bytes(length=(8 + (number + (number < 0)).bit_length()) // 8, byteorder='big', signed=True)


    def check_game_end(self):
        """
        check if all players are caught, True is returned if so
        :return: bool
        """
        for player in self.database:
            if self.database[player][1] == 0:
                return False
        else:
            return True


    def game_loop(self):
        """
        while the reset button isn't presses and the game hasn't ended yet -
        1. calculates "is caught"
            1. checks if player was caught
            2. sends message and verify receiving
            3. updates the database
        2. wait 0.3 seconds
        :return: None
        """
        while not Indicator.is_reset_button_pressed() and self.check_game_end():
            # check if player is caught
            self.is_caught()
            # wait 0.3 sec before rerunning loop
            time.sleep(0.3)


if __name__ == "__main__":
    game_module = Catcher()
    # try:
    #     # set up in order for the game to function properly connection set up
    #     game_module.configure_connections()
    #     # checks if player is caught (via is_caught()) and reacts accordingly while game is played
    #     game_module.game_loop()
    #
    # except ConnectionError:
    #     # print("Closing socket")
    #     game_module.s.close()
    game_module.configure_connections()