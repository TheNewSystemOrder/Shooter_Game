#Створи власний Шутер!

from pygame import *
from pygame.sprite import*
from random import randint
from time import time as timer

#class GameSprite(sprite.Sprite):
img_hero = 'rocket.png'
font.init()
font1 = font.SysFont('Arial', 80)
font2 = font.SysFont('Arial', 36)
win = font1.render("YOU WIN", True, (255, 255, 255))
lose = font2.render("YOU LOSE"  , True, (190, 0 , 0))
lost = 0 
goal = 5               
score = 0
max_lost = 5 
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter_Game")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire = mixer.Sound('fire.ogg')
fire_sound = mixer.Sound("fire.ogg ")

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
        

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill() 

ship = Player(img_hero, 5, win_height - 100, 100, 80, 10)
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(1,5))
    monsters.add(monster)
asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy("asteroid.png", randint(30, win_width - 80), -40, 80, 50, randint(1,7))
    asteroids.add(asteroid)

bullets = sprite.Group()

finish = False

run = True
rel_time = False
num_fire = 0

clock = time.Clock()
FPS = 60
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 10    and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    if not finish:
        window.blit(background,(0, 0))
        text = font2.render("Рахунок" + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render("пропущено" + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 2:
                reload = font2.render("wait reload..." , 1 , (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters,False) or sprite.spritecollide(ship, asteroids ,False) or lost >=max_lost:
            finish = True
            window.blit(lose, (200, 200))
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        display.update()
    time.delay(50)
    clock.tick(FPS)