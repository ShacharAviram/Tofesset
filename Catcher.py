import socket
import select
from ImageProcess.ImageProcessor import ImageProcessor
from Constants import *
import bluetooth
import time


hostMACAddress = '8c:c8:4b:80:50:42'  # The MAC address of a Bluetooth adapter on the server.
port = 5
backlog = 4  # number of devices we can connect to (can be changed)
size = 1024


s = bluetooth.BluetoothSocket()
s.bind((hostMACAddress, port))
s.listen(backlog)

# print(f'Listening for connections on {IP}:{PORT}...')

# Current player status
database = dict()
# connection list of players (client1, client2, client3, client4)
player_list = [False, False, False, False]


def get_player_address_list(dictionary):
    """
    :param dictionary: database of players in game
    :return: List of mac addresses of all players
    """
    mylist = []
    for key in dictionary.keys():
        mylist.append(dictionary[key][0])
    return mylist


def set_database(player_dictionary, player_name, status):
    """
    :param player_dictionary: The dictionary we want to update
    :param player_name: The name of the player
    :param status: The new status we want to set
    :return: None
    """
    player_dictionary[player_name][1] = status


def is_caught():
    """
    check if any player is caught, if so:
    1. change player status in database
    2. send message to client
    :return:
    """
    # check if a player is considered caught, send message and wait for validation
    # assuming the received data is in the following format: (bool, id)
    for returned_data in ImageProcessor.ImageProcessor.return_data():
        player_is_caught = returned_data[0]
        if player_is_caught:
            set_database(database, returned_data[1], 1)  # set player status as caught
            # send message to client and find relevant id address
            for client in get_player_address_list(database):
                if client == returned_data[1]:
                    # send relevant message to client
                    client.send(int_to_bytes(PLAYER_CAUGHT))

                while not(client.recv(1024)):
                    print('waiting for validation')
                    client.send(int_to_bytes(PLAYER_CAUGHT))
                    print('sent another message')
        else:
            pass


def configure_connections():
    """
    1. set up in order for the game to function properly
    2. connection set up
    -calls reset game in end
    :return:
    """
    # connect players - maximum five with break option
    for i in range(1, 5):
        client_mac, client_port = s.accept()
        if client:
            name = client_mac.recv(1024)
            database[name] = [client_mac, 0]
            player_list[i] = True
            check_game_button(database)
        else:
            break
    # send each player a 'start' message
    for player in database:
        database.get(player)[0].send(START)


def check_game_button(player_dict):
    """
    check if game_button was pressed
    :return: True
    """
    if game_button() is True:
        reset_game(player_dict)
        return True


def reset_game(player_dict):
    """
    be called (1) after configure_connections or (2) after the game if reset button pressed.
    1. initialize lights in catcher
    2. resets the database status for players
    :return: returns the database dictionary with reset status
    """
    for player in player_dict:
        set_database(player_dict, player, 0)


def int_from_bytes(binary_data):
    """
    :param binary_data: data in binary format
    :return: given data in int form
    """
    return int.from_bytes(binary_data, byteorder='big', signed=True)


def int_to_bytes(number: int) -> bytes:
    """
    :param number: int data
    :return: given int data in binary format
    """
    return number.to_bytes(length=(8 + (number + (number < 0)).bit_length()) // 8, byteorder='big', signed=True)


def check_game_end():
    """
    check if all players are caught, True is returned if so
    :return: bool
    """
    for player in database:
        if database[player][1] == 0:
            return False
    else:
        return True


def game_loop():
    """
    1. calculates "is caught"
    2. sends message and verify receiving
    3. updates my own database
    *checks for game_end() and end loop if so, wait for game_button() to be pressed -> start game again.
    :return:
    """
    while game_button() and check_game_end():
        # check if player is caught
        is_caught()
        # wait 0.3 sec before rerunning loop
        time.sleep(0.3)


# game loop
try:
    # set up in order for the game to function properly connection set up
    configure_connections()
    # checks if player is caught (via is_caught()) and reacts accordingly while game is played
    game_loop()

except ConnectionError:
    # print("Closing socket")
    s.close()


if __name__ == "__main__":
    configure_connections()
    game_loop()


    # Todo: 21/3/22
    # 1. insert all starting progress to configure_connections() function
    # 2. make option to enter with less than 4 systems
    # 3. create open functions (description in the code)
    # 4. create game_loop.

    # TODO: until 28/3/22
    # 1. check with actual client
    # 2. make real game loop.
    # configure connection - נעבור על זה ביחד
    # 3. pass all Constants to Constants file
    # 4. line 43 - change to const.....................***נראה לי שהושלם***
    # limit line 51 loop (מפחד שניתקע שם לנצח)


