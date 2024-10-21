import pygame
import sys
import random

# CONSTANTS
WIDTH, HEIGHT = 550, 800

GRAVITY = 1
JUMP_POWER = -12

# PIPE SETTINGS

PIPE_SPAWN_RATE = 60 # Frames
PIPE_WIDTH = 70
MIN_GAP_HEIGHT = 150
MAX_GAP_HEIGHT = 250

FPS = 60

class Sprite:
    def __init__(self, x, y, name, width=None, height=None):
        self.x = x
        self.y = y
        self.image = pygame.image.load(f"assets/{name}")

        if width and height:
            self.image = pygame.transform.scale(self.image, (width, height))
        
        self.rect = self.image.get_rect(topleft=(x, y))

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.image.load("assets/pipe.png").convert_alpha()

        gap_height = random.randint(MIN_GAP_HEIGHT, MAX_GAP_HEIGHT)
        gap_y = random.randint(200, HEIGHT - gap_height - 200) 
        
        self.topImage = pygame.transform.scale(self.image, (PIPE_WIDTH, gap_y))
        self.topImage = pygame.transform.flip(self.topImage, False, True)

        self.btmImage = pygame.transform.scale(self.image, (PIPE_WIDTH, HEIGHT - gap_y - gap_height))

        self.topRect = self.topImage.get_rect(topleft=(x, 0))
        self.btmRect = self.btmImage.get_rect(topleft=(x, gap_y + gap_height))

    def update(self):
        self.topRect.x -= 5
        self.btmRect.x -= 5

    def draw(self, screen):
        screen.blit(self.topImage, self.topRect.topleft) 
        screen.blit(self.btmImage, self.btmRect.topleft)

    def off_screen(self):
        return self.topRect.x < -self.topRect.width

class Bird(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y, "yellowbird_m.png", width=50, height=40)
        self.velocity_y = 0

    def update(self):
        self.velocity_y += GRAVITY

        self.rect.y += self.velocity_y

        if bird.rect.y < 0:
            bird.rect.y = 0
        elif bird.rect.y > HEIGHT:
            bird.rect.y = HEIGHT
    
    def jump(self):
        self.velocity_y = JUMP_POWER

class Game:
    def __init__(self):
        self.pipes = []
        self.spawn_timer = 0
    
    def spawn_pipe(self):
        new_pipe = Pipe(WIDTH)
        self.pipes.append(new_pipe)

    def update(self):
        self.spawn_timer += 1
        if self.spawn_timer > PIPE_SPAWN_RATE:
            self.spawn_pipe()
            self.spawn_timer = 0

        for pipe in self.pipes:
            pipe.update()

        self.pipes = [pipe for pipe in self.pipes if not pipe.off_screen()]
    
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")

background = pygame.image.load("assets/bg_day.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

clock = pygame.time.Clock()
bird = Bird(WIDTH/10, HEIGHT/2)

game = Game()

main = True
while main:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()
    
    bird.update()
    game.update()

    screen.blit(background, (0, 0))
    screen.blit(bird.image, bird.rect)

    for pipe in game.pipes:
        pipe.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()