import pew
import random

FPS = 15
GAME_OVER_FPS = 3

pew.init()
screen = pew.Pix()
game = True

class Player:
    def __init__(self, x=0, y=3, height=2, type_player="player"):
        self.x = x
        self.y = y
        self.height = height
        self.type_player = type_player
    
    def collision(self):
        if self.x < 0:
            self.x = 0
        elif self.x > 7:
            self.x = 7

        if self.y + self.height-1 < 0:
            self.y = 0 - self.height+1
        elif self.y > 7:
            self.y = 7
    
    def draw(self, brightness=1):
        x = self.x
        y = self.y
        height = self.height

        for i in range(y, y+height):
             if 0 <= i < 8:
                screen.pixel(x,i,brightness) 

    def update(self):
        self.draw(0)

        keys = pew.keys()
        
        if self.type_player == "player": 
            if keys & pew.K_UP:
                self.y += -1
            elif keys & pew.K_DOWN:
                self.y += 1

        self.collision()
        self.draw(1)

player = Player()
ai = Player(7,3,2,"ai")

class Ball:
    def __init__(self, x=2, y=3, dx=1, dy=1):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def touching_player(self, _player):
        return _player.y <= self.y <= _player.y + _player.height-1

    def player_collision(self):
        if self.x == 1 and self.touching_player(player):
            self.dx = -self.dx
            self.dy = self.randomdir()
        elif self.x == 6 and self.touching_player(ai):
            self.dx = -self.dx
            self.dy = self.randomdir()


    def wall_collision(self):
        global game 

        if self.x <= 0:
            game = False
        elif self.x > 7:
            self.x = 7
            self.dx = -self.dx

        if self.y < 0:
            self.y = 0
            self.dy = -self.dy
        elif self.y > 7:
            self.y = 7
            self.dy = -self.dy
    
    def randomdir(self):
        return random.choice([-1, 0, 1])

    def collision(self):
        self.wall_collision()
        self.player_collision()

    def update(self):
        screen.pixel(self.x, self.y, 0)

        self.collision()
        self.x += self.dx
        self.y += self.dy

        screen.pixel(self.x, self.y, 3)  
      
ball = Ball()

def GameOverAnim():
    global screen

    screen = pew.Pix()

    i = 0
    while i <= 4:
        i += 1
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


frames = 0
while True:
    if game == True:
        if frames % 2 == 0:
            ball.update()
    
        player.update()
        ai.update()

        pew.show(screen)
        pew.tick(1/FPS)
        frames += 1
    else:
        GameOverAnim()
    
        pew.tick(3)
        screen = pew.Pix()
        pew.show(screen)

        player = Player()
        ai = Player(7,3,2,"ai")
        ball = Ball()

        game = True
        player.update()
        ai.update()
        ball.update()
        pew.show(screen)

        

