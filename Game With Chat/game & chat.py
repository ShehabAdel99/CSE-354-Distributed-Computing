import threading
import socket
import tkinter as tk
import winsound

# Create a new class for the chat box that inherits from tkinter's Frame class
class ChatBox(tk.Frame):
    def __init__(self, parent, host, port):
        # Initialize the parent Frame object
        super().__init__(parent)

        # Create the socket connection to the server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

        # Create the chat box GUI elements
        self.messages_frame = tk.Frame(self)
        self.scrollbar = tk.Scrollbar(self.messages_frame)
        self.msg_list = tk.Listbox(self.messages_frame, height=15, width=50, yscrollcommand=self.scrollbar.set)
        self.msg_list.config(border=10, highlightthickness=10, relief=tk.FLAT, font=("Arial", 12), justify=tk.LEFT)
        self.msg_list.config(bg="#f7f7f7", fg="#333333")
        self.msg_list.config(selectbackground="#b5d5ff", selectforeground="#333333")
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
        self.messages_frame.pack()
        self.entry_frame = tk.Frame(self)
        self.entry_field = tk.Entry(self.entry_frame)
        self.entry_field.config(border=8, highlightthickness=0, relief=tk.FLAT, font=("Arial", 12))
        self.entry_field.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Bind the send function to the Return key
        self.entry_field.bind("<Return>", self.send)

        # Create a button to send messages
        self.send_button = tk.Button(self.entry_frame, text="Send 🏎", command=self.send)
        self.send_button.config(border=1, highlightthickness=5, relief=tk.FLAT, font=("Arial", 12), bg="#007bff", fg="#ffffff")
        self.send_button.pack(side=tk.RIGHT)
        self.entry_frame.pack()

        # Create a frame to hold the alias label and entry field
        self.alias_frame = tk.Frame(self)
        self.alias_label = tk.Label(self.alias_frame, text="Enter your Name:")
        self.alias_label.config(border=10, highlightthickness=0, relief=tk.FLAT,font=("Arial", 12), fg="#333333")
        self.alias_label.pack(side=tk.LEFT)
        self.alias_entry = tk.Entry(self.alias_frame)
        self.alias_entry.config(border=5, highlightthickness=0, relief=tk.FLAT, font=("Arial", 12))
        self.alias_entry.pack(side=tk.LEFT)
        self.alias_frame.pack()

        # Create a button to connect to the server
        self.connect_button = tk.Button(self, text="Connect 🏁", command=self.connect)
        self.connect_button.config(border=1, highlightthickness=5, relief=tk.FLAT, font=("Arial", 12), bg="#007bff", fg="#ffffff")
        self.connect_button.pack()

        # Create a button to quit
        self.quit_button = tk.Button(self, text="Quit 🚪", command=self.quit)
        self.quit_button.config(border=1, highlightthickness=5, relief=tk.FLAT, font=("Arial", 12), bg="#dc3545", fg="#ffffff")

    # Function to get the user's alias and connect to the server
    def connect(self):
        alias = self.alias_entry.get()
        if alias:
            self.client_socket.send(bytes(alias, "utf8"))
            self.alias_frame.pack_forget()
            self.connect_button.pack_forget()
            self.quit_button.pack()

            # Function to handle receiving messages from the server and displaying them in the chat window
            def receive():
                while True:
                    try:
                    message = self.client_socket.recv(1024).decode('utf-8')
                        self.msg_list.insert(tk.END, message)
                    except:
                        print('Error!')
                        self.client_socket.close()
                        self.quit()

            # Create a thread to receive messages from the server
            self.receive_thread = threading.Thread(target=receive)
            self.receive_thread.start()

    # Function to handle sending messages from the client to the server
    def send(self, event=None):
        message = self.entry_field.get()
        self.entry_field.delete(0, tk.END)
        self.client_socket.send(bytes(message, "utf8"))
        if message == "{quit}":
            self.quit()

    # Function to quit the client's connection to the server
    def quit(self):
        self.client_socket.send(bytes("{quit}", "utf8"))
        self.client_socket.close()
        self.quit_button.pack_forget()
        self.pack_forget()

# Create the main window for the game
root = tk.Tk()
root.title("My Game")

# Create a function to run the game
def run_game():
    # game code goes here
 

# Create a new thread for the chat box and start it
chat_box_thread = threading.Thread(target=ChatBox, args=(root, "192.168.1.5", 59000))
chat_box_thread.start()

# Start the game loop
run_game()
root.mainloop()