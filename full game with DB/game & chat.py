import threading
import socket
import time
import tkinter as tk
import winsound
import pygame
from network import network
import random
from time import sleep
from dotenv import load_dotenv , find_dotenv
import os
load_dotenv(find_dotenv())
from pymongo import MongoClient
from pygame.locals import *

password = os.environ.get("MONGODB_PWD")
connection_string=f"mongodb+srv://melshafaie123:{password}@game.czsmeor.mongodb.net/?retryWrites=true&w=majority"
client=MongoClient(connection_string)
db = client["game_database"]
collection = db["game_state"]


global client_socket

#chat code
def chat_window():
    # Create the main window
    root = tk.Tk()
    root.title("Racer Chat")

    # Set the window icon
    root.iconbitmap("racer.ico")

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
    send_button.config(border=1, highlightthickness=5, relief=tk.FLAT, font=("Arial", 12), bg="#007bff", fg="#ffffff",
                       cursor="hand2")

    send_button.pack(side=tk.RIGHT)

    entry_frame.pack()

    # Create a frame to hold the alias label and entry field
    alias_frame = tk.Frame(root)
    alias_label = tk.Label(alias_frame, text="Enter your Name:")
    # Set the appearance of the alias label
    alias_label.config(border=10, highlightthickness=0, relief=tk.FLAT, font=("Arial", 12), fg="#333333")
    alias_label.pack(side=tk.LEFT)
    alias_entry = tk.Entry(alias_frame)
    # Set the appearance of the alias entry field
    alias_entry.config(border=5, highlightthickness=0, relief=tk.FLAT, font=("Arial", 12))
    alias_entry.pack(side=tk.LEFT)
    alias_frame.pack()

    # Function to get the user's alias and connect to the server
    def connect():
        global alias
        alias = alias_entry.get()
        if alias:
            # Create a socket connection to the server
            global client_socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('192.168.1.74', 50000))
            client_socket.send(bytes(alias, "utf8"))
            # Play a revving engine sound effect
            winsound.PlaySound("engine_sound.wav", winsound.SND_FILENAME)
            # Remove the alias entry fields and connect button
            alias_frame.pack_forget()
            connect_button.pack_forget()
            # Create a button to quit
            quit_button = tk.Button(root, text="Quit 🚪", command=quit)
            # Set the appearance of the quit button
            quit_button.config(border=1, highlightthickness=5, relief=tk.FLAT, font=("Arial", 12), bg="#dc3545",
                               fg="#ffffff", bd=1, activebackground="#c82333", activeforeground="#ffffff",
                               cursor="hand2")

            quit_button.pack()

            # Function to handle receiving messages from the server and displaying them in the chat window
            def receive():
                while True:
                    try:
                        message = client_socket.recv(1024).decode('utf-8')

                        # Determine if the message was sent by the client or received from the server
                        if message.startswith(alias):
                            # Format the message as sent by the client
                            # message = message[len(alias) + 1:]  # Remove the alias prefix from the message
                            if message.endswith("connected!"):
                                msg_list.insert(tk.END, message)
                                msg_list.itemconfig(tk.END, fg="blue")
                            else:
                                parts = message.split(':')
                                parts[0] = "You "
                                message = ':'.join(parts)
                                msg_list.insert(tk.END, message)
                                msg_list.itemconfig(tk.END, fg="blue")
                        else:
                            # Format the message as received from the server
                            msg_list.insert(tk.END, message)
                            msg_list.itemconfig(tk.END, fg="green")
                    except Exception as e:
                        print('Error:', e)
                        client_socket.close()
                        root.quit()
                        break

            # Create a thread to handle receiving messages from the server
            receive_thread = threading.Thread(target=receive)
            receive_thread.start()

    # Create a button to connect to the server
    connect_button = tk.Button(root, text="Connect 🚀", command=connect)

    # Set the appearance of the connect button
    connect_button.config(border=1, highlightthickness=5, relief=tk.FLAT, font=("Arial", 12), bg="#28a745",
                          fg="#ffffff",
                          bd=1, activebackground="#218838", activeforeground="#ffffff", cursor="hand2")

    connect_button.pack()

    # Function to quit the program and close the socket connection
    def quit():
        client_socket.send(bytes("{quit}", "utf8"))
        client_socket.close()
        root.quit()

    root.protocol("WM_DELETE_WINDOW", quit)

    # Start the GUI event loop
    root.mainloop()


#game code

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
count=0
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
        self.highscore(count, win)

    def draw(self, win):
        win.blit(self.car_image, self.rect)
    def car(self, x, y,win):
        win.blit(self.car_image, (x, y))

    def move(self, win):
        global crash1
        global ready1
        global count
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




        count += 1
        if (count % 10000 == 0):
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
                count = 0
        if self.x < 20 or self.x > 300:
                self.crashed = True
                self.display_message("You lost!", win)
                crash1 = 1
                # ready1=0
                sleep(1)




        self.update()

    def display_message(self, msg, win):
        global count
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
        count = 0

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
    str = str.split(",")
    return int(str[0]), int(str[1]), int(str[2]), int(str[3]), int(str[4])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2]) + "," + str(tup[3]) + "," + str(tup[4])


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



chat_playing = True  # flag to control entering chat while playing

def main():
    global crash2
    global crash1
    global run1
    global ready1
    global count
    global chat_playing

    readye = 0

    n = network()
    car_image = r"D:\Lectures\Senior-1\Semester 8\Distributed\pythonProject\projectDis\img\car.png"
    car_image2 = r"D:\Lectures\Senior-1\Semester 8\Distributed\pythonProject\projectDis\img\enemy_car_2.png"
    bg_img = pygame.image.load(r"D:\Lectures\Senior-1\Semester 8\Distributed\pythonProject\projectDis\img\White-broken-lines.png")
    scaled_image = pygame.transform.scale(bg_img, (360, 650))
    game_state = collection.find_one({"game_id": "my_game"})
    if game_state:
        if game_state["discar"] == 1:
            p = Player(game_state["pos"][1][0], game_state["pos"][1][1], 49, 100, car_image2, scaled_image)
            count = game_state["pos"][1][3]
            p2 = Player(game_state["pos"][0][0], game_state["pos"][0][1], 49, 100, car_image, scaled_image)
        else:
            p = Player(game_state["pos"][0][0], game_state["pos"][0][1], 49, 100, car_image2, scaled_image)
            count = game_state["pos"][0][3]
            p2 = Player(game_state["pos"][1][0], game_state["pos"][1][1], 49, 100, car_image, scaled_image)

    else:
        p = Player(150, 500, 49, 100, car_image2, scaled_image)
        p2 = Player(150, 500, 49, 100, car_image, scaled_image)
    clock = pygame.time.Clock()
    space_click = 0
    xc = 0
    yc = height_dis // 2
    vel_x = 1.5
    vel_y = 0
    white = (255, 255, 255)

    while run1:
        pressed_key2 = 0
        clock.tick(100)
        win.fill((202, 228, 241))
        font = pygame.font.SysFont("Montserrat", 30)
        text = font.render("Press Space to play!", 1, white)
        text2 = font.render("Press Escape to exit!", 1, white)
        text3 = font.render("Press c to chat", 1, white)
        bg_image5 = pygame.image.load(
            r"D:\Lectures\Senior-1\Semester 8\Distributed\pythonProject\projectDis\Wallpaper.jpg")
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
                    space_click = 1
                if event.key == pygame.K_c:
                    chat_thread = threading.Thread(target=chat_window)
                    chat_thread.start()

        while space_click:

            keys = pygame.key.get_pressed()
            if keys[pygame.K_c] and chat_playing == True:
                time.sleep(0.5)  # handling debounce delay of pressing 'c'
                chat_thread = threading.Thread(target=chat_window)
                chat_thread.start()

            p2Pos = read_pos(n.send(make_pos((p.x, p.y, crash1, count, ready1))))
            p2.x = p2Pos[0]
            p2.y = p2Pos[1]
            crash2 = p2Pos[2]
            ready2 = p2Pos[4]

            p2.update()

            if ready2 == 0 and crash2 == 0 and crash1 == 0 and readye == 0:
                image3 = pygame.image.load(r"D:\Lectures\Senior-1\Semester 8\Distributed\pythonProject\projectDis\img\a6rBl.png")
                scaled_image = pygame.transform.scale(image3, (10, 15))
                image_rect = scaled_image.get_rect()
                font = pygame.font.SysFont("comicsansms", 20, True)
                text1 = font.render("waiting for other player", True, white)
                xc += vel_x
                yc += vel_y
                if xc > width_dis:
                    xc = -image_rect.width

                win.fill((135, 206, 250))
                win.blit(image3, (xc, yc))
                win.blit(text1, (155 - text.get_width() // 2, 100 - text.get_height() // 3))
                pygame.display.flip()


            elif ready2 == 1 and crash2 == 1:
                chat_playing = False
                p.display_message("you win!!", win)
                win.fill((202, 228, 241))
                font = pygame.font.SysFont("comicsans", 20)
                text = font.render("Press Space to play again! ", 1, (58, 78, 91))
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
                                chat_playing = True
                                pressed_key2 = 1
                                readye = 0

                                space_click = False

                            if event.key == pygame.K_c:
                                chat_thread = threading.Thread(target=chat_window)
                                chat_thread.start()



            elif ready2 == 1 and crash1 == 1:
                chat_playing = False
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
                                chat_playing = True
                                crash1 = 0
                                pressed_key2 = 1
                                ready1 = 0
                                readye = 0

                                space_click = False

                            if event.key == pygame.K_c:
                                chat_thread = threading.Thread(target=chat_window)
                                chat_thread.start()

            elif ready2 == 1 and crash2 == 0:

                p.move(win)
                redrawWindow(win, p, p2)
                readye = 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    space_click = 0
                    run1 = False

if __name__ == "__main__":
    main()