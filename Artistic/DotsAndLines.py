#  Copyright (c) 2022. Oskar "Bocian" Możdżeń
#  All rights reserved.

import math
import numpy as np
import pygame as pg
import random as rm
import ctypes


class Dot:
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.pos = vec(np.random.randint(0, WIDTH), np.random.randint(0, HEIGHT))
        self.vel = vec(rm.randrange(-3, 3),  rm.randrange(-3, 3))
        if self.vel[0] == 0:
            self.vel[0] = rm.randint(1, 3)
        if self.vel[1] == 0:
            self.vel[1] = rm.randint(1, 3)
        self.acc = vec((0, 0))
        self.frame = 0

    def draw(self):
        pg.draw.circle(self.screen, WHITE, self.pos, 5)

    def move(self):
        self.pos += self.vel
        if self.pos[0] > WIDTH-5:
            self.vel[0] = -self.vel[0]
        elif self.pos[0] < 5:
            self.vel[0] = abs(self.vel[0])
        if self.pos[1] > HEIGHT-5:
            self.vel[1] = -self.vel[1]
        elif self.pos[1] < 5:
            self.vel[1] = abs(self.vel[1])


def run():
    pg.init()
    clock = pg.time.Clock()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    flock = []
    for _ in range(n_units):
        flock.append(Dot(screen))

    while 1:
        clock.tick(FPS)
        screen.fill(0)
        for dot in flock:
            neighbours = flock.copy()
            neighbours.remove(dot)
            for neighbour in neighbours:
                distance = math.sqrt(
                    math.pow(dot.pos[0] - neighbour.pos[0], 2) + math.pow(dot.pos[1] - neighbour.pos[1], 2))
                if distance < 225:
                    ratio = abs((distance/225)-1)
                    color = (int(255*ratio), int(255*ratio), int(255*ratio))
                    pg.draw.aaline(screen, color, dot.pos, neighbour.pos, 4)
            dot.move()
        for dot in flock:
            dot.draw()
        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()


if __name__ == "__main__":
    user32 = ctypes.windll.user32
    WIDTH = user32.GetSystemMetrics(78)
    HEIGHT = user32.GetSystemMetrics(79)
    WHITE = (255, 255, 255)
    FPS = 60
    n_units = 100
    vec = pg.math.Vector2
    run()
