import numpy as np
import pygame as pg
from collision_circle import CollisionCircle

COLOUR = (255, 255, 255)


class StableObject(CollisionCircle):
    def __init__(self, x_position, y_position, r, center_point):
        CollisionCircle.__init__(self, x_position, y_position, r, COLOUR, 0)
        self.asylum = self.calculate_asylum(center_point)

    def calculate_asylum(self, center):
        vector = self._position - center
        vector[0] = vector[0] / vector[0] * 1 if vector[0] > 0 else -1
        vector[1] = vector[1] / vector[1] * 1 if vector[1] > 0 else -1
        return self._position + (vector * 2 * self._radius)

    def get_asylum_point(self):
        return self.asylum

    def draw(self, window):
        pg.draw.circle(window, self._colour, self._position.astype(np.int),
                       self._radius)
        pg.draw.circle(window, self._colour, self.asylum.astype(np.int), 5)

    def update(self, delta):
        pass
