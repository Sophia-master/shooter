#Создай собственный Шутер!

from pygame import *
from random import randint
mixer.init()
font.init()


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, plaer_x, plaer_y, plaer_speed, rect_with, rect_height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (rect_with, rect_height))
        self.speed = plaer_speed
        self.rect = self.image.get_rect()
        self.rect.x = plaer_x
        self.rect.y = plaer_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Plaer(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 20:
            self.rect.x += self.speed 

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -15, 15, 20)
        bullets.add(bullet)
        global score
        score += 1

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width-80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()



lost = 0
score = 0
live = 5

max_lost = 5
goal = 10

win_width = 700
win_height = 530
window = display.set_mode((win_width, win_height))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

z = 10
plaer = Plaer('rocket.png', 100, 435, z, 60, 80)
# enemy = Enemy('cyborg.png', (win_width/2), (win_height/2), z)
# final = GameSprite('treasure.png', 20, 300, 0)
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, win_width-80), -40, randint(1, 3), 80, 50)
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1, 2):
    asteroid = Enemy('asteroid.png', randint(80, win_width-80), -40, randint(1, 2), 80, 50)
    asteroids.add(asteroid)

bullets = sprite.Group()

font2 = font.SysFont('Arial', 36)
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

game = True
finish = False
clock = time.Clock()
FPS = 60

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                plaer.fire()

    if not finish:
        window.blit(background, (0 ,0))

        text_score = font2.render('Счет:' + str(score), True, (255, 255, 255))
        window.blit(text_score, (10, 20))

        text_lost = font2.render('Пропущено:' + str(lost), True, (255, 255, 255))
        window.blit(text_lost, (10, 50))

        plaer.update()
        monsters.update()
        asteroids.update()
        bullets.update()

        plaer.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        collides = sprite.groupcollide(bullets, monsters, True, True)
        for c in collides:
            score += 1
            monster = Enemy('ufo.png', randint(80, win_width-80), -40, randint(1, 3), 80, 50)
            monsters.add(monster)

        if sprite.spritecollide(plaer, asteroids, True) or lost > max_lost:
            live -= 1

        if sprite.spritecollide(plaer, monsters, True) or lost > max_lost:
            live -= 1

        text_live = font2.render('Жизни:' + str(live), True, (255, 255, 255))
        window.blit(text_live, (550, 50))

        if live <= 0:
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        

    else:
        finish = False
        score = 0
        lost = 0
        live = 5
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()

        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy('ufo.png', randint(80, win_width-80), -40, randint(1, 3), 80, 50)
            monsters.add(monster)





    clock.tick(FPS)
    display.update()








