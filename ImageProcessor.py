#import cv2
from PIL import Image
# from pupil_apriltags import Detector
# from time import sleep
# from picamera import PiCamera
from numpy import tan

class TagReader:
    def __init__(self):
        # margin is the odd we got the tag in the image
        #todo: change the margin?
        self.TAG_MARGIN = 5
        self.TAG_DISTANCE = 1
        self.PATH_TO_IMAGES = "/temp_image.jpg"
        # self.TAG_DETECTOR = Detector("tag16h5")
        self.WIDTH_OF_IMAGE = 2592
        self.HEIGHT_OF_IMAGE = 1944
        self.VERTICAL_FIELD_OF_VIEW = 48.8
        self.HORIZONTAL_FIELD_OF_VIEW = 62.2
        # self.camera = PiCamera()
        # self.camera.resolution = (self.WIDTH_OF_IMAGE, self.HEIGHT_OF_IMAGE)


    def refrash_image(self)-> None:
        '''
        Refrash the image
        :return: True if the image was refrashed
        '''
        self.camera.start_preview()
        # sleep(2) # Camera warm-up time
        # self.camera.capture(PATH_TO_IMAGES ,use_video_port=True)
        self.camera.stop_preview()

    def calc_tag_distance(self , det):
        '''
        Calculates the size of the tag in the image
        :param det: detection of the tag
        :return: the distance from the tag
        '''
        #todo: add the calculation of the angles
        h_left = det[0][1] - det[3][1]
        theta1_left = 0
        theta2_left = 0
        d_left = h_left / (tan(theta1_left+theta2_left) - tan(theta1_left))
        
        h_right = det[1][1] - det[2][1]
        theta1_right = 0
        theta2_right = 0
        d_right = h_right / (tan(theta1_right+theta2_right) - tan(theta1_right))
        
        return (d_right + d_left) / 2

    def return_data(self, max_tags_in_game = 5) -> list:
        '''
        Returns a tuple of the form (tag_id, tag_position) of the biggest tag in the image.
        :param image: the image to be analyzed
        :param max_tags_in_game: the maximum number of tags in the game
        :return: a dictionary with the tag_id and tag_position of all the images with a margin + possibility
        '''
        data_list = []
        self.refrash_image()
        # image = cv2.imread(self.PATH_TO_IMAGES, cv2.IMREAD_GRAYSCALE)
        # dets = self.TAG_DETECTOR.detect(image)

        # for det in dets:
        #     if det.tag_id <= max_tags_in_game and det.decision_margin > self.TAG_MARGIN:
        #         det_dist = self.calc_tag_distance(det)
        #         det_dist = None
        #         if det_dist > self.TAG_DISTANCE:
        #             data_list.append((det.tag_id, det_dist))
        return data_list

if __name__ == "__main__":
    print("reads tags")
    scanner = TagReader()
    det_dict = scanner.return_data(5)
    for tup in det_dict:
        print(tup)
    print("done")
