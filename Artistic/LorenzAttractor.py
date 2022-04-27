#  Copyright (c) 2022. Oskar "Bocian" Możdżeń
#  All rights reserved.

import colorsys
from math import sin, cos
import numpy as np
import pygame as pg
import ctypes

def run():
    # only calculate 1500 iterations to maintain good performance
    stop = 1500
    user32 = ctypes.windll.user32
    WIDTH = user32.GetSystemMetrics(78)
    HEIGHT = user32.GetSystemMetrics(79)
    BLACK = (0, 0, 0)
    FPS = 30

    x = 0.01
    y = 0.01
    z = 0.01

    # those are values that don't cause the equation to tend to infinity
    sigma = 10
    rho = 28
    beta = 8 / 3

    angle = 0
    points = [[[0], [0], [0]]]
    scale = 15


    def hsv2rgb(h, s, v):
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()

    projection_matrix = np.matrix([
        [1, 0, 0],
        [0, 1, 0]
    ])

    while len(points) <= stop:
        clock.tick(FPS)
        screen.fill(BLACK)

        sin_a = sin(angle)
        cos_a = cos(angle)

        rotation_matrix_x = np.matrix([
            [1, 0, 0],
            [0, cos_a, -sin_a],
            [0, sin_a, cos_a]
        ])
        rotation_matrix_y = np.matrix([
            [cos_a, 0, sin_a],
            [0, 1, 0],
            [-sin_a, 0, cos_a],
        ])
        rotation_matrix_z = np.matrix([
            [cos_a, -sin_a, 0],
            [sin_a, cos_a, 0],
            [0, 0, 1]
        ])

        angle += 0.01
        hue = 0

        if len(points) <= stop:
            dt = 0.01

            dx = (sigma * (y - x)) * dt
            dy = (x * (rho - z) - y) * dt
            dz = (x * y - beta * z) * dt

            x = x + dx
            y = y + dy
            z = z + dz

            point = [[x], [y], [z]]
            points.append(point)

        for p_i, p in enumerate(points[:-1]):
            rotated_2d = np.dot(rotation_matrix_y, p)
            projected2d = np.dot(projection_matrix, rotated_2d)
            x1_pos = int(projected2d[0][0] * scale) + WIDTH // 2
            y1_pos = int(projected2d[1][0] * scale) + HEIGHT // 2

            rotated_2d = np.dot(rotation_matrix_y, points[p_i + 1])
            projected2d = np.dot(projection_matrix, rotated_2d)
            x2_pos = int(projected2d[0][0] * scale) + WIDTH // 2
            y2_pos = int(projected2d[1][0] * scale) + HEIGHT // 2

            if hue > 1:
                hue = 0

            pg.draw.line(screen, (hsv2rgb(hue, 1, 1)), (x1_pos, y1_pos), (x2_pos, y2_pos), 3)
            hue += 0.004

        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

if __name__ == "__main__":
    while 1:
        run()
