import random
import pew

# Space Invaders

pew.init()
screen = pew.Pix()
game = False 

FPS = 24
ALIEN_COUNT = 4
GAME_OVER_FPS = 10

def inScreen(x, y):
    return 0 <= x < 8 and 0 <= y < 8

class Bullet:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.shot = False

    def fire(self, x, y):
        if not self.shot:
            self.shot = True
            self.x = x
            self.y = y

    def draw(self, brightness=3):
        screen.pixel(self.x, self.y, brightness)

    def updateBullet(self, dy):
        self.draw(0)
        if inScreen(self.x, self.y) and self.shot:
            self.y += dy
            self.draw(3)
        else:
            self.shot = False

class AlienBullet(Bullet):
    def update(self):
        super().updateBullet(1)

class PlayerBullet(Bullet):
    def update(self):
        super().updateBullet(-1)


class Player:
    def __init__(self, x=2, y=7, health=3, width=3):
        self.x = x
        self.y = y
        self.health = health
        self.width  = width
    
    def getBrightness(self):
        if self.health >= 3:
            return 3
        elif self.health == 2:
            return 2
        elif self.health == 1:
            return 1
        else:
            return 0

    def draw(self, brightness=-1):
        if brightness == -1:
            brightness = self.getBrightness()

        for i in range(self.x, self.x + self.width):
            if inScreen(i, self.y):
                screen.pixel(i, self.y, brightness)

    def touching(self, x, y):
        return self.x <= x <= self.x + self.width and y == self.y
    
    def kill(self):
        global game 

        self.health -= 1
        if self.health <= 0:
            game = False
            self.health = 0

    def boundary(self):
        if self.x < -1:
            self.x = -1
        elif self.x + self.width-2 > 7:
            self.x = 7 - self.width+2

    def update(self):
        self.draw(0)

        if self.health > 0:
            keys = pew.keys()
            if keys & pew.K_LEFT:
                self.x -= 1
            elif keys & pew.K_RIGHT:
                self.x += 1
    
        self.boundary()
        self.draw()

class Alien:
    def __init__(self, x=3, y=2):
        self.x = x
        self.y = y
        self.bullet = AlienBullet()
        self.alive = True
        self.updateInterval = random.randint(10, 25+1)

    def kill(self):
        self.alive = False

    def draw(self, brightness=2):
        screen.pixel(self.x,self.y,brightness)

    def touching(self, x, y):
        return self.x == x and self.y == y

    def update(self, frames):
        if frames % self.updateInterval == 0:
           self.bullet.update()

        if self.alive:
            self.draw()
        else:
            self.draw(0)

class Aliens:
    def __init__(self):
        self.aliens = [] 
        self.init()  

    def init(self):
        self.aliens.clear()
        x = -1
        for _ in range(ALIEN_COUNT // 2):
            x += 2
            self.aliens.append(Alien(x, 1))
        
        x = 2
        for _ in range(ALIEN_COUNT // 2):
            x += 2
            self.aliens.append(Alien(x, 3))

    def getAlien(self, alien):
        return self.aliens[alien]

    def getAlienx(self, alien):
        return self.getAlien(alien).x
    
    def getAlieny(self, alien):
        return self.getAlien(alien).y

    def getBullet(self, alien):
        return self.getAlien(alien).bullet

    def checkIfAlienHit(self, bullet_x, bullet_y):
        for alien in range(ALIEN_COUNT):
            if self.getAlien(alien).touching(bullet_x, bullet_y):
                self.getAlien(alien).kill()

    def checkIfPlayerHit(self, player):
        for alien in range(ALIEN_COUNT):
            is_player_hit = player.touching(self.getBullet(alien).x, self.getBullet(alien).y) and self.getBullet(alien).shot

            if is_player_hit:
                player.kill()
                self.getAlien(alien).bullet.shot = False

    def updateAlien(self, alien, frames):
        return self.getAlien(alien).update(frames)
    
    def update(self, frames=0):
        for alien in range(ALIEN_COUNT):
            self.updateAlien(alien, frames)

    def updateBullets(self):
        for alien in range(ALIEN_COUNT):
            new_bullet_can_be_shot = not self.getBullet(alien).shot and self.getAlien(alien).alive and random.randrange(0,2)
            if new_bullet_can_be_shot:
                self.getBullet(alien).fire(self.getAlienx(alien), self.getAlieny(alien))

player = Player()
bullet = PlayerBullet()
aliens = Aliens()


def checkIfShooting():
    keys = pew.keys()
    if keys & pew.K_O and not bullet.shot and player.health > 0:
        bullet.fire(player.x+1, player.y)

def Game(frames=0):
    bullet.update()
    aliens.update(frames)

    aliens.checkIfPlayerHit(player)
    checkIfShooting()
    
    aliens.checkIfAlienHit(bullet.x, bullet.y)
    aliens.updateBullets()

    player.update()

def GameOverAnim():
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

frames = 0
aliens.init()
game = True 

while True:     
    if game:
        Game(frames)

        pew.show(screen)
        pew.tick(1 / FPS)
        frames += 1
    else:
        GameOverAnim()
    
        pew.tick(3)
        screen = pew.Pix()
        pew.show(screen)
            
        aliens.init()
        player = Player()
        bullet = PlayerBullet()

        game = True
