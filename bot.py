import numpy as np
import pygame
import enum
import math
from collision_circle import CollisionCircle
import random

CONST_VELOCITY = 75
COLOUR = (255, 0, 0)
HIDE_TIME = 15000
TICK = 1000


class Behaviour(enum.Enum):
    Explore = 0
    Hide = 1,
    Risk = 2,
    Attack = 3


class Bot(CollisionCircle):

    def __init__(self, x_position, y_position, r, asylums):
        CollisionCircle.__init__(self, x_position, y_position, r, COLOUR, velocity=CONST_VELOCITY)
        self.behavior = Behaviour.Explore
        self.asylums = asylums
        self.safe_areas = asylums.copy()
        self.direction = None
        self.is_visible = False
        self.hide_delta = x_position % 15 * TICK
        random.seed()

    def set_visible(self, is_visible):
        self.is_visible = is_visible

    def rotate_vector_by_angle(self, angle):
        alpha = math.radians(angle)
        self._velocity[0] = self._velocity[0] / self._velocity[0] * CONST_VELOCITY
        self._velocity[1] = self._velocity[1] / self._velocity[1] * CONST_VELOCITY
        new_x = math.cos(alpha) * self._velocity[0] - math.sin(alpha) * self._velocity[1]
        new_y = math.sin(alpha) * self._velocity[0] + math.cos(alpha) * self._velocity[1]
        return np.array([new_x, new_y])

    def adapt_to_state(self):
        if self._delta > TICK:
            if self.behavior == Behaviour.Explore:
                self.explore()
            elif self.behavior == Behaviour.Hide:
                self.hide()
            elif self.behavior == Behaviour.Attack:
                self.attack()
            else:
                self.risk()
            self._delta = 0

    def explore(self):
        random_angle = random.uniform(-180, 180)
        self.hide_delta += self._delta
        self._velocity = self.rotate_vector_by_angle(random_angle)
        if self.hide_delta > HIDE_TIME:
            self.behavior = Behaviour.Hide
            self.hide_delta = 0

    def hide(self):
        if self.hide_delta > HIDE_TIME:
            self.behavior = Behaviour.Risk
        else:
            self.hide_delta += self._delta
        asylum_pos = self.get_nearest_asylum_position() if self.direction is None else self.direction
        n_asylum = self.convert_to_vel_vector(self._position - asylum_pos)
        self._velocity = np.array([CONST_VELOCITY, CONST_VELOCITY])
        self._velocity = self._velocity * n_asylum

    def risk(self):
        self.direction = self.get_nearest_asylum_position()
        self.hide_delta = 0
        self.behavior = Behaviour.Hide

    def attack(self):
        player = self.convert_to_vel_vector(self._position - self.direction)
        self._velocity = np.array([CONST_VELOCITY, CONST_VELOCITY])
        self._velocity = self._velocity * player

    def get_nearest_asylum_position(self):
        min_dist = 1000000
        pos_out = None
        visited_asylum = None
        if len(self.safe_areas) <= 0:
            self.safe_areas = self.asylums.copy()
        for a in self.safe_areas:
            pos = a.get_asylum_point()
            tmp_dist = math.sqrt((pos[0] - self._position[0]) ** 2
                                 + (pos[1] - self._position[1]) ** 2)
            if tmp_dist < min_dist:
                min_dist = tmp_dist
                pos_out = pos
                visited_asylum = a

        self.safe_areas.remove(visited_asylum)
        self.direction = pos_out
        return pos_out if pos_out is not None else (1, 1)

    def convert_to_vel_vector(self, vector):
        vector[0] = vector[0] / vector[0] * 1 if vector[0] > 0 else -1
        vector[1] = vector[1] / vector[1] * 1 if vector[1] > 0 else -1
        return -vector
