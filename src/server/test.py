import game
import headercreator
import server
import threading

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
color = [blue, green]

#tests the snake creation and wether it is able to move and change direction
def test_Snake():
    Snake = game.Snake(1,2,blue)
    if(Snake.color == blue
       and Snake.snake_segments[0][0]==1
       and Snake.snake_segments[0][1]==2):
        Snake.move()
        if(Snake.snake_segments[0][0]==1+20
            and Snake.snake_segments[0][1]==2):
            Snake.change_direction("LEFT")
            if(Snake.direction == "RIGHT"):
                Snake.change_direction("UP")
                if(Snake.direction == "UP"):
                    return 1
    return -1

#tests wether the game can start
#for further tests a client will be needed
def test_game():
    try:
        Snakegame = game.Snakegame()
        gamethread = threading.Thread(target=Snakegame.startgame)
        gamethread.start()
    except:
        return -1
    return 1

#tests if a header can be compiled and decompiled
def test_headercreator():
    test = [1234,4321,10,42]
    header = headercreator.create_udp_header(test[0],test[1],test[2],test[3])
    unpheader = headercreator.unpack_header(header)
    if(unpheader[i] == test[i] for i in range(4)):
        return 1
    return -1

#for testing further a working client will be needed
def test_server():
    split = server.split_into_fixed_parts(b'Hello you!',2)
    if(split[0]==b'He'
       and split[1]==b'll'
       and split[2]==b'o '
       and split[3]==b'yo'
       and split[4]==b'u!'):
        return 1
    return -1

if __name__ ==  '__main__':
    try:
        if(test_game() == 1
           and test_headercreator() == 1
           and test_server() == 1
           and test_server() == 1):
            print("Tests Passed")
        else:
            print("Tests Failed")
    except:
        print("Tests Failed")