from pygame import *
from random import randint, choice
mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.1)
mixer.music.play(-1)
fire_music = mixer.Sound('fire.ogg')
fire_music.set_volume(0.05)
kick_music = mixer.Sound('kick.ogg')
kick_music.set_volume(0.05)
window = display.set_mode((700, 500))
display.set_caption('Шутер')
background = transform.scale(image.load("galaxy.jpg"), (700, 500))
clock = time.Clock()
FPS = 60
game = True
lost = 0
shot = 0
font.init()
font1 = font.SysFont('Arial', 30)
font2 = font.SysFont('Arial', 70)
text_lose = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
text_shot = font1.render('Сбито: ' + str(shot), 1, (255, 255, 255))
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size = (65, 65)):
        super().__init__()
        self.image = transform.scale(image.load(player_image), size)
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 700 - 65:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx - 7, self.rect.y, 15, (15, 20))
        Bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost 
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = randint(-100, -50)
            self.rect.x = randint(10, 650)
            self.speed = randint(1, 3)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

istrebitel = Player('rocket.png', 325, 415, 8, (50, 70))
group = sprite.Group()
Bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(5):
    nlo = Enemy('ufo.png', randint(10, 650), randint(-100, -50), randint(1, 3), (40, 30))
    group.add(nlo)
for i in range(2):
    asteroid = Enemy('asteroid.png', randint(10, 650), randint(-100, -50), randint(1, 2), (50, 40))
    asteroids.add(asteroid)

    



finish = False
while game:
    window.blit(background, (0, 0))
    if finish == False:
        window.blit(text_lose, (0, 0))
        window.blit(text_shot, (0, 31))
        istrebitel.reset()
        istrebitel.update()
        group.draw(window)
        group.update()
        asteroids.draw(window)
        asteroids.update()
        Bullets.draw(window)
        Bullets.update()
        
        text_lose = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        text_shot = font1.render('Сбито: ' + str(shot), 1, (255, 255, 255))

        sprites_list = sprite.spritecollide(istrebitel, group, False)
        if sprites_list:
            kick_music.play()
            finish = True
            win = font2.render('YOU LOSE', True, (255, 255, 255))
        asteroids_list = sprite.spritecollide(istrebitel, asteroids, False)
        if asteroids_list:
            kick_music.play()
            finish = True
            win = font2.render('YOU LOSE', True, (255, 255, 255))
        group_list = sprite.groupcollide(group, Bullets, True, True)
        if group_list:
            shot += 1
            nlo = Enemy('ufo.png', randint(10, 650), randint(-100, -50), randint(1, 3), (40, 30))
            group.add(nlo)
        if lost >= 10:
            finish = True
            win = font2.render('YOU LOSE', True, (255, 255, 255))
        if shot >= 25:
            finish = True
            win = font2.render('YOU WIN', True, (255, 255, 255))
    if finish == True:
        window.blit(win, (230, 230))
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE and finish != True:
                istrebitel.fire()
                fire_music.play()
            if e.key == K_SPACE and finish:
                finish = False
                lost = 0
                shot = 0
                group = sprite.Group()
                Bullets = sprite.Group()
                for i in range(5):
                    nlo = Enemy('ufo.png', randint(10, 650), randint(-100, -50), randint(1, 3), (40, 30))
                    group.add(nlo)
                asteroids = sprite.Group()
                for i in range(2):
                    asteroid = Enemy('asteroid.png', randint(10, 650), randint(-100, -50), randint(1, 2), (50, 40))
                    asteroids.add(asteroid)
                istrebitel.rect.x = 325
                
                
    clock.tick(FPS)
    display.update()