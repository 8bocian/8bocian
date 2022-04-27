#  Copyright (c) 2022. Oskar "Bocian" Możdżeń
#  All rights reserved.

import numpy as np
import pygame as pg

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

vec = pg.math.Vector2


class Translator:
    def __init__(self, x, y):
        # pygame (x, y) coordinates that indicate real (0, 0) coordinates
        self.x = x
        self.y = y

    def translateToPygame(self, point):
        # translate from real system where (0, 0) is at the center of screen to pygame system where (0, 0) is in the top left corner
        new_x = point[0] + self.x
        new_y = abs(point[1] - self.y)
        return vec(new_x, new_y)

    def translateToReal(self, point):
        # translate from pygame system where (0, 0) is in the top left corner to real system where (0, 0) is at the center of screen
        new_x = point[0] - self.x
        new_y = -(point[1] - self.y)
        return vec(new_x, new_y)


class Segment:
    def __init__(self, length, angle, trans):
        self.length = length
        self.angle = angle
        self.trans = trans
        self.end = None
        self.getEnd()

    def getEnd(self, offset_point=(0, 0)):
        # calculate (x, y) end point of the segment
        x = self.length * np.cos(self.angle) + offset_point[0]
        y = self.length * np.sin(self.angle) + offset_point[1]
        self.end = vec(x, y)

    def draw(self, screen, start=(0, 0)):
        pygame_start = self.trans.translateToPygame(start)
        pygame_end = self.trans.translateToPygame(self.end)
        pg.draw.line(screen, GREEN, pygame_start, pygame_end, 1)


class Leg:
    def __init__(self, l1, a1, l2, a2, trans, display):
        self.seg1 = Segment(l1, a1, trans)
        self.seg2 = Segment(l2, a2, trans)
        self.trans = trans
        self.screen = display
        self.total_length = l1 + l2

    def move(self, target=None):
        if target is None:
            target = self.trans.translateToReal(pg.mouse.get_pos())
        else:
            target = self.trans.translateToReal(target)

        if self.total_length >= getLength(target):
            # if target is inside the range of motion of the segment then point towards the target

            seg1_angle_theta = getThetaAngle(target)
            seg1_angle_cos = getAlphaCos(self.seg1.length, self.seg2.length, getLength(target))

            self.seg1.angle = seg1_angle_theta + seg1_angle_cos
            self.seg1.getEnd()

            n_target = target - self.seg1.end
            self.seg2.angle = getThetaAngle(n_target)
        else:
            # if target is outside the range of motion of the segment then point towards the target
            self.seg1.angle = getThetaAngle(target)
            self.seg2.angle = self.seg1.angle

        return self.seg1.angle, self.seg2.angle

    def show(self, bounds=False):
        # draw circle that indicates the range of motion for whole leg
        if bounds:
            center = (self.trans.x, self.trans.y)
            pg.draw.circle(self.screen, RED, center, 1)
            pg.draw.circle(self.screen, RED, center, self.total_length, 1)

        # calculate end of every segment and draw it at the end of the previous segment
        self.seg1.getEnd()
        self.seg1.draw(self.screen)
        self.seg2.getEnd(self.seg1.end)
        self.seg2.draw(self.screen, self.seg1.end)


def getThetaAngle(point):
    # calculate angle to target position
    x = point[0]
    y = point[1]
    radians = np.arctan2(y, x)
    return radians


def getLength(point):
    # calculate length of segment
    x2 = point[0] ** 2
    y2 = point[1] ** 2
    length = np.sqrt(x2 + y2)
    return length


def getAlphaCos(a, b, c):
    # calculate angle
    cosineA = (b ** 2 - a ** 2 - c ** 2) / (-2 * a * c)
    radians = np.arccos(cosineA)
    return radians
