import numpy
import pygame as pg
from collision_circle import CollisionCircle

CONST_VELOCITY = 1
COLOUR = (0, 255, 0)
RAY_SIZE = 4


class Player(CollisionCircle):
    def __init__(self, x_position, y_position, r):
        CollisionCircle.__init__(self, x_position, y_position, r, COLOUR, CONST_VELOCITY)
        self.stable_objects = None

    def update(self, delta):
        self._delta += delta

    def draw_with_laser(self, window, mouse_position):
        self.draw(window)
        pg.draw.line(window, COLOUR, self._position, mouse_position, RAY_SIZE)

    def lenght(self, vector):
        le = vector[0] ** 2 + vector[1] ** 2
        return numpy.np.math.sqrt(le)

    def set_stable_objects(self, objects):
        self.stable_objects = objects
