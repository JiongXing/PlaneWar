import random
import pygame

SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
FRAME_PER_SEC = 60
CREATE_ENEMY_EVENT = pygame.USEREVENT + 1
HERO_FIRE_EVENT = pygame.USEREVENT + 2


class GameSprite(pygame.sprite.Sprite):

    def __init__(self, image_name, speed=1):
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        pass


class Background(GameSprite):

    def __init__(self, is_alt=False):
        super().__init__("./images/background.png")
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
        super().update()
        self.rect.y += self.speed
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):

    def __init__(self):
        super().__init__("./images/enemy1.png", random.randint(1, 3))
        self.rect.x = random.randint(0, SCREEN_RECT.width - self.rect.width)
        self.rect.bottom = 0

    def update(self):
        super().update()
        self.rect.y += self.speed
        if self.rect.y >= SCREEN_RECT.height:
            # kill方法会把自己从所有精灵组删除
            self.kill()


class Hero(GameSprite):

    def __init__(self):
        super().__init__("./images/me1.png", speed=0)
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.height - 100
        self.bullets = pygame.sprite.Group()

    def update(self):
        super().update()
        self.rect.x += self.speed
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.right > SCREEN_RECT.width:
            self.rect.right = SCREEN_RECT.width

    def fire(self):
        for index in (0, 1, 2):
            bullet = Bullet()
            bullet.rect.centerx = self.rect.centerx
            bullet.rect.bottom = self.rect.y - index * (bullet.rect.height + 8)
            self.bullets.add(bullet)

    def __del__(self):
        print("英雄挂了...")

class Bullet(GameSprite):

    def __init__(self):
        super().__init__("./images/bullet1.png", speed=-5)

    def update(self):
        super().update()
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()
