from pygame import *
from random import randint
from time import time as timer

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
font.init()
fire_sound = mixer.Sound('fire.ogg')
font2 = font.SysFont('Arial', 36)
font1 = font.SysFont('Arial', 80)     #sound
win = font1.render('YOU WIN!!!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
score = 0
lost = 0
goal = 20

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed,):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def move(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bulet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, 30)
        bullets.add(bulet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.y = 0
            lost = lost + 1
            self.rect.x = randint(80, win_width - 80)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()
img_bullet = "bullet.png"
ship = Player("rocket.png", 5, win_height - 100, 80, 100, 30)
monsters = sprite.Group()
img_enemy = "ufo.png" #objek
asteroids = sprite.Group()
img_steroid = "asteroid.png"

for i in range(5):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
#loop monsteraste
for i in range(3):
    asteroid = Enemy(img_steroid, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    asteroids.add(asteroid)

finish = False
run = True
max_lost = 10
life = 3

rel_time = False
num_fire = 0


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    ship.fire()
                    fire_sound.play()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True



    if not finish:
        window.blit(background, (0, 0))

        bullets.update()
        bullets.draw(window)
        ship.draw()
        ship.move()
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Reloading..', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life = life - 1

        if life == 0 or lost >= max_lost:
            window.blit(lose, (200, 200))
            finish = True
        
        if score >= goal:
            window.blit(win, (200, 200))
            finish = True
        
        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text1 = font2.render("Miss: " + str(lost), 1, (255, 255, 255))
        window.blit(text1, (10, 50))
        
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)
        
        text_life = font1.render(str(life), 1, (life_color))
        window.blit(text_life, (650, 10))
        display.update()
    time.delay(60)





