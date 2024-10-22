import pygame
import sys
import random

# CONSTANTS
WIDTH, HEIGHT = 550, 800
FPS = 60

GRAVITY = 1
JUMP_POWER = -12

# PIPE SETTINGS
PIPE_SPAWN_RATE = 45
PIPE_SPEED = 5
MIN_GAP_HEIGHT = 100
MAX_GAP_HEIGHT = 150

# IMAGES
birds = [
    pygame.image.load("assets/yellowbird_m.png")
]
top_pipe_image = pygame.image.load("assets/pipetop.png")
btm_pipe_image = pygame.image.load("assets/pipebtm.png")
bg1 = pygame.image.load("assets/bg_day.png")

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self):
        self.rect.x -= PIPE_SPEED

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def off_screen(self):
        return self.rect.x < -self.rect.width

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = birds[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = 0

    def update(self):
        self.vel += GRAVITY
        self.rect.y += self.vel

        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > HEIGHT:
            self.rect.y = HEIGHT

    def jump(self):
        self.vel = JUMP_POWER

class Game:
    def __init__(self):
        self.spawn_timer = 0

    def spawn_pipe(self):
        x_top = 550
        y_top = random.randint(-600, -480)
        y_btm = y_top + random.randint(MIN_GAP_HEIGHT, MAX_GAP_HEIGHT) + btm_pipe_image.get_height()
        pipes.add(Pipe(x_top, y_top, top_pipe_image))
        pipes.add(Pipe(x_top, y_btm, btm_pipe_image))

    def update(self):
        self.spawn_timer += 1
        if self.spawn_timer > PIPE_SPAWN_RATE:
            self.spawn_pipe()
            self.spawn_timer = 0

        pipes.update()

        for pipe in list(pipes):
            if pipe.off_screen():
                pipes.remove(pipe)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")

background = pygame.transform.scale(bg1, (WIDTH, HEIGHT))

clock = pygame.time.Clock()

bird = pygame.sprite.GroupSingle()
bird.add(Bird(WIDTH / 10, HEIGHT / 2))

pipes = pygame.sprite.Group()

game = Game()

main = True
while main:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.sprite.jump()

    bird.update()
    game.update()

    screen.blit(background, (0, 0))
    pipes.draw(screen)
    if bird.sprite:
        screen.blit(bird.sprite.image, bird.sprite.rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
