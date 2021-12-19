"""
    This file is the overall manager of the device. it contains the player status and controls the actions in the game.
"""


class Manager:
    def __init__(self):
        """
        initialize an instance of an project manager
        contains player's status
        """
        self.transmitter = Transmitter
        self.reciever = Reciever
        self.cameramanager = CameraManager
        self.indicator = Indicator
        pass

