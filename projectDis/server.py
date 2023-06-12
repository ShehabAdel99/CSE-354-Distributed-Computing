import socket
from _thread import *
import sys


server="192.168.1.9"
port=5555

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

def threaded_client(conn,player):
    conn.send(str.encode(make_pos(pos[player])))
    reply=""


    while True:
        try:
            data=read_pos(conn.recv(2048).decode())
            pos[player]=data

            if not data:
                print("Disconnected")
                break
            else:
                if player ==1:
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