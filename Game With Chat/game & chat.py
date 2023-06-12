import threading
import socket
import tkinter as tk
import winsound
import pygame
from network import network
import random
from time import sleep



# Create a new class for the chat box that inherits from tkinter's Frame class
class ChatBox(tk.Frame):
    def _init_(self, parent, chat_host, chat_port):
        # Initialize the parent Frame object
        super()._init_(parent)

        # Create the socket connection to the server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((chat_host, chat_port))

        # Create the chat box GUI elements
        self.messages_frame = tk.Frame(self)
        self.scrollbar = tk.Scrollbar(self.messages_frame)
        self.msg_list = tk.Listbox(self.messages_frame, height=15, width=50, yscrollcommand=self.scrollbar.set)
        self.msg_list.config(border=10, highlightthickness=10, relief=tk.FLAT, font=("Arial", 12), justify=tk.LEFT)
        self.msg_list.config(bg="#f7f7f7", fg="#333333")
        self.msg_list.config(selectbackground="#b5d5ff", selectforeground="#333333")
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
        self.messages_frame.pack()
        self.entry_frame = tk.Frame(self)
        self.entry_field = tk.Entry(self.entry_frame)
        self.entry_field.config(border=8, highlightthickness=0, relief=tk.FLAT, font=("Arial", 12))
        self.entry_field.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Bind the send function to the Return key
        self.entry_field.bind("<Return>", self.send)

        # Create a button to send messages
        self.send_button = tk.Button(self.entry_frame, text="Send 🏎", command=self.send)
        self.send_button.config(border=1, highlightthickness=5, relief=tk.FLAT, font=("Arial", 12), bg="#007bff", fg="#ffffff")
        self.send_button.pack(side=tk.RIGHT)
        self.entry_frame.pack()

        # Create a frame to hold the alias label and entry field
        self.alias_frame = tk.Frame(self)
        self.alias_label = tk.Label(self.alias_frame, text="Enter your Name:")
        self.alias_label.config(border=10, highlightthickness=0, relief=tk.FLAT,font=("Arial", 12), fg="#333333")
        self.alias_label.pack(side=tk.LEFT)
        self.alias_entry = tk.Entry(self.alias_frame)
        self.alias_entry.config(border=5, highlightthickness=0, relief=tk.FLAT, font=("Arial", 12))
        self.alias_entry.pack(side=tk.LEFT)
        self.alias_frame.pack()

        # Create a button to connect to the server
        self.connect_button = tk.Button(self, text="Connect 🏁", command=self.connect)
        self.connect_button.config(border=1, highlightthickness=5, relief=tk.FLAT, font=("Arial", 12), bg="#007bff", fg="#ffffff")
        self.connect_button.pack()

        # Create a button to quit
        self.quit_button = tk.Button(self, text="Quit 🚪", command=self.quit)
        self.quit_button.config(border=1, highlightthickness=5, relief=tk.FLAT, font=("Arial", 12), bg="#dc3545", fg="#ffffff")

    # Function to get the user's alias and connect to the server
    def connect(self):
        alias = self.alias_entry.get()
        if alias:
            self.client_socket.send(bytes(alias, "utf8"))
            self.alias_frame.pack_forget()
            self.connect_button.pack_forget()
            self.quit_button.pack()

            # Function to handle receiving messages from the server and displaying them in the chat window
            def receive():
                while True:
                    try:
                        message = self.client_socket.recv(1024).decode('utf-8')
                        self.msg_list.insert(tk.END, message)
                    except:
                        print('Error!')
                        self.client_socket.close()
                        self.quit()

            # Create a thread to receive messages from the server
            self.receive_thread = threading.Thread(target=receive)
            self.receive_thread.start()

    # Function to handle sending messages from the client to the server
    def send(self, event=None):
        message = self.entry_field.get()
        self.entry_field.delete(0, tk.END)
        self.client_socket.send(bytes(message, "utf8"))
        if message == "{quit}":
            self.quit()

    # Function to quit the client's connection to the server
    def quit(self):
        self.client_socket.send(bytes("{quit}", "utf8"))
        self.client_socket.close()
        self.quit_button.pack_forget()
        self.pack_forget()

chat_root = tk.Tk()
chat_root.title("Chat box")

Chat = ChatBox(chat_root, "192.168.1.5", 59000)

def runChat() :
    Chat.mainloop()


# game code
width_dis = 360
height_dis = 650
win = pygame.display.set_mode((width_dis, height_dis))
pygame.display.set_caption("Client")
vel = 1
clientNumber = 0
crash1=0
crash2=0
ready1=0
ready2=0

class Player():
    def _init_(self, x, y, width, height, car_image, bg_image):
        pygame.init()
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
    return int(str[0]), int(str[1]), int(str[2])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2])


def redrawWindow(win, player, player2):
    player.draw(win)
    player2.draw(win)
    pygame.display.update()



# function to run the game
def run_game():
    global crash2
    global crash1
    global ready2
    global ready1
    run = True
    n = network()
    startPos = read_pos(n.getPos())
    car_image = "img\car.png"
    car_image2 = "img\enemy_car_2.png"
    bg_img = pygame.image.load("img\White-broken-lines.png")
    scaled_image = pygame.transform.scale(bg_img, (360, 650))
    p = Player(startPos[0], startPos[1], 49, 100, car_image2, scaled_image)
    p2 = Player(0, 0, 49, 100, car_image, scaled_image)

    while run:
        p2Pos = read_pos(n.send(make_pos((p.x, p.y, crash1))))
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]
        crash2 = p2Pos[2]

        p2.update(win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move(win)
        redrawWindow(win, p, p2)
    pass


while True:
    # Create a new thread for the chat box and start it
    chat_box_thread = threading.Thread(target=runChat())
    chat_box_thread.start()

    game_thread = threading.Thread(target=run_game())
    game_thread.start()