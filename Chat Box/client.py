import threading
import socket
import tkinter as tk
import winsound

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
root.mainloop()



#fsvbero;dvshcbwr4;io;ehvgb