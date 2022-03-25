import socket
import bluetooth
import time
from ImageProcess.ImageProcessor import ImageProcessor
from Constants import *
from IndicationAndExperience.Indicator_catcher_API import Indicator



hostMACAddress = '8c:c8:4b:80:50:42'  # The MAC address of a Bluetooth adapter on the server.
port = 5
backlog = 4  # number of devices we can connect to (can be changed)
size = 1024


s = bluetooth.BluetoothSocket()
s.bind((hostMACAddress, port))
s.listen(backlog)


# Current player status data structure
database = dict()
# connection list of players (client1, client2, client3, client4)
player_list = [False, False, False, False]


def get_player_address(dictionary, player_name):
    """
    :param player_name: the name of the player
    :param dictionary: database of players in game
    :return: mac addresses of given player
    """
    return dictionary[player_name][0]


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
    3. wait for eco from client, else, (after 3 seconds) turn to IndicationAndExperience
    :return: None
    """
    # check if a player is considered caught, send message and wait for validation
    for returned_data in ImageProcessor.ImageProcessor.return_data():
        player_is_caught = returned_data[0]
        if player_is_caught:
            set_database(database, returned_data[1], 1)  # set player status as caught
            # send message to client and find relevant id address
            caught_player_mac_address = get_player_address(database, returned_data[1])
            caught_player_mac_address.send(int_to_bytes(PLAYER_CAUGHT))
            # try to send message for at most 3 whole seconds
            iteration = 0
            while not(client.recv(1024)) and iteration <= 9:
                iteration += 1
                print('waiting for validation')
                client.send(int_to_bytes(PLAYER_CAUGHT))
                print('sent another message')
                time.sleep(0.3)
            # do we want to do something if message wasn't received?
            if iteration == 10:
                # do something in IndicationAndExperience...?
                pass
        else:
            pass


def configure_connections():
    """
    1. set up in order for the game to function properly
    2. connection set up
    3. calls reset_game() in end
    :return: None
    """
    # connect players - maximum four with break option
    while len(database) <= 4 and not(Indicator.Indicator.is_reset_button_pressed()):
        try:
            client_mac, client_port = s.accept()
            name = client_mac.recv(1024)         # receive name from player
            database[name] = [client_mac, 0]     # mac address and starting status
            player_list[len(database)-1] = True  # "len(database)-1" index in list
            check_game_button(database)
        except bluetooth.BluetoothError:
            break
    # send each player a 'start' message
    else:
        for player in database:
            player_address = get_player_address(database, player)
            player_address.send(START)
    # reset player's status
    reset_game(database)

def check_game_button(player_dict):
    """
    :param player_dict: dictionary with player info
    check if reset_game_button was pressed, if so, reset all player's status
    :return: True or None
    """
    if Indicator.Indicator.is_reset_button_pressed() is True:
        reset_game(player_dict)
        return True


def reset_game(player_dict):
    """
    :param player_dict: dictionary with player info
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
    while the reset button isn't presses and the game hasn't ended yet -
    1. calculates "is caught"
        1. checks if player was caught
        2. sends message and verify receiving
        3. updates the database
    2. wait 0.3 seconds
    :return: None
    """
    while not(Indicator.Indicator.is_reset_button_pressed()) and check_game_end():
        # check if player is caught
        is_caught()
        # wait 0.3 sec before rerunning loop
        time.sleep(0.3)


if __name__ == "__main__":
    try:
        # set up in order for the game to function properly connection set up
        configure_connections()
        # checks if player is caught (via is_caught()) and reacts accordingly while game is played
        game_loop()

    except ConnectionError:
        # print("Closing socket")
        s.close()


# Todo: 21/3/22
# 1. insert all starting progress to configure_connections() function
# 2. make option to enter with less than 4 systems
# 3. create open functions (description in the code)
# 4. create game_loop.

# TODO: until 28/3/22
# 1. check with actual client
# 2. make real game loop.......................Done (most of the loop is executed ny is_caught())
# configure connection.........................Done (conformation needed)
# 3. pass all Constants to Constants file......Done (START, PLAYER_CAUGHT)
# 4. line 43 - change to const.................Done (conformation needed)
# limit line 51 loop...........................Done (10 tries, altogether 3 whole seconds)
# line 52 - question towards Geva
