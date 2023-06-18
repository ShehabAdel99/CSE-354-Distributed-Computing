import socket
from _thread import *
import threading
import pygame
import sys
from dotenv import load_dotenv , find_dotenv
import os
load_dotenv(find_dotenv())
from pymongo import MongoClient
lock = threading.Lock()
password = os.environ.get("MONGODB_PWD")
connection_string=f"mongodb+srv://melshafaie123:{password}@game.czsmeor.mongodb.net/?retryWrites=true&w=majority"
client=MongoClient(connection_string)
server="192.168.1.9"
port=5555
# client = MongoClient(connection_string)
db = client["game_database"]
collection = db["game_state"]

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
def read_pos(str):
     str=str.split(",")
     return int(str[0]), int(str[1]), int(str[2]), int(str[3]), int(str[4])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2]) + "," + str(tup[3])+ "," + str(tup[4])
pos=[(50,500,0,0,0),(200,500,0,0,0)]
try:
    s.bind((server,port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection")

game_state_structure = {
    "game_id": "my_game",
    "pos": [
        (),
        ()
    ],
    "discar":0,
    "count":0,

}
collection.delete_one({"game_id": "my_game"})

currentPlayer = 0
def threaded_client(conn, player):
    global pos
    count=0
    global currentPlayer
    # Load the game state from MongoDB
    game_state = collection.find_one({"game_id": "my_game"})

    print(game_state)

    if game_state:
        count+=1

    conn.send(str.encode(make_pos(pos[player])))

    reply = ""
    while True:
        try:

            data = read_pos(conn.recv(4096).decode())


            pos[player] = data

            if not data:
                currentPlayer = player

                print("Player disconnected")
                # Update the game state in the database

                game_state = {"game_id": "my_game", "pos": pos,"discar":player}
                collection.replace_one({"game_id": "my_game"}, game_state, upsert=True)

                break
            else:
                print("REDA2")
                if player == 1 and pos[0][2] == 1:
                    pos[1] = (*pos[1][:4], 0)
                    reply = pos[0]
                elif player == 0 and pos[1][2] == 1:
                    pos[0] = (*pos[0][:4], 0)
                    reply = pos[1]
                elif player == 1 and pos[1][4]==0:
                    pos[1] = (*pos[1][:4], 1)
                    reply = pos[0]
                elif player == 0 and pos[0][4]==0:
                    pos[0] = (*pos[0][:4], 1)
                    reply = pos[1]
                elif player == 1:
                     reply = pos[0]
                else:
                     reply = pos[1]


                print("Received :", reply)
                print("Sending :", reply)

                conn.sendall(str.encode(make_pos(reply)))




        except:
            currentPlayer=player

            print("Player disconnected")
            # Update the game state in the database
            game_state = {"game_id": "my_game", "pos": pos,"discar":player}
            collection.replace_one({"game_id": "my_game"}, game_state, upsert=True)
            break

    print("lost connection")
    conn.close()



while True:

    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, currentPlayer))
    if currentPlayer < 1:
        currentPlayer += 1