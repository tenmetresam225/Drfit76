import pygame
import time
import math
import platform
import os

uname = os.uname()

if uname[1] == "raspberrypi":
    print("I am on a Pi, Importing GPIO Lib")
    from gpiozero import Button

    joystick_up = Button(4)
    joystick_down = Button(17)
    joystick_left = Button(27)
    joystick_right = Button(22)
    button_top_left = Button(18)
    button_top_middle = Button(15)
    button_top_right = Button(14)
    button_bottom_left = Button(25)
    button_bottom_middle = Button(24)
    button_bottom_right = Button(23)
    button_blue_left = Button(10)
    button_blue_right = Button(9)


from utils import scale_image, blit_rotate_center

GRASS = scale_image(pygame.image.load("Images/grass.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("Images/final-test-track-border.png"), 0.6)

TRACK_BORDER = scale_image(pygame.image.load("Images/final-test-track-border.png"), 0.6)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

FINISH = pygame.image.load("Images/finish.png")
RED_CAR = scale_image(pygame.image.load("Images/red-car.png"), 0.55)
GREEN_CAR = scale_image(pygame.image.load("Images/green-car.png"), 0.55)
MAIN_CAR = scale_image(pygame.image.load("Images/main-car.png"), 0.35)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Drift76")

FPS = 60

class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        moving = True
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        moving = True
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 1, 0)
        self.move()

    def bounce(self):
        if forward:
            self.vel = -1
        if reverse:
            self.vel = +1

    def stall(self):
        self.vel == 0

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

class PlayerCar(AbstractCar):
    IMG = MAIN_CAR
    START_POS = (180, 200)
def draw(win, images, player_car):
    for img, pos in images:
        win.blit(img, pos)

    player_car.draw(win)
    pygame.display.update()

run = True
clock = pygame.time.Clock()
images = [(GRASS, (0, 0)), (TRACK, (0, 0))]
player_car = PlayerCar(4, 4)

while run:
    clock.tick(FPS)

    draw(WIN, images, player_car)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    keys = pygame.key.get_pressed()
    moved = False
    moving = False
    forward = False
    reverse = False

    if keys[pygame.K_w]:
        moved = True
        moving = True
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved = True
        moving = True
        player_car.move_backward()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()

    if uname[1] == "raspberrypi":
        if button_bottom_left.is_pressed:
            if button_bottom_middle.is_pressed:
                AbstractCar.stall()
            else:
                moved = True
                moving = True
                forward = True
                player_car.move_forward()
        if button_bottom_middle.is_pressed:
            moved = True
            moving = True
            reverse = True
            player_car.move_backward()
        if button_blue_left.is_pressed:
            pygame.quit()

    if moving:
        if keys[pygame.K_a]:
            player_car.rotate(left=True)
        if keys[pygame.K_d]:
            player_car.rotate(right=True)
        if uname[1] == "raspberrypi":
            if joystick_left.is_pressed:
                player_car.rotate(left=True)
            if joystick_right.is_pressed:
                player_car.rotate(right=True)

    if not moved:
        player_car.reduce_speed()

    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce()

pygame.quit()
