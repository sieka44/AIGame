import math
import random

import pygame as pg
from numpy import array as Vector

from collision_circle import CollisionCircle
from collision_handler import CircleCollisionHandler
from player import Player
from bot import Bot
from stable_object import StableObject

BACKGROUND_COLOUR = (0, 0, 0)
WINDOW_SIZE_X = 800
WINDOW_SIZE_Y = 800
DEFAULT_BOT_COUNT = 15
DEFAULT_OBJECT_COUNT = 3
DEFAULT_BALL_COLOUR = (45, 173, 60)
DEFAULT_INERTIA = 1.
DEFAULT_BOT_SIZE = 10
DEFAULT_USER_SIZE = 25
VISIBLE_FPS = False


def spawn_bots(no_of_balls):
    bots = []
    i = 0
    while i < no_of_balls:
        radius = DEFAULT_BOT_SIZE
        x = random.randrange(radius + 5, WINDOW_SIZE_X - radius - 5)
        y = random.randrange(radius + 5, WINDOW_SIZE_Y - radius - 5)
        b = Bot(x, y, DEFAULT_BOT_SIZE, stable_objects)
        b.set_delta(x)
        if CircleCollisionHandler.detect_any_collision(bots, b):
            i -= 1
        else:
            bots.append(b)
        i += 1
    return bots


def spawn_additional_bots(position):
    bot = Bot(position[0], position[1], DEFAULT_BOT_SIZE, stable_objects)
    return bot


def spawn_user(position):
    p = Player(position[0], position[1], DEFAULT_USER_SIZE)
    p.set_velocity(0)
    return p


def spawn_stable_objects(no_of_objects):
    obj = []
    i = 0
    while i < no_of_objects:
        radius = random.uniform(40, 60)
        x = random.randrange(WINDOW_SIZE_X * 0.4, WINDOW_SIZE_X * 0.6)
        y = random.randrange(WINDOW_SIZE_Y * 0.4, WINDOW_SIZE_Y * 0.6)
        x += WINDOW_SIZE_X / 6 if x > WINDOW_SIZE_X / 2 else -WINDOW_SIZE_X / 6
        y += WINDOW_SIZE_Y / 6 if y > WINDOW_SIZE_Y / 2 else -WINDOW_SIZE_Y / 6
        b = StableObject(x, y, radius, user.get_position())
        if CircleCollisionHandler.detect_any_collision(obj, b):
            i -= 1
        else:
            obj.append(b)
        i += 1
    return obj


def calculate_ray(player_position, m_position):
    dx = player_position[0] - m_position[0]
    dy = player_position[1] - m_position[1]

    reversed_sign_x = 1 if dx < 0 else -1
    slope = dy / dx if dx != 0 else 1
    x_new = reversed_sign_x * WINDOW_SIZE_X
    y_new = player_position[1] + slope * (x_new - player_position[0])

    return x_new, y_new


if __name__ == "__main__":
    random.seed()
    pg.init()

    window = pg.display.set_mode((WINDOW_SIZE_X, WINDOW_SIZE_Y))

    pg.display.set_caption("AI Game 2D")

    previous_time = pg.time.get_ticks()
    user = spawn_user((WINDOW_SIZE_X / 2, WINDOW_SIZE_Y / 2))
    stable_objects = spawn_stable_objects(DEFAULT_OBJECT_COUNT)
    bots = spawn_bots(DEFAULT_BOT_COUNT)
    user.set_stable_objects(stable_objects)
    collision_handler = CircleCollisionHandler((WINDOW_SIZE_X, WINDOW_SIZE_Y), DEFAULT_INERTIA)

    new_bot_position = None
    mouse_position = (0, 0)
    should_run = True

    while should_run:
        window.fill(BACKGROUND_COLOUR)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                should_run = False
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                new_bot_position = Vector(event.pos)
            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                if new_bot_position is not None:
                    new_bot_velocity = Vector(event.pos) - new_bot_position
                    bots.append(spawn_additional_bots(new_bot_position))
                    new_bot_position = None

        mouse_position = calculate_ray(user.get_position(), pg.mouse.get_pos())
        current_time = pg.time.get_ticks()
        dt = float(current_time - previous_time)
        previous_time = current_time

        collision_handler.handle_boundaries(bots)
        collision_handler.handle_collisions(bots)
        collision_handler.handle_stable_objects(bots, stable_objects)

        if collision_handler.detect_any_collision(bots, user):
            should_run = False
        for o in stable_objects:
            o.handle_group_attack(bots, user.get_position())
            o.draw(window)
            o.update(dt)

        for b in bots:
            b.draw(window)
            b.update(dt)
            b.adapt_to_state()
        user.draw_with_laser(window, mouse_position)
        pg.display.update()
        if VISIBLE_FPS and dt > 0.0:
            print(1.0 / dt)
