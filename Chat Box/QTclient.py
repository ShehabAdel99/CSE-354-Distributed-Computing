import sys
import threading
import socket
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor, QPalette
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title and icon
        self.setWindowTitle("Racing Game Chat Room")
        self.setWindowIcon(QIcon("racing_icon.png"))

        # Set the background color of the window
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#333"))
        self.setPalette(palette)

        # Create a main widget and set a layout for it
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        layout.setAlignment(Qt.AlignTop)

        # Create a text edit widget to display the chat messages
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setStyleSheet("""
            QTextEdit {
                background-color: #f7f7f7;
                border: 10px solid #999;
                color: #333;
                font-size: 14px;
                font-family: Arial;
            }
        """)

        # Add the text edit to the layout
        layout.addWidget(self.text_edit)

        # Create a widget for the chat input field and send button
        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)
        input_layout.setAlignment(Qt.AlignTop)

        # Create a text edit widget for the chat input field
        self.input_edit = QTextEdit()
        self.input_edit.setFixedHeight(50)
        self.input_edit.setStyleSheet("""
            QTextEdit {
                background-color: #f7f7f7;
                border: 8px solid #999;
                color: #333;
                font-size: 14px;
                font-family: Arial;
            }
        """)

        # Add the input edit to the layout
        input_layout.addWidget(self.input_edit)

        # Create a send button
        self.send_button = QPushButton("Send 🏎")
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                border: 2px solid #007bff;
                border-radius: 15px;
                color: #fff;
                font-size: 16px;
                font-family: Arial;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #0069d9;
                border: 2px solid #0062cc;
            }
            QPushButton:pressed {
                background-color: #0062cc;
                border: 2px solid #005cbf;
            }
        """)
        # Connect the send button to the send function
        self.send_button.clicked.connect(self.send)

        # Add the send button to the layout
        input_layout.addWidget(self.send_button)

        # Add the input widget to the main layout
        layout.addWidget(input_widget)

        # Set the central widget of the main window
        self.setCentralWidget(main_widget)

        # Create a socket connection to the server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('192.168.1.3', 50174))

        # Create a thread to receive messages from the server
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

    def send(self):
        # Get the message from the input field
        message = self.input_edit.toPlainText()

        # Clear the input field
        self.input_edit.clear()

        # Display the message in the chat window
        self.text_edit.append(message)

        # Send the message to the server
        self.client_socket.send(bytes(message, "utf8"))

        # Play a revving engine sound effect
        engine_sound = QSound("car_sound.wav")
        engine_sound.play()

        # If the message is "{quit}", close the socket and quit the application
        if message == "{quit}":
            self.client_socket.close()
            self.close()

    def receive(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                self.text_edit.append(message)
            except:
                print('Error!')
                self.client_socket.close()
                self.close()
                break


if __name__ == "__main__":
    # Create the application and main window
    app = QApplication(sys.argv)
    main_window = MainWindow()

    # Set the size and position of the main window
    main_window.setGeometry(100, 100, 600, 400)

    # Show the main window
    main_window.show()

    # Run the application event loop
    sys.exit(app.exec_())