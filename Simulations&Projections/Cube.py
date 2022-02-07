#  Copyright (c) 2022. Oskar "Bocian" Możdżeń
#  All rights reserved.

from math import cos, sin
import pygame as pg
import numpy as np


class Cube:
    def __init__(self, screen, position):
        self.scale = 100
        self.screen = screen
        self.rotation_matrix_z = None
        self.rotation_matrix_y = None
        self.rotation_matrix_x = None
        self.angle = 0
        self.position = position
        self.points = np.array([
            [[-1], [-1], [1]],
            [[1], [-1], [1]],
            [[1], [1], [1]],
            [[-1], [1], [1]],
            [[-1], [-1], [-1]],
            [[1], [-1], [-1]],
            [[1], [1], [-1]],
            [[-1], [1], [-1]]
        ])

        self.projection_matrix = np.matrix([
            [1, 0, 0],
            [0, 1, 0]
        ])

        self.projected_points = [
            [n, n] for n, _ in enumerate(self.points)
        ]

    @staticmethod
    def __connect_points(i, j, points, screen):
        pg.draw.line(screen, WHITE, (points[i][0], points[i][1]), (points[j][0], points[j][1]))

    def project_cube(self):
        cos_a = cos(self.angle)
        sin_a = sin(self.angle)
        self.rotation_matrix_x = np.matrix([
            [1, 0, 0],
            [0, cos_a, -sin_a],
            [0, sin_a, cos_a]
        ])
        self.rotation_matrix_y = np.matrix([
            [cos_a, 0, sin_a],
            [0, 1, 0],
            [-sin_a, 0, cos_a],
        ])
        self.rotation_matrix_z = np.matrix([
            [cos_a, -sin_a, 0],
            [sin_a, cos_a, 0],
            [0, 0, 1]
        ])
        self.angle += 0.01

        for i, point in enumerate(self.points):
            rotated2d = np.dot(self.rotation_matrix_x, point)
            rotated2d = np.dot(self.rotation_matrix_y, rotated2d)
            rotated2d = np.dot(self.rotation_matrix_z, rotated2d)
            projected2d = np.dot(self.projection_matrix, rotated2d)

            x = int(projected2d[0][0] * self.scale) + self.position[0]
            y = int(projected2d[1][0] * self.scale) + self.position[1]

            self.projected_points[i] = [x, y]

        for p in range(4):
            self.__connect_points(p, (p + 1) % 4, self.projected_points, self.screen)
            self.__connect_points(p + 4, ((p + 1) % 4) + 4, self.projected_points, self.screen)
            self.__connect_points(p, (p + 4), self.projected_points, self.screen)


def run():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()

    cube_position = [WIDTH / 2, HEIGHT / 2]
    cube = Cube(screen, cube_position)

    while 1:
        clock.tick(FPS)
        screen.fill(BLACK)

        cube.project_cube()

        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    quit()


if __name__ == '__main__':
    WIDTH, HEIGHT = 1920, 1080
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    FPS = 60
    run()
