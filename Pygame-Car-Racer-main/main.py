import pygame
import time
import math
from utils import scale_image, blit_rotate_center, blit_text_center
pygame.font.init()

GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("imgs/track.png"), 0.9)

TRACK_BORDER = scale_image(pygame.image.load("imgs/track-border.png"), 0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

FINISH = pygame.image.load("imgs/finish.png")
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (130, 250)

RED_CAR = scale_image(pygame.image.load("imgs/red-car.png"), 0.55)
GREEN_CAR = scale_image(pygame.image.load("imgs/green-car.png"), 0.55)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game!")

MAIN_FONT = pygame.font.SysFont("comicsans", 44)

FPS = 60


class GameInfo:
    LEVELS = 1

    def __init__(self, level=1):
        self.level = level
        self.started = False
        self.level_start_time = 0

    def reset(self):
        self.level = 1
        self.started = False
        self.level_start_time = 0


    def start_level(self):
        self.started = True
        self.level_start_time = time.time()

    def get_level_time(self):
        if not self.started:
            return 0
        return round(time.time() - self.level_start_time)




class PlayerCar:
    def __init__(self, max_vel, rotation_vel, IMG, START_POS):
        self.img = IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = START_POS
        self.acceleration = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel
        self.move()


def reset_cars(player1_car,player2_car):
    player1_car.x, player1_car.y = (180, 200)
    player1_car.angle = 0
    player1_car.vel = 0
    player2_car.x, player2_car.y = (150, 200)
    player2_car.angle = 0
    player2_car.vel = 0

def draw(win, images, player1_car, player2_car):
    for img, pos in images:
        win.blit(img, pos)

    player1_car.draw(win)
    player2_car.draw(win)
    pygame.display.update()


def move_player1(player1_car):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_LEFT]:
        player1_car.rotate(left=True)
    if keys[pygame.K_RIGHT]:
        player1_car.rotate(right=True)
    if keys[pygame.K_UP]:
        moved = True
        player1_car.move_forward()
    if keys[pygame.K_DOWN]:
        moved = True
        player1_car.move_backward()

    if not moved:
        player1_car.reduce_speed()


def move_player2(player2_car):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player2_car.rotate(left=True)
    if keys[pygame.K_d]:
        player2_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player2_car.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player2_car.move_backward()

    if not moved:
        player2_car.reduce_speed()


def handle_collision(player1_car, player2_car):
    if player1_car.collide(TRACK_BORDER_MASK) != None:
        player1_car.bounce()

    if player2_car.collide(TRACK_BORDER_MASK) != None:
        player2_car.bounce()

    player1_finish_poi_collide = player1_car.collide(
        FINISH_MASK, *FINISH_POSITION)
    if player1_finish_poi_collide != None:
        if player1_finish_poi_collide[1] == 0:
            player1_car.bounce()
        else:
            blit_text_center(WIN, MAIN_FONT, "Player 1 won the game!!!!")
            pygame.display.update()
            time.sleep(1.5)
            game_info.reset()
            reset_cars(player1_car, player2_car)

    player2_finish_poi_collide = player2_car.collide(
        FINISH_MASK, *FINISH_POSITION)
    if player2_finish_poi_collide != None:
        if player2_finish_poi_collide[1] == 0:
            player2_car.bounce()
        else:
            blit_text_center(WIN, MAIN_FONT, "Player 2 won the game!!!!")
            pygame.display.update()
            time.sleep(1.5)
            game_info.reset()
            reset_cars(player1_car, player2_car)


run = True
clock = pygame.time.Clock()
images = [(GRASS, (0, 0)), (TRACK, (0, 0)),
          (FINISH, FINISH_POSITION), (TRACK_BORDER, (0, 0))]
player1_car = PlayerCar(4, 4, RED_CAR, (180, 200))
player2_car = PlayerCar(4, 4, GREEN_CAR, (150, 200))
finisher = 0
game_info = GameInfo()

"""

draw(WIN, images, player1_car, player2_car)
timer=["3","2","1","GO !!!!"]
for i in timer:
    pygame.display.update()
    blit_text_center(WIN, MAIN_FONT, f"{i}")
    time.sleep(1)
    blit_text_center(WIN, MAIN_FONT, " ")
    
"""

while run:
    clock.tick(FPS)

    draw(WIN, images, player1_car, player2_car)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    move_player1(player1_car)
    move_player2(player2_car)
    handle_collision(player1_car, player2_car)




pygame.quit()
