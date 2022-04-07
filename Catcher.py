import socket
import bluetooth
import time
import ImageProcessor
from Constants import *
from IndicationAndExperience.Indicator_catcher_API import Indicator
import select


backlog = 4  # number of devices we can connect to (can be changed)
size = 1024

# DATABASE VISION:
# client_to_tag => {Client_Address:tagID}
# client_to_status => {Client_Address:Player_Status,...}

class Catcher:
    def __init__(self):
        try:
            self.server = bluetooth.BluetoothSocket()
            self.server.bind((SERVER_MAC, COMMUNICATION_PORT))
            self.server.listen(backlog)
        except Exception as e:
            raise ConnectionError("Server can't bind and set...")
        # connection list of players (client1, client2, client3, client4)
        self.client_to_tag = dict()
        self.client_to_status = dict()
        # TODO: check how to hold all active channels and know when client becomes inactive
        self.active_client_sockets = []
        self.messages_to_send = []
        self.Indicator = Indicator()
        self.Image_processor = ImageProcessor.TagReader()
        self.game_mode = None  # None, or one of the game-modes (see constants file)

    def get_player_address(self, connection):
        """
        :param connection: the name of the player
        :return: mac addresses of given player
        """
        return self.client_to_tag[connection]

    def set_status_database(self, connection, status):
        """
        :param connection: The name of the player
        :param status: The new status we want to set
        :return: None
        """
        self.client_to_status[connection] = status

    def tagid_to_client(self, tagid):
        for key, value in self.client_to_tag.items():
            if tagid == value:
                return key
        print("No Player as such Connected...May try again to process image")
        return None

    def is_caught(self):
        """
        check if any player is caught, if so:
        1. change player status in database
        :return: list of clients that were caught
        """
        # check if a player is considered caught, send message and wait for validation
        for returned_data in self.Image_processor.return_data():
            tagid, distance = returned_data
            current_client = self.tagid_to_client(tagid)
            if distance < CATCH_DISTANCE and self.client_to_status[current_client] == PLAYER_FREE:
                # if tag is close enough AND not caught yet:
                self.messages_to_send.append((current_client, self.int_to_bytes(PLAYER_CAUGHT)))
                self.client_to_status[current_client] = PLAYER_CAUGHT

                # player_is_caught = returned_data[0]
                # if player_is_caught:
                #     self.set_database(returned_data[1], PLAYER_CAUGHT)  # set player status as caught
                #     # send message to client and find relevant id address
                #     caught_player_mac_address = self.get_player_address(returned_data[1])
                #     caught_player_mac_address.send(self.int_to_bytes(PLAYER_CAUGHT))
                #     # try to send message for at most 3 whole seconds
                #     iteration = 0
                #     while not(client.recv(1024)) and iteration <= 9:
                #         iteration += 1
                #         print('waiting for validation')
                #         client.send(self.int_to_bytes(PLAYER_CAUGHT))
                #         print('sent another message')
                #         time.sleep(0.3)
                #     # do we want to do something if message wasn't received?
                #     if iteration == 10:
                #         # do something in IndicationAndExperience...?
                #         pass


    def configure_connections(self):
        """
        1. set up in order for the game to function properly
        2. connection set up
        3. calls reset_game() in end
        :return: None
        """
        # print("started configuration")
        # # connect players - maximum four with break option
        # while len(self.database) <= 4 and not(self.Indicator.is_reset_button_pressed()):
        #     try:
        #         client_mac, client_port = self.s.accept()
        #         name = client_mac.recv(1024)     # receive name from player
        #         print(self.int_from_bytes(name))
        #         self.database[name] = [client_mac, 0]     # mac address and starting status
        #         self.player_list[len(self.database)-1] = True  # "len(database)-1" index in list
        #         self.check_game_button()
        #     except bluetooth.BluetoothError:
        #         break
        # # send each player a 'start' message
        # else:
        #     for player in self.database:
        #         player_address = self.get_player_address(player)
        #         player_address.send(START)
        # # reset player's status
        # self.reset_game(self.database)
        pass

    def check_game_button(self):
        """
        check if reset_game_button was pressed, if so, reset all player's status
        :return: True or None
        """
        if self.Indicator.is_reset_button_pressed() is True:
            self.reset_game(self.client_to_status)
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
            self.set_status_database(player, PLAYER_FREE)


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
        for player in self.client_to_status:
            if self.client_to_status[player] == 0:
                return False
        else:
            return True


    def wake_up(self):
        """
        Make wakeup sound
        :return: None
        """
        self.Indicator.play_sound(WAKE_UP_BEEP)


    def add_new_client_to_DB(self, connection, tagid):
        """
        Updates list of active clients and databases
        :param connection: Bluetooth socket
        :param tagid: The players ID
        :return: None
        """
        self.active_client_sockets.append(connection)
        self.client_to_status[connection] = PLAYER_FREE
        self.client_to_tag[connection] = tagid
        # Todo: solve conflicts when client re-connect


    def start_the_game(self):
        """
        Sends each player a message to indicate that the game has started
        :return: None
        """
        for client in self.active_client_sockets:
            self.messages_to_send.append((client, self.int_to_bytes(START)))


    def reset_to_default_setup(self):
        self.Indicator.play_sound(WAKE_UP_BEEP)
        for client in self.active_client_sockets:
            self.client_to_status[client] = PLAYER_FREE
            self.messages_to_send.append((client, PLAYER_FREE))


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
        while True:
            if self.game_mode:
                self.is_caught()

            rlist, wlist, xlist = select.select([self.server] + self.active_client_sockets,
                                                self.active_client_sockets, [])
            for current_socket in rlist:
                if current_socket is self.server:
                    connection, client_address = current_socket.accept()
                    new_tagid = current_socket.recv(BUFFER_SIZE)
                    print("New client joined!", client_address, "and tagID is", new_tagid)
                    self.add_new_client_to_DB(connection, new_tagid)
                    # print_client_sockets(client_sockets)
                else:
                    try:
                        data = self.int_from_bytes(current_socket.recv(BUFFER_SIZE))
                    except socket.error as e:
                        print("Connection closed", current_socket)
                        self.active_client_sockets.remove(current_socket)
                        current_socket.close()

            for message in self.messages_to_send:
                current_socket, data = message
                if current_socket in wlist:
                    current_socket.send(self.int_to_bytes(data))
                    self.messages_to_send.remove(message)

            if self.Indicator.is_reset_button_pressed():
                self.reset_to_default_setup()


        # while not self.reset_state:# and self.check_game_end():
        #     # check if player is caught
        #     self.is_caught()
        #     # wait 0.3 sec before rerunning loop
        #     time.sleep(0.3)
        #     self.reset_state = self.Indicator.is_reset_button_pressed()


if __name__ == "__main__":
    game_module = Catcher()
    game_module.wake_up()
    game_module.game_loop()
    # try:
    #     # set up in order for the game to function properly connection set up
    #     game_module.configure_connections()
    #     # checks if player is caught (via is_caught()) and reacts accordingly while game is played
    #     game_module.game_loop()
    #
    # except ConnectionError:
    #     # print("Closing socket")
    #     game_module.s.close()
