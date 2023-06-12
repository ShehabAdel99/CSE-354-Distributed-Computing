import threading
import socket
import tkinter as tk
import winsound
import pygame
from network import network
import random
from time import sleep



# Create the main window
root = tk.Tk()
root.title("Chat Room")

# Create a frame to hold the chat messages
messages_frame = tk.Frame(root)
scrollbar = tk.Scrollbar(messages_frame)

# This will contain the chat messages
msg_list = tk.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)

# Set the chat bubble appearance
msg_list.config(border=10, highlightthickness=10, relief=tk.FLAT, font=("Arial", 12), justify=tk.LEFT)

# Set the background color and foreground color of the chat bubbles
msg_list.config(bg="#f7f7f7", fg="#333333")

# Set the color of the selection highlight
msg_list.config(selectbackground="#b5d5ff", selectforeground="#333333")

scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
messages_frame.pack()

# Create a frame to hold the entry field and send button
entry_frame = tk.Frame(root)
entry_field = tk.Entry(entry_frame)

# Set the appearance of the entry field
entry_field.config(border=8, highlightthickness=0, relief=tk.FLAT, font=("Arial", 12))

entry_field.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

# Function to handle sending messages from the client to the server
def send(event=None):
    message = entry_field.get()
    entry_field.delete(0, tk.END)
    client_socket.send(bytes(message, "utf8"))
    if message == "{quit}":
        client_socket.close()
        root.quit()

    # Play a revving engine sound effect
    winsound.PlaySound("car_sound.wav", winsound.SND_FILENAME)


# Bind the send function to the Return key
entry_field.bind("<Return>", send)

# Create a button to send messages
send_button = tk.Button(entry_frame, text="Send 🏎", command=send)

# Set the appearance of the send button
send_button.config(border=1, highlightthickness=5, relief=tk.FLAT, font=("Arial", 12), bg="#007bff", fg="#ffffff")

send_button.pack(side=tk.RIGHT)

entry_frame.pack()

# Create a frame to hold the alias label and entry field
alias_frame = tk.Frame(root)
alias_label = tk.Label(alias_frame, text="Enter your Name:")

# Set the appearance of the alias label
alias_label.config(border=10, highlightthickness=0, relief=tk.FLAT,font=("Arial", 12), fg="#333333")

alias_label.pack(side=tk.LEFT)
alias_entry = tk.Entry(alias_frame)

# Set the appearance of the alias entry field
alias_entry.config(border=5, highlightthickness=0, relief=tk.FLAT, font=("Arial", 12))

alias_entry.pack(side=tk.LEFT)
alias_frame.pack()

# Function to get the user's alias and connect to the server
def connect():
    alias = alias_entry.get()
    if alias:
        # Create a socket connection to the server
        global client_socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('192.168.1.5', 59000))
        client_socket.send(bytes(alias, "utf8"))


        # Play a revving engine sound effect
        winsound.PlaySound("engine_sound.wav", winsound.SND_FILENAME)




        # Remove the alias entry fields and connect button
        alias_frame.pack_forget()
        connect_button.pack_forget()

        # Create a button to quit
        quit_button = tk.Button(root, text="Quit 🚪", command=quit)

        # Set the appearance of the quit button
        quit_button.config(border=1, highlightthickness=5, relief=tk.FLAT, font=("Arial", 12), bg="#dc3545", fg="#ffffff")

        quit_button.pack()

        # Function to handle receiving messages from the server and displaying them in the chat window
        def receive():
            while True:
                try:
                    message = client_socket.recv(1024).decode('utf-8')
                    msg_list.insert(tk.END, message)
                except:
                    print('Error!')
                    client_socket.close()
                    root.quit()
                    break

        # Create a thread to receive messages from the server
        receive_thread = threading.Thread(target=receive)
        receive_thread.start()

# Create a button to connect to the server
connect_button = tk.Button(root, text="Connect 🏁", command=connect)

# Set the appearance of the connect button
connect_button.config(border=1, highlightthickness=5, relief=tk.FLAT, font=("Arial", 12), bg="#007bff", fg="#ffffff")

connect_button.pack()

# Function to quit the client's connection to the server
def quit():
    client_socket.send(bytes("{quit}", "utf8"))
    client_socket.close()
    root.quit()

# Start the GUI main loop
def runChat() :
    root.mainloop()


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
    def __init__(self, x, y, width, height, car_image, bg_image):
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


# Create a new thread for the chat box and start it
chat_box_thread = threading.Thread(target=ChatBox, args=(root, "192.168.1.5", 59000))
chat_box_thread.start()

# Start the game loop
run_game()
root.mainloop()