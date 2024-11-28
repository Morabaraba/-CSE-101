import pew
import random
pew.init()
screen = pew.Pix()
game_speed = 4
player = (2, 4)
while True:    
    x, y = player
    pew.show(screen)
    pew.tick(1 / game_speed)
    screen.pixel(x, y, 0)
    keys = pew.keys()
    if keys & pew.K_UP:
        y -= 1
    if keys & pew.K_DOWN:
        y += 1
    elif keys & pew.K_LEFT:
        x -= 1
    elif keys & pew.K_RIGHT:
        x += 1
    player = (x, y )
    screen.pixel(x, y, 1)