#  Copyright (c) 2022. Oskar "Bocian" Możdżeń
#  All rights reserved.

from Utilities import *

WIDTH, HEIGHT = 800, 800
FPS = 60

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
run = True

trans = Translator(WIDTH // 2, HEIGHT // 2)
leg = Leg(100, 0, 100, 0, trans, screen)

while run:
    screen.fill(BLACK)
    clock.tick(FPS)

    leg.move()
    leg.show()

    pg.display.flip()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            break
