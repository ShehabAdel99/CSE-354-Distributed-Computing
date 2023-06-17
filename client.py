import threading

import pygame
from network import network
import random
from time import sleep
from dotenv import load_dotenv , find_dotenv
import os
load_dotenv(find_dotenv())
from pymongo import MongoClient
password = os.environ.get("MONGODB_PWD")
connection_string=f"mongodb+srv://melshafaie123:{password}@game.czsmeor.mongodb.net/?retryWrites=true&w=majority"
client=MongoClient(connection_string)
db = client["game_database"]
collection = db["game_state"]

pygame.init()
width_dis = 360
height_dis = 650
win = pygame.display.set_mode((width_dis, height_dis))
pygame.display.set_caption("Client")
vel = 1
clientNumber = 0
ready1 = 0
crash1=0
crash2=0
run1=True
lock =threading.Lock
class Player():
def __init__(self, x, y, width, height, car_image, bg_image):
self.crashed = False
self.white = (255, 255, 255)
self.xin=x
self.yin =y
self.x = x
self.y = y
self.width = width
self.height = height
self.car_image = pygame.image.load(car_image)
self.rect = self.car_image.get_rect()
self.rect.x = x
self.rect.y = y
self.vel = vel
self.bg_img = bg_image
self.bg_img_x1 = (width_dis / 2) - (360 / 2)
self.bg_img_x2 = (width_dis / 2) - (360 / 2)
self.bg_img_y1 = 0
self.bg_img_y2 = -600
self.bg_img_speed = 0.7
self.count = 0
self.enemy_car = pygame.image.load('.\\img\\enemy_car_1.png')
self.enemy_car_startx = random.randrange(100, 360)
self.enemy_car_starty = -600
self.enemy_car_speed = 0.5
self.enemy_car_width = 49
self.enemy_car_height = 100

def run_enemy_car(self, thingx, thingy,win):
win.blit(self.enemy_car, (thingx, thingy))
def back_ground_raod(self, win):
win.blit(self.bg_img, (self.bg_img_x1, self.bg_img_y1))
win.blit(self.bg_img, (self.bg_img_x2, self.bg_img_y2))

self.bg_img_y1 += self.bg_img_speed
self.bg_img_y2 += self.bg_img_speed

if self.bg_img_y1 >= height_dis:
self.bg_img_y1 = -600

if self.bg_img_y2 >= height_dis:
self.bg_img_y2 = -600
self.highscore(self.count, win)

def draw(self, win):
win.blit(self.car_image, self.rect)
def car(self, x, y,win):
win.blit(self.car_image, (x, y))

def move(self, win):
global crash1
global ready1
for event in pygame.event.get():
if event.type == pygame.QUIT:
self.crashed = True

keys = pygame.key.get_pressed()

if keys[pygame.K_LEFT]:
self.x -= self.vel

if keys[pygame.K_RIGHT]:
self.x += self.vel

if keys[pygame.K_UP]:
self.y -= self.vel

if keys[pygame.K_DOWN]:
self.y += self.vel

self.update()
self.back_ground_raod(win)
self.run_enemy_car(self.enemy_car_startx, self.enemy_car_starty, win)
self.enemy_car_starty += self.enemy_car_speed

if self.enemy_car_starty > height_dis:
self.enemy_car_starty = 0 - self.enemy_car_height
self.enemy_car_startx = random.randrange(100, 300)




self.count += 1
if (self.count % 10000 == 0):
self.enemy_car_speed += 0.05
self.bg_img_speed += 0.05

if self.enemy_car_starty + self.enemy_car_height > self.y + 25 and self.enemy_car_starty < self.y + self.height - 25:
if self.x + 25 > self.enemy_car_startx and self.x + 25 < self.enemy_car_startx + self.enemy_car_width:
self.crashed = True
self.display_message("You lost!", win)
crash1 = 1
sleep(1)
self.x = 160
self.y = 550
self.enemy_car_starty = -600
self.enemy_car_startx = random.randrange(100, 300)
self.enemy_car_speed = 0.5
self.bg_img_speed = 0.7
self.count = 0
if self.x < 20 or self.x > 300:
self.crashed = True
self.display_message("You lost!", win)
crash1 = 1
# ready1=0
sleep(1)




self.update()

def display_message(self, msg, win):
font = pygame.font.SysFont("comicsansms", 30, True)
text = font.render(msg, True, (255, 255, 255))
win.blit(text, (200 - text.get_width() // 2, 150 - text.get_height() // 3))
pygame.display.update()
pygame.time.delay(1000)
self.x = self.xin
self.y = self.yin
self.enemy_car_starty = -600
self.enemy_car_startx = random.randrange(100, 300)
self.enemy_car_speed = 0.5
self.bg_img_speed = 0.7
self.count = 0

# Pause the game until the player chooses to play again
clock = pygame.time.Clock()
clock.tick(60)




def highscore(self, count, win):
font = pygame.font.SysFont("arial", 20)
text = font.render("Score : " + str(count), True, self.white)
win.blit(text, (0, 0))

def update(self):
self.rect = (self.x, self.y, self.width, self.height)


def read_pos(str):
str=str.split(",")
return int(str[0]), int(str[1]), int(str[2]), int(str[3])


def make_pos(tup):
return str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2])+ "," + str(tup[3])


def redrawWindow(win, player, player2):
player.draw(win)
player2.draw(win)
pygame.display.update()
game_state_structure = {
"game_id": "my_game",
"pos": [
(),
()
]
}


def main():
global crash2
global crash1
global run1
global ready1


n = network()
car_image = r"C:\Users\melsh\Desktop\gam3a\projectDis\img\car.png"
car_image2 = r"C:\Users\melsh\Desktop\gam3a\projectDis\img\enemy_car_2.png"
bg_img = pygame.image.load(r"C:\Users\melsh\Desktop\gam3a\projectDis\img\White-broken-lines.png")
scaled_image = pygame.transform.scale(bg_img, (360, 650))
game_state = collection.find_one({"game_id": "my_game"})
if game_state:
if game_state["discar"]==1:
p = Player(game_state["pos"][1][0], game_state["pos"][1][1], 49, 100, car_image2, scaled_image)
p2 = Player(game_state["pos"][0][0], game_state["pos"][0][1], 49, 100, car_image, scaled_image)
else:
p = Player(game_state["pos"][0][0], game_state["pos"][0][1], 49, 100, car_image2, scaled_image)
p2 = Player(game_state["pos"][1][0], game_state["pos"][1][1], 49, 100, car_image, scaled_image)

else:
p = Player(50, 500, 49, 100, car_image2, scaled_image)
p2 = Player(200,500, 49, 100, car_image, scaled_image)
clock=pygame.time.Clock()
space_click=0
xc = 0
yc = height_dis // 2
vel_x = 1.5
vel_y = 0
again=0
white = (255, 255, 255)

while run1:
pressed_key2 = 0
clock.tick(100)
win.fill((202, 228, 241))
font = pygame.font.SysFont("Montserrat", 30)
text = font.render("Press Space to play!", 1, white)
text2 = font.render("Press Escape to exit!", 1, white)
text3 = font.render("Press c to chat", 1, white)
bg_image5 = pygame.image.load(r"C:\Users\melsh\Desktop\gam3a\projectDis\img\DiRT-5-Vide-Game-Race-4K-Ultra-HD-Mobile-Wallpaper-scaled.jpg")
bg_image5 = pygame.transform.scale(bg_image5, (width_dis, height_dis))
win.blit(bg_image5, (0, 0))
win.blit(text, (width_dis / 2 - text.get_width() / 2, 100))
win.blit(text2, (width_dis / 2 - text2.get_width() / 2, 500))
win.blit(text3, (width_dis / 2 - text3.get_width() / 2, 200))

pygame.display.update()
for event in pygame.event.get():
if event.type == pygame.QUIT:
run1 = False
if event.type == pygame.KEYDOWN:
if event.key == pygame.K_ESCAPE:
run1 = False
if event.key == pygame.K_SPACE:
space_click=1


while space_click:
p2Pos = read_pos(n.send(make_pos((p.x, p.y, crash1, ready1))))
p2.x = p2Pos[0]
p2.y = p2Pos[1]
crash2 = p2Pos[2]
ready2= p2Pos[3]

p2.update()

if ready2==1 and crash1==1 :
win.fill((202, 228, 241))
font = pygame.font.SysFont("comicsans", 20)
text = font.render("Press Space to play again!", 1, (58, 78, 91))
text2 = font.render("Press Escape to exit!", 1, (58, 78, 91))
win.blit(text, (80, 200))
win.blit(text2, (80, 600))
pygame.display.update()
while pressed_key2 == 0:
for event in pygame.event.get():
if event.type == pygame.QUIT:
run1 = False
if event.type == pygame.KEYDOWN:
if event.key == pygame.K_ESCAPE:
run1 = False
if event.key == pygame.K_SPACE:

crash1 = 0
pressed_key2 = 1
ready1=0

space_click= False
elif ready2 == 1 and crash2 == 0:

p.move(win)
redrawWindow(win, p, p2)


elif ready2==0 and crash2==0 and crash1==0 :
image3 = pygame.image.load(r"C:\Users\melsh\Desktop\gam3a\projectDis\img\a6rBl.png")
scaled_image = pygame.transform.scale(image3, (10, 15))
image_rect = scaled_image.get_rect()
font = pygame.font.SysFont("comicsansms", 20, True)
text1 = font.render("waiting for other player", True, white)
# xc += vel_x
# yc+= vel_y
# if xc > width_dis:
# xc = -image_rect.width
#
win.fill((135, 206, 250))
# win.blit(image3, (xc, yc))
win.blit(text1, (155 - text.get_width() // 2, 100 - text.get_height() // 3))
pygame.display.update()

elif ready2==1 and crash2==1 :

p.display_message("you win!!", win)
win.fill((202, 228, 241))
font = pygame.font.SysFont("comicsans", 20)
text = font.render("Press Space to play again! ", 1, (58, 78, 91))
text2 = font.render("Press Escape to exit!", 1, (58, 78, 91))
win.blit(text, (80, 200))
win.blit(text2, (80, 600))
pygame.display.update()
while pressed_key2==0 :
for event in pygame.event.get():
if event.type == pygame.QUIT:
run1 = False
if event.type == pygame.KEYDOWN:
if event.key == pygame.K_ESCAPE:
run1 = False
if event.key == pygame.K_SPACE:
pressed_key2=1
space_click = False






for event in pygame.event.get():
if event.type == pygame.QUIT:
space_click=0
run1 = False





main()