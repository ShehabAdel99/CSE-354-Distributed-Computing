import pygame
from network import network
import random
from time import sleep
from pygame.locals import *
import redis

r=redis.Redis(host="192.168.1.10",port=6379,db=0)





pygame.init()
width_dis = 360
height_dis = 650
win = pygame.display.set_mode((width_dis, height_dis))
pygame.display.set_caption("Client")
vel = 1
clientNumber = 0
crash1=0
crash2=0

class Player():
    def __init__(self, x, y, width, height, car_image, bg_image):
        self.crashed = False
        self.white = (255, 255, 255)
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
        self.enemy_car = pygame.image.load(r"E:\Semseter 8\Distributed Computing\Project\img\enemy_car_1.png")
        self.enemy_car_startx = random.randrange(100, 360)
        self.enemy_car_starty = -600
        self.enemy_car_speed = 0.5
        self.enemy_car_width = 49
        self.enemy_car_height = 100

    def run_enemy_car(self, thingx, thingy,win):
        win.blit(self.enemy_car, (thingx, thingy))


        data={
            "x":self.x,
            "y":self.y,
            'start_x': self.enemy_car_startx,
            'start_y': self.enemy_car_starty,
            'score': self.count,
            'bg_speed': self.bg_img_speed,
            'enemy_speed': self.enemy_car_speed,
            'enemy_start_x': self.enemy_car_startx,
            'enemy_start_y': self.enemy_car_starty
    }
        r.hmset("game_data",data)
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

        self.update(win)
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
                sleep(1)
                self.x = 160
                self.y = 550
                self.enemy_car_starty = -600
                self.enemy_car_startx = random.randrange(100, 300)
                self.enemy_car_speed = 0.5
                self.bg_img_speed = 0.7
                self.count = 0
        data = {
            "x": self.x,
            "y": self.y,
            'start_x': self.enemy_car_startx,
            'start_y': self.enemy_car_starty,
            'score': self.count,
            'bg_speed': self.bg_img_speed,
            'enemy_speed': self.enemy_car_speed,
            'enemy_start_x': self.enemy_car_startx,
            'enemy_start_y': self.enemy_car_starty
        }
        r.hmset("game_data", data)



        self.update(win)

    def display_message(self, msg, win):
        font = pygame.font.SysFont("comicsansms", 30, True)
        text = font.render(msg, True, (255, 255, 255))
        win.blit(text, (200 - text.get_width() // 2, 150 - text.get_height() // 3))
        pygame.display.update()

        # Pause the game until the player chooses to play again
        clock = pygame.time.Clock()
        clock.tick(60)

        font = pygame.font.SysFont("comicsansms", 15, True)

        # Display a message on the screen
        text = font.render("Press Any key to continue", True, (255, 255, 255))
        win.blit(text, (200- text.get_width() / 2, 400 - text.get_height() / 2))
        pygame.display.update()
        pygame.event.clear()
        pygame.event.wait()
        while pygame.event.peek(pygame.KEYUP):
            pygame.event.wait()



    def highscore(self, count, win):
        font = pygame.font.SysFont("arial", 20)
        text = font.render("Score : " + str(count), True, self.white)
        win.blit(text, (0, 0))

    def update(self,win):
        global crash2
        global crash1
        self.rect = (self.x, self.y, self.width, self.height)
        if crash2 == 1:
          self.display_message("you win!!",win)
          crash2=0
          crash1=0
          font = pygame.font.SysFont("comicsansms", 15, True)

          # Display a message on the screen
          text = font.render("Press Any key to continue", True, (255, 255, 255))
          win.blit(text, (200- text.get_width() / 2, 400 - text.get_height() / 2))
          pygame.display.update()
          pygame.event.clear()
          pygame.event.wait()
          while pygame.event.peek(pygame.KEYUP):
              pygame.event.wait()






def read_pos(str):
    str=str.split(",")
    return int(str[0]), int(str[1]), int(str[2]), int(str[3])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2])+ "," + str(tup[3])


def redrawWindow(win, player, player2):
    player.draw(win)
    player2.draw(win)
    pygame.display.update()


def main():
    global crash2
    global crash1

    run = True
    n = network()
    car_image = r"E:\Semseter 8\Distributed Computing\Project\img\car.png"
    car_image2 = r"E:\Semseter 8\Distributed Computing\Project\img\enemy_car_2.png"
    bg_img = pygame.image.load(r"E:\Semseter 8\Distributed Computing\Project\img\White-broken-lines.png")
    scaled_image = pygame.transform.scale(bg_img, (360, 650))
    if r.exists("game_data"):
        dataa=r.hgetall("game_data")
        p=Player(int(data["x"],int(data["y"],49,100,car_image2,scaled_image)))
        p.enemy_car_startx = int(data['start_x'])
        p.enemy_car_starty = int(data['start_y'])
        p.count = int(data['score'])
        p.bg_img_speed = float(data['bg_speed'])
        p.enemy_car_speed = float(data['enemy_speed'])
        p.enemy_car_startx = int(data['enemy_start_x'])
        p.enemy_car_starty = int(data['enemy_start_y'])

    #p = Player(50, 500, 49, 100, car_image2, scaled_image)
    p2 = Player(0,0, 49, 100, car_image, scaled_image)
    clock=pygame.time.Clock()
    space_click=0
    ready1 = 0
    xc = 0
    yc = height_dis  // 2
    vel_x = 1.5
    vel_y = 0
    while run:

      clock.tick(100)
      win.fill((202, 228, 241))
      font = pygame.font.SysFont("comicsans", 20)
      text = font.render("Press Space to play!", 1, (58,78, 91))
      text2= font.render("Press Escape to exit!", 1, (58,78, 91))
      win.blit(text, (80, 200))
      win.blit(text2, (80, 600))
      pygame.display.update()
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
             run = False
        if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_ESCAPE:
                 run = False
           if event.key == pygame.K_SPACE:
               space_click=1
      while space_click:
          p2Pos = read_pos(n.send(make_pos((p.x, p.y, crash1, ready1))))
          p2.x = p2Pos[0]
          p2.y = p2Pos[1]
          crash2 = p2Pos[2]
          ready2= p2Pos[3]
          p2.update(win)

          if ready2==1:
           p.move(win)
           redrawWindow(win, p, p2)
          else :
              image3 = pygame.image.load(r"E:\Semseter 8\Distributed Computing\Project\img\a6rBl.png")
              scaled_image = pygame.transform.scale(image3, (10, 15))
              image_rect = scaled_image.get_rect()
              font = pygame.font.SysFont("comicsansms", 20, True)
              text1 = font.render("waiting for other player", True, (8,78, 91))
              xc += vel_x
              yc+= vel_y
              if xc > width_dis:
                  xc = -image_rect.width
              #
              win.fill((202, 228, 241))
              win.blit(image3, (xc, yc))
              win.blit(text1, (155 - text.get_width() // 2, 100 - text.get_height() // 3))
              pygame.display.flip()


          for event in pygame.event.get():
            if event.type == pygame.QUIT:
                space_click=0
                run = False





main()