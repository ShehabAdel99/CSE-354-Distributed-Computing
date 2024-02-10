
# Car-Racer 🚗 -Distributed-Computing-Project 

Car-Racer is an exhilarating distributed computing project developed using Python's Pygame library. This high-speed racing game pits players against each other in a race to achieve the highest score while dodging obstacles and rival drivers. Featuring real-time communication via a built-in chat room, Car-Racer delivers an immersive gaming experience that transcends geographical boundaries.

## Project Scope
Car-Racer is a client-server architecture-based game that allows players to compete against each other over a network. It offers fast-paced racing action with two players, each navigating their cars through challenging obstacles to secure victory. The game's chat feature enhances player interaction, adding an extra layer of excitement to the gameplay.

## Key Features
- Real-time multiplayer racing action.
- Interactive chat room for communication between players.
- Smooth gameplay experience powered by Pygame.
- Customizable game settings and controls.
- Database integration for storing player scores and locations using MongoDB hosted on Amazon AWS instances.
- Dynamic graphics and sound effects for an immersive gaming atmosphere.

## Technical Details and System Architecture
Car-Racer's architecture is designed to offer a seamless gaming experience, with the server managing game state and communication between players. The use of MongoDB, hosted on Amazon AWS instances, enables efficient storage and retrieval of player data, while Pygame provides the framework for graphics and gameplay mechanics.



## Gameplay overview 🎮 
Players enter the game lobby and click the spacebar to play, then they wait for the other player to join the game. Once both players have joined, they start the race together and try to avoid collisions with enemy cars to increase their score.

The game also features a chat room that players can access at any time by pressing the "C" button before or during the game.

If a player collides with an enemy car, they lose the race and the other player wins. However, they can play again without having to exit the game.

The race continues until one of the players reaches the finish line, and the winner is declared
## Controls 🕹️

<ul>
  <li>Arrow Up: Move Forward</li>
  <li>Arrow Down: Move Downward</li>
  <li>Arrow Right: Move Right</li>
  <li>Arrow Left: Move Left</li>
</ul>

## Screenshots 📷

| Screenshot 1 | Screenshot 2 | Screenshot 3 |
|--------------|--------------|--------------|
| <img src="Screenshots/Screenshot 1.png" width="250" height="250"> | <img src="Screenshots/Screenshot 2.png" width="450"> | <img src="Screenshots/Screenshot 3.png" width="450"> |

| Screenshot 4 | Screenshot 5 | Screenshot 6|
|--------------|--------------|--------------|
| <img src="Screenshots/Screenshot 4.png" width="250"> | <img src="Screenshots/Screenshot 5.png" width="450"> | <img src="Screenshots/Screenshot 6.png" width="450"> |

## Demo 🎥

[![Video Demo](https://img.youtube.com/vi/OYNIrqZUx9Y/0.jpg)](https://www.youtube.com/watch?v=OYNIrqZUx9Y "Car Racer2D")

## Getting Started 💻


<ol>
  <li>Install pycharm Compiler or any python compiler </li>
  <li>install pygame library</li>
  <li>Run server.py</li>
  <li>Run game & chat.py</li>
</ol>

## Important Note 📝
Make sure that you connect the your instance, you can use ubuntu linux virtual machine 
## Included Libraries 📚

<ul>
  <li>import pygame</li>
  <li>import threading</li>
  <li>import socket</li>
  <li>import time</li>
  <li>import tkinter</li>
  <li>import winsound</li>
  <li>import random</li>
  <li>from time import sleep</li>
 
</ul>

## Conclusion
Car-Racer showcases the power of Pygame, Python, distributed computing, and cloud services in game development. Its immersive gameplay, real-time communication, and database integration make it a standout project in the gaming community. Whether you're a player looking for thrilling racing action or a developer seeking insights into game development, Car-Racer has something to offer for everyone.

## Authors
- Shehab Adel Ramadan
- Amr Essam Kamal El-din
- Omar Salah Abdelkader
- Mohamed Reda Mohamed

# Have Fun! 🚀
