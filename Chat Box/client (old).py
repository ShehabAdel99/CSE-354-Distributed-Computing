import threading
import socket
import tkinter as tk
# import pyqt5
# Create the main window
root = tk.Tk()
root.title("Chat Room")

# Create a frame to hold the chat messages
messages_frame = tk.Frame(root)
scrollbar = tk.Scrollbar(messages_frame)

# This will contain the chat messages
msg_list = tk.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
msg_list.pack()
messages_frame.pack()

# Create a frame to hold the entry field and send button
entry_frame = tk.Frame(root)
entry_field = tk.Entry(entry_frame)
entry_field.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

# Function to handle sending messages from the client to the server
def send(event=None):
    message = entry_field.get()
    entry_field.delete(0, tk.END)
    client_socket.send(bytes(message, "utf8"))
    if message == "{quit}":
        client_socket.close()
        root.quit()

# Bind the send function to the Return key
entry_field.bind("<Return>", send)

# Create a button to send messages
send_button = tk.Button(entry_frame, text="Send", command=send)
send_button.pack(side=tk.RIGHT)

entry_frame.pack()

# Create a frame to hold the alias label and entry field
alias_frame = tk.Frame(root)
alias_label = tk.Label(alias_frame, text="Enter your alias:")
alias_label.pack(side=tk.LEFT)
alias_entry = tk.Entry(alias_frame)
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

        # Remove the alias entry fields and connect button
        alias_frame.pack_forget()
        connect_button.pack_forget()

        # Create a button to quit
        quit_button = tk.Button(root, text="Quit", command=quit)
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
connect_button = tk.Button(root, text="Connect", command=connect)
connect_button.pack()

# Function to quit the client's connection to the server
def quit():
    client_socket.send(bytes("{quit}", "utf8"))
    client_socket.close()
    root.quit()

# Start the GUI main loop
root.mainloop()