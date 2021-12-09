"""
    This file is the main py file in the image process module
    The main goal of the file is the get an image from CameraManager file and detect whether a catch occurred or not.
"""

import time
from typing import *
from ImageProcess import CameraManager

MAX_DISTANCE_CATCH = 1.5
PACE = 0.25

class ImageProcessor:
    def __init__(self, camera: CameraManager):
        """
        initialize an instance of an image processor
        :type camera: the camera manager that gives us images
        """
        self.camera = camera

    def processConstantly(self) -> None:
        """
        this function operates the camera and makes it shoot constantly and then process the images
        :return: None
        """
        while True:
            # todo - insert quit condition
            time.sleep (PACE)
            image = self.camera.singleShoot()
            self.catchFromImage(image)

    def catchFromImage(self, image) -> Tuple[bool,object]:
        #todo - what type is object?
        #todo - define Image class?
        """
        This is the main function that is supposed to notify if the player caught
        :param image: the image that needs to be processed
        :return: Tuple - the first item is a boolean that indicates whether the player caught another player or not
        the second item is the id of the player that has been caught.
        """
        if self.isThereCatch():
            id = self.getCaughtPlayer()
            return (True, id)
        return (False, None) #or id.None

    def isThereCatch(self) -> bool:
        """
        This function needs to check if a the player caught someone or not
        :return: boolean - True - if another player has been caught, False - otherwise
        """
        if self.isThereFiducial():
            if self.getFiducialDistance() <= MAX_DISTANCE_CATCH:
                return True
        return False

    def isThereFiducial(self) -> bool:
        """
        This function needs to check if a there is a fiducial marker in the image
        :return: boolean - True - if there is another fiducial, False - otherwise
        """
        pass

    def getFiducialDistance(self) -> float:
        """
        calculates the distance from us to the fiducial that we found
        :return: the distance
        """
        pass

    def getCaughtPlayer(self):
        #todo - define return value (id)
        """
        get from known list of players and fiducials who is the player that we caught
        :return: the id of the player that we caught
        """
        pass