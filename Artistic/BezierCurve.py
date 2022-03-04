#  Copyright (c) 2022. Oskar "Bocian" Możdżeń
#  All rights reserved.

import pygame as pg
import colorsys

def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))

def interpol(p1, p2, t):
    interpolation = ((1 - t) * p1[0] + t * p2[0], (1 - t) * p1[1] + t * p2[1])
    return interpolation

def calc_points(pts, t, n):
    o0 = interpol(pts[0], pts[1], t)
    if n == 2:
        return o0
    o1 = interpol(pts[1], pts[2], t)
    o2 = interpol(pts[2], pts[3], t)
    o3 = interpol(o0, o1, t)
    if n == 3:
        return o3
    o4 = interpol(o1, o2, t)
    o5 = interpol(o3, o4, t)
    return o5

WIDTH, HEIGHT = 0, 0
BLACK = (0, 0, 0)
WHITE = (255, 255 ,255)
FPS = 60

rate = 0.01
delta = rate
t = 0
n_points = 4
k = ""
draw = True

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

w, h = pg.display.get_surface().get_size()
points = [[0, h/2], [w/2, 0], [w/2, h], [w, h/2]]
start = points[0]

while 1:
    clock.tick(FPS)
    if type(k) == int:
        points[k] = pg.mouse.get_pos()
    t = 0
    screen.fill(BLACK)
    start = points[0]

    while t <= 1:
        p = calc_points(points, t, n_points)
        pg.draw.line(screen, hsv2rgb(t, 1, 1), start, p, 2)
        start = p
        t += delta
    pg.draw.line(screen, hsv2rgb(1, 1, 1), start, points[n_points-1], 2)
    if draw:
        for p in points:
            pg.draw.circle(screen, WHITE, p, 3)
    pg.display.flip()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
            break
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                quit()
                break
            if event.key == pg.K_1:
                k = 0
            elif event.key == pg.K_2 and n_points >= 2:
                k = 1
            elif event.key == pg.K_3 and n_points >= 3:
                k = 2
            elif event.key == pg.K_4 and n_points >= 4:
                k = 3
            elif event.key == pg.K_TAB:
                k = ""
            if event.key == pg.K_h:
                draw = not draw
            if event.key == pg.K_DOWN and n_points >= 3:
                n_points -= 1
            elif event.key == pg.K_UP and n_points <= 3:
                n_points += 1
                points[n_points-1] = pg.mouse.get_pos()
                k = n_points-1
            if event.key == pg.K_LEFT and delta <= 0.09:
                delta += rate
            elif event.key == pg.K_RIGHT and delta >= 0.01:
                delta -= rate
