import pygame
import time
import math
from utils import scale_image

GRASS = scale_image(pygame.image.load("Images/grass.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("Images/track.png"), 0.9)

TRACK_BORDER = scale_image(pygame.image.load("Images/track-border.png"), 0.9)
FINISH = pygame.image.load("Images/finish.png")
RED_CAR = scale_image(pygame.image.load("Images/red-car.png"), 0.55)
GREEN_CAR = scale_image(pygame.image.load("Images/green-car.png"), 0.55)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drift76")

FPS = 60

def draw(win, images):
    for img, pos in images:
        win.blit(img, pos)

run = True
clock = pygame.time.Clock()
images = [(GRASS, (0, 0)), (TRACK, (0, 0))]

while run:
    clock.tick(FPS)

    draw(WIN, images)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
pygame.quit()