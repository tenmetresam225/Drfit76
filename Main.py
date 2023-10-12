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
TRACK = scale_image(pygame.image.load("Images/track.png"), 0.6)
MENU = scale_image(pygame.image.load("Images/Logo.png"), 0.6)
TRACK_BORDER = scale_image(pygame.image.load("Images/track-border.png"), 0.6)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

FINISH = pygame.image.load("Images/finish.png")
RED_CAR = scale_image(pygame.image.load("Images/red-car.png"), 0.55)
GREEN_CAR = scale_image(pygame.image.load("Images/green-car.png"), 0.55)
MAIN_CAR = scale_image(pygame.image.load("Images/main-car.png"), 0.35)
RIVAL_CAR = scale_image(pygame.image.load("Images/rival-car.png"), 0.35)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Drift76")

FPS = 60
PATH = [(190, 87), (235, 50), (487, 50), (506, 107), (486, 180), (401, 185), (316, 171), (262, 209), (291, 249), (353, 253), (415, 255), (478, 255), (504, 282), (503, 321), (503, 361), (505, 452), (489, 490), (448, 500), (408, 485), (396, 444), (404, 393), (404, 347), (380, 320), (348, 311), (320, 311), (294, 324), (279, 347), (270, 381), (267, 415), (273, 443), (278, 464), (260, 488), (228, 497), (201, 487), (166, 450), (126, 409), (93, 371), (48, 331), (34, 277), (33, 193), (29, 124), (32, 68), (69, 38), (102, 39), (126, 61), (130, 104), (128, 153), (114, 194), (104, 228), (105, 258), (135, 285), (167, 286), (193, 254), (189, 220), (186, 165), (186, 126)]


class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.2

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
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
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
            self.vel = -0.5
            moving = False
        if reverse:
            self.vel = +0.5
            moving = False

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi


class ComputerCar(AbstractCar):
    IMG = RIVAL_CAR
    START_POS = (175, 200)

    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel)
        self.path = path
        self.current_point = 0
        self.vel = max_vel

    def draw_points(self, win):
        for point in self.path:
            pygame.draw.circle(win, (255, 0, 0), point, 5)

    def draw(self, win):
        super().draw(win)

        self.draw_points(win)

    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff == 0:
            desired_radian_angle = math.pi / 2
        else:
            desired_radian_angle = math.atan(x_diff/y_diff)

        if target_y > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))

    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1


    def move(self):
        if self.current_point >= len(self.path):
            return

        self.calculate_angle()
        self.update_path_point()
        super().move()

class PlayerCar(AbstractCar):
    IMG = MAIN_CAR
    START_POS = (190, 200)


def draw(win, images, player_car, computer_car):
    for img, pos in images:
        win.blit(img, pos)

    player_car.draw(win)
    computer_car.draw(win)
    pygame.display.update()


def Main(x, y):
    WIN.blit(MENU, (0, 0))
    pygame.display.update()


run = True
clock = pygame.time.Clock()
images = [(GRASS, (0, 0)), (TRACK, (0, 0))]
player_car = PlayerCar(2, 4)
computer_car = ComputerCar(2, 4, PATH)
Menu = False

while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    computer_car.move()

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
    if keys[pygame.K_TAB]:
        Menu = True

    if uname[1] == "raspberrypi":
        if button_blue_left.is_pressed:
            Menu = not Menu
            pygame.time.wait(1500)
            print("FREESIA")
        if button_bottom_left.is_pressed:
            moved = True
            moving = True
            forward = True
            player_car.move_forward()
        if button_bottom_middle.is_pressed:
            moved = True
            moving = True
            reverse = True
            player_car.move_backward()
        if button_blue_right.is_pressed:
            pygame.quit()

    if not Menu:
        Main(0, 0)
    else:
        draw(WIN, images, player_car, computer_car)

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

    print(computer_car.path)
print("diddly doo")
pygame.quit()
