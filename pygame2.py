## Imports

import pygame
import sys

## Constants

WIDTH, HEIGHT = 600, 800
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Classes

class Sprite:
    def __init__(self, x, y, name, width=None, height=None):
        self.x = x
        self.y = y
        self.image = pygame.image.load(name)

        if width and height:
            self.image = pygame.transform.scale(self.image, (width, height))
        
        self.rect = self.image.get_rect(topleft=(x, y))

class Player(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y, "testSprite.png", width=50, height=50)

def CheckCollisions(player):
    if player.rect.left < 0:
        player.rect.left = 0
    elif player.rect.right > WIDTH:
        player.rect.right = WIDTH

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")

clock = pygame.time.Clock()
player = Player(300, 400)

main = True
while main:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill(WHITE)

    screen.blit(player.image, player.rect)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.rect.x -= 5
    if keys[pygame.K_d]:
        player.rect.x += 5

    CheckCollisions(player)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
