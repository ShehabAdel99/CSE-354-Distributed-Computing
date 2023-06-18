import threading
import socket
from _thread import *
from dotenv import load_dotenv , find_dotenv
import os
load_dotenv(find_dotenv())
from pymongo import MongoClient



password = os.environ.get("MONGODB_PWD")
connection_string=f"mongodb+srv://Shehab_Adel_:{password}@cluster0.euh8kxv.mongodb.net/?retryWrites=true&w=majority"
client=MongoClient(connection_string)
server="172.31.45.134"
port=5555
# client = MongoClient(connection_string)
db = client["game_database"]
collection = db["game_state"]
# Define the server address and port for the chat box server
chat_box_host = "172.31.45.134"
chat_box_port = 50000

# Create a socket connection for the chat box server
chat_box_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
chat_box_server.bind((chat_box_host, chat_box_port))
chat_box_server.listen()

# Lists to hold the clients and their aliases for the chat box server
clients = []
aliases = []

# Function to broadcast messages to all connected clients for the chat box server
def broadcast(message):
    for client in clients:
        client.send(message)

# Function to handle a client connection for the chat box server
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                break
            alias_index = clients.index(client)
            alias = aliases[alias_index]
            # if message.decode('utf-8').startswith('You: '):
            #     broadcast(f'{alias}: {message.decode("utf-8")}'.encode('utf-8'))
            # else:
            broadcast(f'{alias}: {message.decode("utf-8")}'.encode('utf-8'))
        except Exception as e:
            print(f"Error: {e}")
            index = clients.index(client)
            clients.remove(client)
            alias = aliases[index]
            aliases.remove(alias)
            client.close()
            broadcast(f'{alias} has left the chat room!'.encode('utf-8'))
            break

# Function to receive client connections for the chat box server
def receive_chat_box():
    while True:
        print('Chat box server is running and listening ...')
        client, address = chat_box_server.accept()
        print(f'connection is established with {str(address)}')
        # client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024).decode('utf-8')
        aliases.append(alias)
        clients.append(client)
        print(f'The alias of this client is {alias}'.encode('utf-8'))
        broadcast(f'{alias} has connected to the chat room. '.encode('utf-8'))
        client.send('you are now connected!'.encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()






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



def receive_game_server():
    global currentPlayer
    while True:

        conn, addr = s.accept()
        print("Connected to:", addr)
        start_new_thread(threaded_client, (conn,currentPlayer))
        if currentPlayer < 1:
            currentPlayer += 1


# Start the servers
if __name__ == '__main__':
    chat_box_thread = threading.Thread(target=receive_chat_box)
    chat_box_thread.start()

    game_server_thread = threading.Thread(target=receive_game_server)
    game_server_thread.start()