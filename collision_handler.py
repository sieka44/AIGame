import numpy as np


class CollisionHandler:

    def __init__(self, bound_size):
        self._width = bound_size[0]
        self._height = bound_size[1]

    def handle_boundaries(self, objects):
        raise NotImplementedError()

    @staticmethod
    def detect_any_collision(objects, subject):
        raise NotImplementedError()

    @staticmethod
    def _detect_pair_collision(a, b):
        raise NotImplementedError()


class CircleCollisionHandler(CollisionHandler):

    def __init__(self, bound_size, restitution):
        CollisionHandler.__init__(self, bound_size)
        self._restitution = restitution

    def handle_boundaries(self, objects):
        for o in objects:
            r = o.get_radius()
            vel = o.get_velocity()
            pos = o.get_position()
            if pos[0] <= r or pos[0] >= (self._width - r):
                vel[0] *= -1
                pos[0] = max(r, min(self._width - r, pos[0]))
            if pos[1] <= r or pos[1] >= (self._height - r):
                vel[1] *= -1
                pos[1] = max(r, min(self._height - r, pos[1]))
            o.set_velocity(vel)

    def handle_collisions(self, objects):
        for i in range(len(objects)):
            a = objects[i]
            for j in range(i + 1, len(objects)):
                b = objects[j]
                if CircleCollisionHandler._detect_pair_collision(a, b):
                    col_normal = a.get_position() - b.get_position()
                    col_normal /= np.linalg.norm(col_normal)

                    if np.dot(col_normal, a.get_velocity() - b.get_velocity()) >= 0.0:
                        continue

                    J = a.get_mass() * b.get_mass() * (self._restitution + 1.0) / (a.get_mass() + b.get_mass())
                    J *= np.dot(a.get_velocity() - b.get_velocity(), col_normal)

                    u1 = a.get_velocity() - (J / a.get_mass()) * col_normal
                    u2 = b.get_velocity() + (J / b.get_mass()) * col_normal

                    a.set_velocity(u1)
                    b.set_velocity(u2)

    def handle_stable_objects(self, bots, objects):
        for b in bots:
            for o in objects:
                if CircleCollisionHandler._detect_pair_collision(b, o):
                    col_normal = b.get_position() - o.get_position()
                    col_normal /= np.linalg.norm(col_normal)

                    if np.dot(col_normal, b.get_velocity() - o.get_velocity()) >= 0.0:
                        continue
                    J = b.get_mass() * o.get_mass() * (self._restitution + 1.0) / (b.get_mass() + o.get_mass())
                    J *= np.dot(b.get_velocity() - o.get_velocity(), col_normal)

                    u1 = b.get_velocity() - (J / b.get_mass()) * col_normal

                    b.set_velocity(u1)

    @staticmethod
    def is_in_area(a, sub_pos, sub_r):
        return True if np.sqrt(np.sum((a.get_position() - sub_pos) ** 2)) <= (a.get_radius() + sub_r) \
            else False

    @staticmethod
    def detect_any_collision(objects, subject):
        for o in objects:
            if CircleCollisionHandler._detect_pair_collision(o, subject):
                return True
        else:
            return False

    @staticmethod
    def _detect_pair_collision(a, b):
        return True if np.sqrt(np.sum((a.get_position() - b.get_position()) ** 2)) <= (a.get_radius() + b.get_radius()) \
            else False
