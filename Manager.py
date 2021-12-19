"""
    This file is the overall manager of the device. it contains the player status and controls the actions in the game.
"""


class Manager:
    def __init__(self):
        """
        initialize an instance of an project manager
        contains player's status
        """
        self.mode = '' #am i a catcher or a player?
        self.cameramanager = None #if i am a catcher
        self.indicator = None

        #TODO: init_for_player(connection, indications, status)

        #TODO: init for catch(connection, indication, status)

        pass

    def init_connection(self):
        """
        set connection to server,

        :return:
        """
        pass

    def init_camera_manager(self):

        pass

    def init_indicator(self, role):

        pass

    def main_loop_catcher(self):
        """
        1. check for updates from server
        2. check if There is a catch (ImageProccessor) (catch from image)
        3. send to server (if needed)
        4. get verification
        :return:
        """

    def main_loop_player(self):
        """
        1. check for updates from server
        2. process message
        3. change indication
        :return:
        """

