import pygame
from plane_sprites import *


class PlaneGame(object):

    def __init__(self):
        super().__init__()
        print("游戏初始化")
        self.is_game_playing = False
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        self.clock = pygame.time.Clock()
        self.__create_sprites()
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)

    def __create_sprites(self):
        bg1 = Background()
        bg2 = Background(is_alt=True)
        self.bg_group = pygame.sprite.Group(bg1, bg2)

        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

        self.enemy_group = pygame.sprite.Group()

    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # 退出游戏
                self.__game_over()
                break
            elif event.type == CREATE_ENEMY_EVENT:
                # 创建敌机
                enemy = Enemy()
                self.enemy_group.add(enemy)
            elif event.type == HERO_FIRE_EVENT:
                # 发射子弹
                self.hero.fire()

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_RIGHT]:
            self.hero.speed = 2
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.speed = -2
        else:
            self.hero.speed = 0

    def __update_sprites(self):
        self.bg_group.update()
        self.bg_group.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.hero_group.update()
        self.hero_group.draw(self.screen)

        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

        pygame.display.update()

    def __check_collide(self):
        pygame.sprite.groupcollide(self.enemy_group, self.hero.bullets, True, True)
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        if len(enemies) > 0:
            self.hero.kill()
            self.__game_over()

    def __game_over(self):
        self.is_game_playing = False

    def start_game(self):
        pygame.init()
        print("游戏开始")
        bg = pygame.image.load("./images/background.png")
        self.is_game_playing = True
        while self.is_game_playing:
            self.clock.tick(FRAME_PER_SEC)
            self.__event_handler()
            self.__update_sprites()
            self.__check_collide()

        pygame.quit()
        print("游戏结束")


if __name__ == '__main__':
    PlaneGame().start_game()
