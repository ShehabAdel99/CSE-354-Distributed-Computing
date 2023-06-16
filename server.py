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
game_db =game_db.game
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
tup1=()
tup2=()
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
    information1 = [50, 500, 0, 0]
    information={
        "x1":information1[0],
        "y1":information1[1],
        "crash1":information1[2],
        "ready1":information1[3]

    }
    game_db.insert_one(information)



insert_player1_info()

def insert_player2_info():
    information2 = [200,500,0,0]
    information={
        "x2":information2[0],
        "y2":information2[1],
        "crash2":information2[2],
        "ready2":information2[3]
    }
    game_db.insert_one(information)



insert_player2_info()


def get_person_by_id(person_id):
    from bson.objectid import ObjectId
    _id = ObjectId(person_id)
    res = game_db.find_one({"_id": _id})
    return res


def threaded_client(conn,player_id):
    player_info = game_db.find_one({"_id": ObjectId(player_id)})
    if player_info:
        if player_info.get('x2') is not None:
            # Player 2
            info = (player_info['x2'], player_info['y2'], player_info['crash2'], player_info['ready2'])
        else:
            # Player 1
            info = (player_info['x1'], player_info['y1'], player_info['crash1'], player_info['ready1'])
    conn.send(str.encode(make_pos(info)))
    reply=""




    while True:
        try:
            data=read_pos(conn.recv(4096).decode())
            if(player == 0):
                tup1=data
                game_db.update_one({"_id": ObjectId(player_id)},{"$set": {"x1": (tup1[0])}})
                game_db.update_one({"_id": ObjectId(player_id)},{"$set": {"y1": (tup1[1])}})
                game_db.update_one({"_id": ObjectId(player_id)},{"$set": {"crash1": (tup1[2])}})
                game_db.update_one({"_id": ObjectId(player_id)},{"$set": {"ready1": (tup1[3])}})

                #pos1= get_person_by_id("648baafce1784ec7f4592892")
                #pos1=data
                # updated_pos1=data

                #updated_pos1=data
            elif(player==1):
                  tup2=data
                  game_db.update_one({"_id": ObjectId(player_id)},{"$set": {"x2":tup2[0]}})
                  game_db.update_one({"_id": ObjectId(player_id)},{"$set": {"y2":tup2[1]}})
                  game_db.update_one({"_id": ObjectId(player_id)},{"$set": {"crash2":tup2[2]}})
                  game_db.update_one({"_id": ObjectId(player_id)},{"$set": {"ready2":tup3[3]}})

                #pos2=get_person_by_id("648babb6a63e936ac6370be7")
                #pos2=data
                #updated_p2=data
            #pos[player]=data # hena ha7ot l data 3ala hasab anhy player

            if not data:
                print("Disconnected")
                break
            else:
                var1 = game_db.find_one({"_id": ObjectId(player_id)}, {"crash1"})
                var2 = game_db.find_one({"_id": ObjectId(player_id)}, {"crash2"})
                if player ==1 and var1==1:  # pos[0][2]==1: # hatly mn player 0 hwa crashed wla la
                    game_db.update_one({"_id": ObjectId(player_id)},{"$set": {"ready2":0}})   # hakhaly l flag bta3 ready bta3 player 1 = 0
                    reply = game_db.find_one({"_id": ObjectId(player_id)})  #pos[0] # hgeb l information bta3t player 0 w a7otaha fe reply
                elif player ==0 and var2==1:
                    game_db.update_one({"_id": ObjectId(player_id)}, {"$set": {"ready1": 0}})
                    reply = game_db.find_one({"_id": ObjectId(player_id)})
                elif player ==1:
                    game_db.update_one({"_id": ObjectId(player_id)}, {"$set": {"ready2": 1}})   #   pos[1] = (*pos[1][:3], 1)
                    reply = game_db.find_one({"_id": ObjectId(player_id)})   #pos[0]
                else:
                    game_db.update_one({"_id": ObjectId(player_id)}, {"$set": {"ready1": 1}})    #     pos[0] = (*pos[0][:3], 1)
                    reply =game_db.find_one({"_id": ObjectId(player_id)}) #     pos[1]



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