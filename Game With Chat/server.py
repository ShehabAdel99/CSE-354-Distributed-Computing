import socket
from _thread import *
import threading
import sys

# Define the server address and port
host = '192.168.1.5'
chat_port = 59000

# Create a socket connection
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, chat_port))
server.listen()

# Lists to hold the clients and their aliases
clients = []
aliases = []

# Function to broadcast messages to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Function to handle a client connection
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat room!'.encode('utf-8'))
            aliases.remove(alias)
            break

# Function to receive client connections
def receive():
    while True:
        print('Server is running and listening ...')
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024).decode('utf-8')
        aliases.append(alias)
        clients.append(client)
        print(f'The alias of this client is {alias}'.encode('utf-8'))
        broadcast(f'{alias} has connected to the chat room'.encode('utf-8'))
        client.send('you are now connected!'.encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

# Start the chat server
    receive()

game_port=5555

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
def read_pos(str):
    str=str.split(",")
    return int(str[0]), int(str[1]),int(str[2])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])+ "," + str(tup[2])
pos=[(50,500,0),(200,500,0)]
try:
    s.bind((host,game_port))
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
                    reply = pos[0]


                else:
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