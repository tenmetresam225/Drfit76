import pygame
import time
import math

GRASS = pygame.image.load("Images/grass.jpg")
TRACK = pygame.image.load("Images/track.png")

TRACK_BORDER = pygame.image.load("Images/track-border.png")
FINISH = pygame.image.load("Images/finish.png")
RED_CAR = pygame.image.load("Images/red-car.png")
GREEN_CAR = pygame.image.load("Images/green-car.png")

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game!")

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
pygame.quit()