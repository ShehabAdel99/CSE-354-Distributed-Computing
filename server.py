import socket
from _thread import *
import sys

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
import os
import pprint
from pymongo import MongoClient

server="192.168.1.12"
port=5555
password = os.environ.get("MONGODB_PWD")

connection_string = f"mongodb+srv://omaaarsg2001:{password}@cluster0.wfljxfn.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)
dbs = client.list_database_names()
game_db=client.game
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
def read_pos(str):
     str=str.split(",")
     return int(str[0]), int(str[1]), int(str[2]), int(str[3])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2]) + "," + str(tup[3])
pos=[(50,500,0,0),(200,500,0,0)]
try:
    s.bind((server,port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection")



def insert_player1_info():
    p1_information=game_db.game
    information1 = [50, 500, 0, 0]
    information={
        "x":information1[0],
        "y":information1[1],
        "crash":information1[2],
        "ready":information1[3]
    }
    p1_information.insert_one(information)



insert_player1_info()

def threaded_client(conn,player):
    conn.send(str.encode(make_pos(pos[player])))
    reply=""


    while True:
        try:
            data=read_pos(conn.recv(2048).decode())
            pos[player]=data # hena ha7ot l data 3ala hasab anhy player

            if not data:
                print("Disconnected")
                break
            else:
                if player ==1 and pos[0][2]==1: # hatly mn player 0 hwa crashed wla la
                    pos[1] = (*pos[1][:3], 0) # hakhaly l flag bta3 ready bta3 player 1 = 0
                    reply = pos[0] # hgeb l information bta3t player 0 w a7otaha fe reply
                elif player ==0 and pos[1][2]==1:
                    pos[0] = (*pos[0][:3], 0)
                    reply = pos[1]

                elif player ==1:
                    pos[1] = (*pos[1][:3], 1)
                    reply = pos[0]
                else:
                    pos[0] = (*pos[0][:3], 1)
                    reply = pos[1]



                print("Received :",reply)
                print("Sending :", reply)

            conn.sendall(str.encode(make_pos(reply)))
        except:
            break

    print("lost connection")
    conn.close()



currentPlayer = 0
while True:
 conn,addr=s.accept()

 print("Connected to:",addr)
 start_new_thread(threaded_client,(conn,currentPlayer))
 currentPlayer +=1