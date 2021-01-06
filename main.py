import sys
import pygame
from pygame.sprite import Sprite


class Settings:
    'A class to store all settings for Lunar Lander.'

    def __init__(self):
        self.screen_width = 1080
        self.screen_height = 720
        self.bg = pygame.image.load('assets/fundo.png')
        self.white = (255,255,255)
        self.font = pygame.font.SysFont('comicsans', 60)
        self.font_gameover = pygame.font.SysFont('comicsans', 150)

class Lander(Sprite):
    'A class to manage the lander.'

    def __init__(self, ll_game):
        super().__init__()

        self.screen = ll_game.screen
        self.screen_rect = ll_game.screen.get_rect()

        self.image = pygame.image.load('assets/space.ship.png')
        self.rect = self.image.get_rect()
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.speed = [0, 2]
        self.move_left = False
        self.move_right = False
        self.move_up = False

        self.fuel = 1000

    def move(self):
        self.rect = self.rect.move(self.speed)

    def update(self):
        if self.move_left and self.rect.left > 0:
            if self.speed[0] > -2:
                self.speed[0] -= 0.25
        if self.move_right and self.rect.right < self.screen_rect.right:
            if self.speed[0] < 2:
                self.speed[0] += 0.25
        if self.move_up and self.fuel > 0:
            self.fuel -= 1
            if self.speed[1] > -1.5:
                self.speed[1] -= 0.25
        if self.speed[1] < 2:
            self.speed[1] += 0.18
        if self.rect.left <= 0 and self.move_left:
            self.speed[0] = 0
        if self.rect.right >= self.screen_rect.right and self.move_right:
            self.speed[0] = 0

    def draw_lander(self):
        self.screen.blit(self.image, self.rect)


class Moon(Sprite):
    'A class to manage the moon'

    def __init__(self, ll_game):
        super().__init__()
        self.screen = ll_game.screen
        self.settings = ll_game.settings

        self.image = pygame.image.load('assets/pixel.moon.png')
        self.rect = self.image.get_rect()

    def draw_moon(self):
        self.screen.blit(self.image, self.rect)

class Base(Sprite):
    'A class to manage the base'

    def __init__(self, ll_game):
        super().__init__()
        self.screen = ll_game.screen

        self.image = pygame.image.load('assets/base.png')
        self.rect = self.image.get_rect()
        self.rect.x += 500
        self.rect.y += 479

    def draw_base(self):
        self.screen.blit(self.image, self.rect)
        # (500,479)

class ScoreBoard:
    'A class to manage the scoreboard'

    def __init__(self, ll_game):
        self.screen = ll_game.screen
        self.settings = Settings()
        self.lander = Lander(ll_game)

        self.total_score = 0
        self.total_fuel = 1000
        self.wastefuel = False 
        self.is_gameover = False 
        self.is_gameover_clutch = False 

    def draw_fuel(self):
        if self.wastefuel:
            if self.total_fuel > 0: 
                self.total_fuel -= 1
        self.fuel = self.settings.font.render('Fuel  ' + str(self.total_fuel),1,self.settings.white)
        self.screen.blit(self.fuel, self.screen.get_rect())

    def draw_score(self):
        if self.is_gameover_clutch:
            self.score = self.settings.font.render('Score  ' + str(self.total_score + 1),1,self.settings.white)
            self.screen.blit(self.score,(0,50))
        else:
            self.score = self.settings.font.render('Score  ' + str(self.total_score),1,self.settings.white)
            self.screen.blit(self.score,(0,50))

    def draw_gameover(self):
        self.gameover = self.settings.font_gameover.render('Game Over!',1,self.settings.white)
        if self.is_gameover:
            self.screen.blit(self.gameover,(self.settings.screen_width / 2 - self.gameover.get_width() / 2 , self.settings.screen_height / 2 - self.gameover.get_height() / 2 - 55))
            self.screen.blit(self.score, (self.settings.screen_width / 2 - self.score.get_width() / 2 , self.settings.screen_height / 2 - self.score.get_height() / 2 + 7))
        if self.is_gameover_clutch:
            self.score = self.settings.font.render('Score  ' + str(self.total_score + 1),1,self.settings.white)
            self.screen.blit(self.gameover,(self.settings.screen_width / 2 - self.gameover.get_width() / 2 , self.settings.screen_height / 2 - self.gameover.get_height() / 2 - 55))
            self.screen.blit(self.score, (self.settings.screen_width / 2 - self.score.get_width() / 2 , self.settings.screen_height / 2 - self.score.get_height() / 2 + 7))

class LunarLander:
    'Overall class to manage game assets and behavior.'

    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Lunar Lander')

        self.lander = Lander(self)
        self.moon = Moon(self)
        self.base = Base(self)
        self.scoreboard = ScoreBoard(self)

    def run_game(self):
        while True:
            self._check_events()
            self.lander.update()
            self.lander.move()
            self._collisions()
            self._landing()
            self._update_screen()

    def _check_events(self):
        'Respond to key presses.'
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_w:
            self.lander.move_up = True
            self.scoreboard.wastefuel = True
        elif event.key == pygame.K_a:
            self.lander.move_left = True
        elif event.key == pygame.K_d:
            self.lander.move_right = True
        elif event.key == pygame.K_ESCAPE:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_w:
            self.lander.move_up = False
            self.scoreboard.wastefuel = False 
        elif event.key == pygame.K_a:
            self.lander.move_left = False
        elif event.key == pygame.K_d:
            self.lander.move_right = False

    def _collisions(self):
        collisions = pygame.sprite.collide_mask(self.lander, self.moon)
        if collisions:
            if self.scoreboard.total_fuel >= 100:
                self.scoreboard.total_fuel -= 100
                self.lander.fuel -= 100
                self.lander.rect = self.lander.image.get_rect()
            else:
                self.scoreboard.total_fuel = 0
                self.lander.fuel = 0 
                self.lander.speed = [0,0]
                self.scoreboard.is_gameover = True
    
    def _landing(self):
        landing = pygame.sprite.collide_mask(self.lander, self.base)
        if landing:
            if self.scoreboard.total_fuel > 0:
                self.lander.speed = [0, 0]
                self.lander.rect = self.lander.image.get_rect()
                self.scoreboard.total_score += 1 
            else:
                self.lander.speed = [0,0]
                self.scoreboard.is_gameover_clutch =  True
                  
    def _update_screen(self):
        'Update images on the screen, and flip to the new screen.'
        self.screen.blit(self.settings.bg, (0, 0))
        self.moon.draw_moon()
        self.base.draw_base()
        self.lander.draw_lander()
        self.scoreboard.draw_fuel()
        self.scoreboard.draw_score()
        self.scoreboard.draw_gameover()

        pygame.display.flip()
        pygame.time.delay(5)

if __name__ == '__main__':
    ll = LunarLander()
    ll.run_game()