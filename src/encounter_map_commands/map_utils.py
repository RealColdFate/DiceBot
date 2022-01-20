from urllib.request import urlopen

import cv2 as cv
import numpy as np

from src.encounter_map_commands.color_map import BGR_STRING_MAP
from src.encounter_map_commands.map_entity import UNIT_SIZE

DEFAULT_RESIZE_WIDTH = UNIT_SIZE
DEFAULT_RESIZE_HEIGHT = UNIT_SIZE
CURRENT_IMAGE_PATH = '../../data/current-image.png'


def draw_lines(canvas, width, height, line_thickness=1, line_color=BGR_STRING_MAP['grey']):
    for i in range(len(canvas)):
        if i % height == 0:
            for p in range(line_thickness):
                canvas[i + p][0:-1] = line_color
        for j in range(len(canvas[i])):
            if j % width == 0:
                for p in range(line_thickness):
                    canvas[i][j + p] = line_color


# resizes the image in proportion to the unit size based on the width and height given
def resize_map(canvas, width=DEFAULT_RESIZE_WIDTH, height=DEFAULT_RESIZE_HEIGHT):
    return cv.resize(canvas, (width * UNIT_SIZE + 1, height * UNIT_SIZE + 1), interpolation=cv.INTER_CUBIC)


def draw_on_map(canvas, image, x, y):
    for i in range(len(image)):
        for j in range(len(image[i])):
            if len(canvas) > i + y > -1 and len(canvas[i + y]) > j + x > -1:
                canvas[i + y][j + x] = image[i][j]


def draw_entities(blank_canvas, entities):
    for e in entities:
        draw_on_map(blank_canvas, e.icon, e.get_x(), e.get_y())


def url_to_image(image_url):
    req = urlopen(image_url)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    return cv.imdecode(arr, 1)  # 'Load image as np array of shape (height, width, 3)'
