# Game Rules - easy to change! (ensure change on all systems)
CATCH_DISTANCE = 150
KNOCK_OUT_TIME = 8 # (IN SECONDS)
IMAGES_TO_CATCH = 9


# GPIO PINS
#RED_PIN = 16
#GREEN_PIN = 17
#BLUE_PIN = 15
LED_STRIP_PIN = 18
SWITCH_PIN = 27
BUTTON_PIN = 7
CATCHER_PINS = [1, 2, 3, 4]
AUDIO_PIN = 14

# LED COTROL
NUM_OF_PIXELS = 10
COLOR_DICT = {"off":(0,0,0),"red":(255,0,0),"green":(0,255,0),"blue":(0,0,255),
              "yellow":(255,255,0),"violet":(255,0,255),"turquoise":(0,255,255), "orange":(255,50,0)}
PLAYER_LED_LIST = [4, 6, 8, 10, None]

# General Constants
PLAYER_FREE = 10
START = 11
PLAYER_CAUGHT = 12  # for player and server use
PLAYER_STATUSES = [PLAYER_FREE, PLAYER_CAUGHT]

# Communication
SERVER_MAC = 'B8:27:EB:E1:D1:A2'
COMMUNICATION_PORT = 5
BUFFER_SIZE = 128

# Systems IDs
ID_1 = 0
ID_2 = 1
ID_3 = 2
ID_4 = 3
#ID_5 = 4 #not in use
#ID_6 = 5 #not in use

# system ID list
ID_LIST = [ID_1, ID_2, ID_3, ID_4]

# Game Modes
CATCH_EM_ALL = 333
RISE_OF_THE_DEAD = 444
GAME_MODES = [CATCH_EM_ALL, RISE_OF_THE_DEAD]
SERVER_DOWN = 404


#logs
DESKTOP_DIR_CONST = "/home/pi/Desktop/"