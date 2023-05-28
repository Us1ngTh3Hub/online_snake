# online_snake
This is the repository for an online multiplayer snake game, including a network library extending the UDP standard.

## structure
The project consists of 3 modules. The client application, which registers user input and displays the game, the server application, which processes the input of multiple client applications to update the game and finally a network library, which is based on UDP and connects the server and client application.

## network library
The network library should implement a standard used by both client and server. This standard extends UDP and needs to meet the following specifications:
- Establish connection and initial client identification
- Timeout-recognition
- Keep-alive packets between client and server
- Own packet logic which allows sending of data streams
- CRC for error recognition

## client application
The client application is responsible for collecting user input (the direction of the snake) and sending that input to the server, using the aforementioned network library. It also has to be able to display the game returned from the server. In order to accomplish this task, the client application has to run in 2 threads. One thread is responsible for the sending and receiving of keep-alive packets, while the second thread collects the user input, sends that to the server and receives information to display the game. Finally the client application should print the game.

## server application
The server application is working similar to the client application. However, it communicates with several clients at the same time. There are still 2 threads needed. While the firist thread is again responsible for transmitting and receiving keep-alive packets, this time to and from different sockets, the second thread acts as the backend of the game. It takes the user input, transmitted by the client, and from that calculates the position of the snakes and sends that back to the client. It also randomly generates te position of an apple and checks for collisions between either a player and the apple or between different players.

## game parameters
The playing field will be displayed in the terminal and has a width of 32 characters and a height of 16. The snakes will be 3 characters long in the beginning. There will always be one apple at a time, with two players contending for it.
