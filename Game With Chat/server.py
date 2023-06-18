import threading
import socket
from _thread import *


# Define the server address and port for the chat box server
chat_box_host = '172.31.45.134'
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


# Define the server address and port for the game server
server="172.31.45.134"
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
                if player ==1 and pos[0][2]==1:
                    pos[1] = (*pos[1][:3], 0)
                    reply = pos[0]
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

# Function to receive game server connections
def receive_game_server():
    currentPlayer = 0
    while True:
        conn,addr=s.accept()

        print("Connected to:",addr)
        start_new_thread(threaded_client,(conn,currentPlayer))
        currentPlayer +=1


# Start the servers
if __name__ == '__main__':
    chat_box_thread = threading.Thread(target=receive_chat_box)
    chat_box_thread.start()

    game_server_thread = threading.Thread(target=receive_game_server)
    game_server_thread.start()