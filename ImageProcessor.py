import cv2
from PIL import Image
# from TagReader import TagReader
from pupil_apriltags import Detector
from math import sin, radians
# todo: import picamara
from time import sleep


# from picamera import PiCamera


class TagReader:
    def __init__(self):
        # margin is the odd we got the tag in the image
        # todo: change the margin
        self.TAG_MARGIN = 5
        self.TAG_DISTANCE = 100
        # todo: change the path to the images
        # self.PATH_TO_IMAGES = "/tmp/curr_image"
        self.PATH_TO_IMAGES = "/tmp/curr_image.jpg"
        self.TAG_DETECTOR = Detector("tag16h5")
        self.WIDTH_OF_IMAGE = 3280
        self.HEIGHT_OF_IMAGE = 2464
        self.VERTICAL_FIELD_OF_VIEW = 48.8
        self.HORIZONTAL_FIELD_OF_VIEW = 62.2
        self.SIZE_CONST = 18
        # self.CAMERA = PiCamera()
        # self.CAMERA.resolution = (self.WIDTH_OF_IMAGE, self.HEIGHT_OF_IMAGE)
        #self.CAMERA.start_preview()


    def refrash_image(self) -> None:
        '''
        Refrash the image
        :return: True if the image was refrashed
        '''
        # todo: create the object in the __init__
        '''
        camera.capture(self.PATH_TO_IMAGES)
        '''

    def calc_tag_distance(self, det):
        '''
        Calculates the size of the tag in the image
        :param det: detection of the tag
        :return: the distance of the tag
        '''
        l_l_h = det[0][1] - det[3][1]
        l_r_h = det[1][1] - det[2][1]
        l_b_w = det[1][0] - det[0][0]
        l_t_w = det[2][0] - det[3][0]
        left_teta_1 = l_l_h / self.HEIGHT_OF_IMAGE * self.VERTICAL_FIELD_OF_VIEW * 2
        right_teta_1 = l_r_h / self.HEIGHT_OF_IMAGE * self.VERTICAL_FIELD_OF_VIEW * 2
        buttom_teta_1 = l_b_w / self.WIDTH_OF_IMAGE * self.HORIZONTAL_FIELD_OF_VIEW * 2
        top_teta_1 = l_t_w / self.WIDTH_OF_IMAGE * self.HORIZONTAL_FIELD_OF_VIEW * 2
        average_teta_base = (buttom_teta_1 + top_teta_1) / 2
        average_teta_sides = (left_teta_1 + right_teta_1) / 2
        sin_teta = sin(radians(average_teta_sides))

        return self.SIZE_CONST / sin_teta

    def set_image_path(self, path):
        self.PATH_TO_IMAGES = path

    def return_data(self, max_tags_in_game=5) -> list:
        '''
        Returns a tuple of the form (tag_id, tag_position) of the biggest tag in the image.
        :param image: the image to be analyzed
        :param max_tags_in_game: the maximum number of tags in the game
        :return: a dictionary with the tag_id and tag_position of all the images with a margin + possibility
        '''
        data_list = []
        self.refrash_image()
        image = cv2.imread(self.PATH_TO_IMAGES, cv2.IMREAD_GRAYSCALE)
        dets = self.TAG_DETECTOR.detect(image)

        for det in dets:
            if det.tag_id <= max_tags_in_game and det.decision_margin > self.TAG_MARGIN:
                det_dist = self.calc_tag_distance(det.corners)
                if det_dist < self.TAG_DISTANCE:
                    data_list.append((det.tag_id, det_dist))
        return data_list


if __name__ == "__main__":
    print("reads tags")
    scanner = TagReader()
    det_list = scanner.return_data(5)
    for tup in det_list:
        print(tup)
    print("done")
