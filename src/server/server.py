import socket
import headercreator
import threading
import game

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
color = [blue, green]

#funtion to send a message via a given socket to the given address
def send(socket, server_address, _message):
    #forms bitestring from the message for a common format and to make sure it can be send
    encoded_message = _message.encode('utf-8')
    #gets header for information
    header = getheader(encoded_message)
    complete_message = header + encoded_message
    #makes sure to send the message in packages if it is to big
    if(len(complete_message)>1024):
        for part in split_into_fixed_parts(complete_message,1024):
            socket.sendto(part, server_address)
    else:
        socket.sendto(complete_message, server_address)

#returns header from given message
def getheader(self, encoded_message):
    len = len(encoded_message)
    summ = headercreator.calculate_checksum(encoded_message)
    return headercreator.create_udp_header(self.port, self.port, len, summ)

#run to start the server and game
def connect():
    #Setup the game tread
    Snakegame = game.Snakegame()
    gamethread = threading.Thread(target=Snakegame.startgame, args=(client_socket, client_address))
    gamethread.start()

    #opens Port and connects new players
    ip = socket.gethostname()
    port = 42069
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
    sock.bind((ip, port))
    sock.settimeout(5)
    sock.listen(2)
    #counter to check wich player is connecting
    counter = 0
    while True:
        #check if new players want to connect
        client_socket, client_address = sock.accept()
        # Start a new thread to handle the player connection and give information to gamefunktions
        Snakegame.player_controller[counter] = client_socket
        Snakegame.player_address[counter] = client_address
        Snakegame.player_snake[counter] = game.Snake(0, 0, color[counter])
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, Snakegame, counter))
        client_thread.start()
        counter = 1

#funktion to check for messages from the client
def handle_client(client_socket, client_address, game, snake):
    while True:
        try:
            #recieve new messages
            data = client_socket.recv(1024)
            if not data:
                break
            #check header for message length (needed if split in multiple messages)
            header = headercreator.unpack_header(data[:8])
            message = data[8:]
            #Recieve new data until its the supposed length
            while header[2] != len(message):
                data = client_socket.recv(1024)
                message += data
            #update the message for the game thread
            game.message[snake] = message
        except socket.timeout:
            #if the client doesnt send messages for a while send a keepalive for connection upkeep
            send(client_socket, client_address, 'KeepAlive')
    #when done close the connection (needed for raised exceptions that are not handled)
    client_socket.close()
    print("Connection closed for:", client_address)

#splits byte string into parts of part_size
def split_into_fixed_parts(data, part_size):
    num_parts = (len(data) + part_size - 1) // part_size
    return [data[i*part_size:(i+1)*part_size] for i in range(num_parts)]
