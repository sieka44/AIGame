import math

import numpy
import numpy as np
import pygame as pg


class CollisionCircle:

    def __init__(self, x, y, radius, colour, rotation=0.0, velocity=10):
        self._position = np.array([float(x), float(y)])
        self._radius = int(radius)
        self._angle = rotation
        self._mass = (radius / 10.0) * 2
        self._colour = colour
        self._velocity = np.array([velocity, velocity])
        self._angular_velocity = 0
        self._delta = 0

    def draw(self, window):
        pg.draw.circle(window, self._colour, self._position.astype(np.int),
                       self._radius)

    def update(self, delta):
        self._angle += self._angular_velocity * (delta / 1000)
        self._position += self._velocity * (delta / 1000)
        self._delta += delta

    def get_position(self):
        return self._position

    def get_radius(self):
        return self._radius

    def set_velocity(self, velocity):
        self._velocity = velocity

    def get_velocity(self):
        return self._velocity

    def set_angular_velocity(self, angular_velocity):
        self._angular_velocity = angular_velocity

    def get_angular_velocity(self):
        return self._angular_velocity

    def get_mass(self):
        return self._mass

    def get_delta(self):
        return self._delta

    def set_delta(self, delta):
        self._delta = delta
