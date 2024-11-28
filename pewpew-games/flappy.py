import pew
import random

# Game Constants
FPS = 10
GAME_OVER_FPS = 3

COL_FPS = 30
MAX_COLSPEED = 3
MIN_COLSPEED = 7

frames_elapsed = 0

screen = pew.Pix()

pew.init()

x = 1
y = 3

colx = 8
space = 0
col_speed = 6 
col_passed = False
game = True

def drawCol(pos, space):
    for i in range(8):
        if i != space and i-1 != space and i-2 != space:
            screen.pixel(pos, i, 1)
        
def delCol(pos):
    for i in range(8):
        screen.pixel(pos, i, 0)

def Game():
    global x, y, colx, space, col_speed, col_passed, game, frames_elapsed
    # Erase 
    screen.pixel(x,y, 0)
    
    # Draws moving column
    delCol(colx)
   
    # Smooth sped up/ slow down of columns
    if colx == 8:
        if col_speed > MAX_COLSPEED and col_passed == True:
             col_speed -= 1
        elif col_speed < MIN_COLSPEED and col_passed == False:
            col_speed += 1

    if frames_elapsed % col_speed == 0:
        colx -= 1
        if not 0 <= colx <= 7:
            space = random.randint(0, 7-2)
            colx = 8

    drawCol(colx, space)
    
    # Player controls
    keys = pew.keys()
    
    if keys & pew.K_O:
        y -= 1

    elif frames_elapsed % 2:
            y += 1 # Gravity

    

    # Check player is not out of screen
    if y > 7:
        y = 7
    elif y < 0:
        y = 0

    screen.pixel(x, y, 3)

    # If player successfully passed column, we make column faster
    if x == colx:
        if space <= y <= space+2:
            col_passed = True
        else:
            col_passed = False
            game = False

    pew.show(screen)
    pew.tick(1/FPS)

    frames_elapsed += 1

    if frames_elapsed > 10:
        frames_elapsed = 0

def GameOver():
    global frames_elapsed, game, col_speed, y, colx, space, col_passed

    screen = pew.Pix()

    i = 0
    while i <= 4:
        i += 1
        # Draws game over screen
        if i == 1:
            screen.pixel(2, 2, 3)
            screen.pixel(5, 2, 3)
        elif i == 2:
            screen.pixel(3, 4, 3)
            screen.pixel(4, 4, 3)
        elif i == 3:
            screen.pixel(2, 5, 3)
            screen.pixel(3, 5, 3)
            screen.pixel(4, 5, 3)
            screen.pixel(5, 5, 3)
        elif i == 4:
            screen.pixel(2, 6, 3)
            screen.pixel(3, 6, 3)
            screen.pixel(4, 6, 3)
            screen.pixel(5, 6, 3)

        pew.show(screen)
        pew.tick(1/GAME_OVER_FPS)


while True:
    if game == True:
        Game()
    else: 
        GameOver()
        
        # Reset game
        y = 3
        colx = 8
        col_speed = MIN_COLSPEED
        frames_elapsed = 0
        space = 0
        col_passed = False

        # Wait a bit
        pew.tick(3)
        screen = pew.Pix()
        pew.show(screen)
        game = True
