import pygame
import os

WIDTH, HEIGHT = 1080, 720
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Lunar Lander')


MOON = pygame.image.load(os.path.join('assets','pixel.moon.png'))
SPACESHIP = pygame.image.load(os.path.join('assets','space.ship.png'))
SPACESHIP_HEIGHT = SPACESHIP.get_height()
SPACESHIP_WIDTH = SPACESHIP.get_width()

FPS = 60
VEL = 1.5

def draw_window(space_ship):
    WIN.fill((0,0,0))
    WIN.blit(MOON,(0,0))
    WIN.blit(SPACESHIP,(space_ship.x,space_ship.y))
    pygame.display.update()
    pygame.display.flip()



def space_ship_movement(keys_pressed, spaceship):
    #LEFT
    if keys_pressed[pygame.K_a] and spaceship.x - VEL > 0:
        spaceship.x -= VEL
    #RIGHT
    if keys_pressed[pygame.K_d] and spaceship.x + VEL + spaceship.width < 1080:
        spaceship.x += VEL
    #UP
    if keys_pressed[pygame.K_w] and spaceship.y - VEL > 0:
        spaceship.y -= VEL
    #DOWN
    if keys_pressed[pygame.K_s] and spaceship.y + VEL + spaceship.height  < HEIGHT :
        spaceship.y += VEL


def main():
    run = True
    clock = pygame.time.Clock()
    space_ship = pygame.Rect(700,300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys_pressed = pygame.key.get_pressed()
        space_ship_movement(keys_pressed, space_ship)
        draw_window(space_ship)


main()
