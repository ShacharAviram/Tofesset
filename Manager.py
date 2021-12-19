"""
    This file is the overall manager of the device. it contains the player status and controls the actions in the game.
"""
import Client
import ImageProcessor
import Indicator
import time


class Manager:
    def __init__(self):
        """
        initialize an instance of a project manager
        contains player's status
        """
        self.mode = None  # Am I a catcher or a player?  0 - free player, 1 - catcher, 2 - caught player
        self.imageprocessor = None  # If I am a catcher
        self.indicator = None
        self.client = Client()

        #TODO: init_for_player(connection, indications, status)

        #TODO: init for catch(connection, indication, status)

        pass

    def init_connection(self):
        """
        Make the first connection and update the mode
        :return: None
        """
        Client.client.connect()
        self.mode = self.Client.check_if_received_return()


    def init_camera_manager(self):
        """
        Create an Image processor class for the catcher
        :return: None
        """
        self.imageprocessor = ImageProcessor.ImageProcess()


    def init_indicator(self, role):
        """
        Create an Indicator class for each player
        :param role:
        :return: None
        """
        self.indicator = Indicator.Indicator()
        self.indicator.indicate(role)

    def begin_game(self):
        """
        Begin the game and call the relevant functions
        :return:
        """
        self.init_connection()
        self.init_indicator(self.mode)

        if self.mode == 1:
            self.init_camera_manager()

        if self.mode == 0:
            self.main_loop_player()
        elif self.mode == 1:
            self.main_loop_catcher()
        else:
            print('the player is suspended')

    def main_loop_catcher(self):
        """
        1. check for updates from server
        2. check if There is a catch (ImageProcessor) (catch from image)
        3. send to server (if needed)
        4. get verification
        :return: None
        """
        while self.client.is_game_started:
            self.client.check_if_received_return()
            if self.imageprocessor.catchFromImage()[0] is True:
                message = self.imageprocessor.catchFromImage()[1]
                self.client.send_message(bytes('{}message'.format(message)))  # TODO: check message format
            time.sleep(0.3)

    def main_loop_player(self):
        """
        1. check for updates from server
        2. process message
        3. change indication
        :return: None
        """
        while self.client.is_game_started:
            # self.check_connection()
            self.client.status = self.client.check_if_received_return()  # TODO: check message format
            time.sleep(0.3)

