import socket
import bluetooth
import time
import ImageProcessor
from Constants import *
from Indicator import *
import select
import logger as logfile
from Indicator import Indication

backlog = 4  # number of devices we can connect to (can be changed)
size = 1024

# DATABASE VISION:
# tagid_to_client => {tagID:Client_Address}
# client_to_status => {tagID:Player_Status,...}

class Catcher:
    def __init__(self):
        self.logger = logfile.log_creater(LOG_FILE_NAME)
        try:
            self.server = bluetooth.BluetoothSocket()
            self.server.bind((SERVER_MAC, COMMUNICATION_PORT))
            self.server.listen(backlog)
        except Exception as e:
            raise ConnectionError("Server can't bind and set...")
        # connection list of players (client1, client2, client3, client4)
        self.tagid_to_client = dict()
        self.tagid_to_status = dict()
        self.players_catches = dict() 
        # TODO: check how to hold all active channels and know when client becomes inactive
        self.active_client_sockets = []
        self.Indicator = Indication()
        self.disconnected_client_sockets = []
        self.messages_to_send = []
        self.Image_processor = ImageProcessor.TagReader()
        self.game_mode = None  # None, or one of the game-modes (see constants file)
        
    
    def get_player_address(self, tagid):
        """
        :param tagid: the name of the player
        :return: BT object to communicate with
        """
        return self.tagid_to_client[tagid]

    def set_status_database(self, tagid, status):
        """
        :param tagid: The name of the player
        :param status: The new status we want to set
        :return: None
        """
        self.tagid_to_status[tagid] = status

    def get_client_from_tag(self, tagid):
        if tagid in self.tagid_to_client:
            return self.tagid_to_client[tagid]
        print("No Player as such Connected...May try again to process image")
        return None

    def get_tagid_from_client(self, socket):
        for tagid, client in self.tagid_to_client.items():
            if client == socket:
                return tagid
                   

    def is_caught(self):
        """
        check if any player is caught, if so:
        1. change player status in database
        :return: list of clients that were caught
        """
        for tagid,catches in self.players_catches.items():
            if self.tagid_to_status[tagid] == PLAYER_FREE and catches > 0:
                self.players_catches[tagid] -= 1
                print(self.players_catches[tagid])

        # check if a player is considered caught, send message and wait for validation
        for returned_data in self.Image_processor.return_data():
            tagid, distance = returned_data
            if tagid in self.tagid_to_status.keys():
                current_client = self.tagid_to_client[tagid]
                print("trying to catch player that is:", self.tagid_to_status[tagid])
                if current_client and 0 < distance < CATCH_DISTANCE and self.tagid_to_status[tagid] == PLAYER_FREE:
                    # if tag is close enough AND not caught yet:
                    self.players_catches[tagid] += 2
                    print(tagid, self.players_catches[tagid]) 
                    if self.players_catches[tagid] > IMAGES_TO_CATCH:
                        self.messages_to_send.append((current_client, PLAYER_CAUGHT))
                        self.tagid_to_status[tagid] = PLAYER_CAUGHT
                        self.Indicator.catcher_caught_sound()
                        self.Indicator.turn_on_LED("red")
                        time.sleep(0.3)
                        self.Indicator.turn_on_LED("turquoise")
                        self.players_catches[tagid] = 0 

    def check_game_button(self):
        """
        check if reset_game_button was pressed, if so, reset all player's status
        :return: True or None
        """
        # if is_reset_button_pressed() is True:
        #     return True
        pass


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
        if len(self.tagid_to_status) == 1 and self.game_mode == RISE_OF_THE_DEAD:
            return False
        for player in self.tagid_to_status:
            if self.tagid_to_status[player] == PLAYER_CAUGHT:
                return True
        else:
            return False


    def wake_up(self):
        """
        Make wakeup sound
        :return: None
        """
        self.Indicator.wake_up_sound()
        self.Indicator.turn_on_LED("yellow")


    def add_new_client_to_DB(self, connection, tagid):
        """
        Updates list of active clients and databases
        :param connection: Bluetooth socket
        :param tagid: The players ID
        :return: None
        """
        self.tagid_to_status[tagid] = PLAYER_FREE
        self.tagid_to_client[tagid] = connection
        self.players_catches[tagid] = 0
        if not self.game_mode:
          self.Indicator.show_connection(tagid)
        # Todo: solve conflicts when client re-connect


    def start_the_game(self):
        """
        ****NOT IN USE****
        Sends each player a message to indicate that the game has started
        :return: None
        """
        pass
        #for client in self.active_client_sockets:
        #    self.messages_to_send.append((client, self.int_to_bytes(START)))



    def reset_to_default_setup(self):
        """
        Sends each player a message to indicate that the game has started plus the current GameMode
        :return: None
        """
        # get gamemode from button
        self.Indicator.turn_off_all()
        time.sleep(0.3)
        
        print("Game started!")
        print("active players: ", self.tagid_to_status.keys())
        try:
            print(self.Indicator.switch_read())
            if self.Indicator.switch_read() == 1:
                self.game_mode = CATCH_EM_ALL
                print("Game mode: CATCH_EM_ALL")

            else:
                self.game_mode = RISE_OF_THE_DEAD
                print("Game mode: RISE_OF_THE_DEAD")

        except Exception as e:
            print(e)
            self.game_mode = CATCH_EM_ALL
            print("Default Game mode: CATCH_EM_ALL")

            
        self.Indicator.start_game_sound()
        self.Indicator.turn_on_LED("turquoise")
        for client in self.active_client_sockets:
            self.set_status_database(self.get_tagid_from_client(client), PLAYER_FREE)
            self.messages_to_send.append((client, self.game_mode))
        

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
            print(self.active_client_sockets)
            rlist, wlist, xlist = select.select([self.server] + self.active_client_sockets,
                                                self.active_client_sockets, [])
            for current_socket in rlist:
                if current_socket is self.server:
                    # Connect player to the server
                    connection, client_address = current_socket.accept()
                    self.active_client_sockets.append(connection)
                    # Remove client from disconnected player list, and set player as free
                    if current_socket in self.disconnected_client_sockets:
                        self.disconnected_client_sockets.remove(current_socket)

                    # Print client info
                    print("New client joined! It's address is:", client_address)
                    print(self.active_client_sockets)
                
                else:
                    try:
                        data = self.int_from_bytes(current_socket.recv(BUFFER_SIZE))
                        if data in ID_LIST:
                            print("And tag ID is:", data)
                            self.add_new_client_to_DB(self.active_client_sockets[-1], data)
                            print(self.tagid_to_status, self.game_mode)
                            self.messages_to_send.append((current_socket, self.tagid_to_status[data]))
                            if self.game_mode:
                                self.messages_to_send.append((current_socket, self.game_mode))

                        elif data == PLAYER_FREE and self.game_mode == RISE_OF_THE_DEAD:
                            self.tagid_to_status[self.get_tagid_from_client(current_socket)] = data
                            #self.active_client_sockets.append(current_socket)

                    except socket.error as e:
                        print("Connection closed", current_socket, e)
                        self.disconnected_client_sockets.append(current_socket)
                        self.active_client_sockets.remove(current_socket)
                        current_socket.close()

            for message in self.messages_to_send:
                current_socket, data = message
                if current_socket in wlist:
                    current_socket.send(self.int_to_bytes(data))
                    self.messages_to_send.remove(message)

            if self.Indicator.is_button_pressed():
                self.reset_to_default_setup()
            
            if self.check_game_end():
                self.Indicator.catcher_caught_sound()
                self.Indicator.rainbow()
                if self.Indicator.is_button_pressed():
                    self.reset_to_default_setup()
                time.sleep(1)
                
if __name__ == "__main__":
    try:
        game_module = Catcher()
        game_module.wake_up()
        game_module.game_loop()
    except KeyboardInterrupt as e:
        print(e)
        game_module.Indicator.turn_off_all()
    except Exception as e:
        print(e)
        while True:
            self.Indicator.turn_off_all()
            time.sleep(0.5)
            self.Indiator.turn_on_LED("red")
            time.sleep(0.5)
    #Indication.turn_off_all(Indication())
    #dicator = Indication()
    #dicator.turn_on_LED("violet")
    
