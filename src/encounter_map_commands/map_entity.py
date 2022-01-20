from cv2 import INTER_CUBIC
from cv2 import resize

UNIT_SIZE = 50


class MapEntity:
    def __init__(self, name, x, y, icon, outline_color, board_height):
        self.name = name
        self.board_height = board_height
        self.x = x - 1
        self.y = y
        self.y = board_height - self.y # to convert from matrix indices to cartesian cords
        self.icon = resize(icon, (UNIT_SIZE, UNIT_SIZE), INTER_CUBIC)

        # set the outline of the icon to the outline color for visibility purposes
        for i in range(len(self.icon)):
            for j in range(len(self.icon[i])):
                if i != 0 and i != len(self.icon) - 1 and j != 0 and j != len(self.icon[i]) - 1:
                    continue
                else:
                    self.icon[i][j] = outline_color

    # adjusts the coordinates of the entity
    def move(self, x_units, y_units):
        self.x += x_units
        self.y -= y_units

    def get_x(self):
        return self.x * UNIT_SIZE

    def get_y(self):
        return self.y * UNIT_SIZE

    def get_cord_string(self):
        return f'({self.x + 1}, {self.board_height - self.y})'
