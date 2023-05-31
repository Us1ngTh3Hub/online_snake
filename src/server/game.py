import random
import server

# Game window dimensions
window_width = 800
window_height = 600

# Snake settings
block_size = 20
snake_speed = 10

class Snake:
    def __init__(self, x, y, color):
        #adding first segment for the snake
        self.snake_segments = [(x, y)]
        #starting direction for the snake
        self.direction = "RIGHT" 
        self.color = color

    #moves the snake in the designated direction
    def move(self):
        x, y = self.snake_segments[0]

        if self.direction == "UP":
            y -= block_size
        elif self.direction == "DOWN":
            y += block_size
        elif self.direction == "LEFT":
            x -= block_size
        elif self.direction == "RIGHT":
            x += block_size

        self.snake_segments.insert(0, (x, y))
        self.snake_segments.pop()

    #used to change the direction of the snake. Applies rules for movement
    #can't move in the opposite direction it is heading to now
    def change_direction(self, new_direction):
        if (new_direction == "UP" and self.direction != "DOWN") or \
                (new_direction == "DOWN" and self.direction != "UP") or \
                (new_direction == "LEFT" and self.direction != "RIGHT") or \
                (new_direction == "RIGHT" and self.direction != "LEFT"):
            self.direction = new_direction

class Food:
    def __init__(self):
        #adds new food at random location
        self.x = random.randint(0, (window_width - block_size) // block_size) * block_size
        self.y = random.randint(0, (window_height - block_size) // block_size) * block_size

class Snakegame:
    def __init__(self):
        #adds needed variables + first food
        self.player_snake = [None, None] #Snake(0, 0, green)  Snake(0, 3, blue)
        self.player_controller = [None, None]
        self.player_address = [None, None]
        self.food = Food()

    def startgame(self):
        self.message = [None, None]
        self.game_over = False
        self.game_quit = False
        self.score = 0
        #wait till the game actually has players
        while self.player_controller[0] == None:
            print('No Player yet')
        while not self.game_quit:
            while self.game_over:
                self.game_over_message()
                exit()

            #looks for changes from player 1
            msg = self.message[0]
            if(msg == b'UP'):
                self.player_snake[0].change_direction("UP")
            elif(msg == b'DOWN'):
                self.player_snake[0].change_direction("DOWN")
            elif(msg == b'LEFT'):
                self.player_snake[0].change_direction("LEFT")
            elif(msg == b'RIGHT'):
                self.player_snake[0].change_direction("RIGHT")
            elif(msg == b'quit'):
                self.game_quit = True

            #looks for changes from player 2
            if(self.player_controller[1]):
                msg = self.message[1]
                if(msg == b'UP'):
                    self.player_snake[1].change_direction("UP")
                elif(msg == b'DOWN'):
                    self.player_snake[1].change_direction("DOWN")
                elif(msg == b'LEFT'):
                    self.player_snake[1].change_direction("LEFT")
                elif(msg == b'RIGHT'):
                    self.player_snake[1].change_direction("RIGHT")
                elif(msg == b'quit'):
                    self.game_quit = True

            # Move the snakes
            self.player_snake[0].move()
            if self.player_snake[1]:
                self.player_snake[1].move()

            # Check if the snakes collided with the boundaries or themselves
            if any(segment in self.player_snake[0].snake_segments[1:] for segment in self.player_snake[0].snake_segments[0]) or \
                    self.player_snake[0].snake_segments[0][0] < 0 or \
                    self.player_snake[0].snake_segments[0][0] >= window_width or \
                    self.player_snake[0].snake_segments[0][1] < 0 or \
                    self.player_snake[0].snake_segments[0][1] >= window_height:
                self.game_over = True

            if self.player_snake[1] and (
                    any(segment in self.player_snake[1].snake_segments[1:] for segment in self.player_snake[1].snake_segments[0]) or
                    self.player_snake[1].snake_segments[0][0] < 0 or
                    self.player_snake[1].snake_segments[0][0] >= window_width or
                    self.player_snake[1].snake_segments[0][1] < 0 or
                    self.player_snake[1].snake_segments[0][1] >= window_height):
                self.game_over = True

            # Check if the snakes ate the food
            if self.player_snake[0].snake_segments[0][0] == self.food.x and self.player_snake[0].snake_segments[0][1] == self.food.y:
                self.player_snake[0].snake_segments.append((self.food.x, self.food.y))
                self.score += 1
                self.food = Food()
                if(self.player_controller[1]!=None):
                    server.send(self.player_controller[1], self.player_address[1],"Food:"+str(self.x)+":"+str(self.y))
                server.send(self.player_controller[0], self.player_address[0],"Food:"+str(self.x)+":"+str(self.y))

            if self.player_snake[1] and self.player_snake[1].snake_segments[0][0] == self.food.x and self.player_snake[1].snake_segments[0][1] == self.food.y:
                self.player_snake[1].snake_segments.append((self.food.x, self.food.y))
                self.score += 1
                self.food = Food()
                if(self.player_controller[1]!=None):
                    server.send(self.player_controller[1], self.player_address[1],"Food:"+str(self.x)+":"+str(self.y))
                server.send(self.player_controller[0], self.player_address[0],"Food:"+str(self.x)+":"+str(self.y))

            #tells clients the score and state of game
            self.display_score(self.score)
            for segment in self.player_snake[0].snake_segments:
                server.send(self.player_controller[0], self.player_address[0],"Snake:"+str(segment[0])+":"+str(segment[1]))
            if(self.player_snake[1]):
                for segment in self.player_snake[1].snake_segments:
                    server.send(self.player_controller[1], self.player_address[1],"Snake:"+str(segment[0])+":"+str(segment[1]))
            
    # Function to send score to the clients
    def display_score(self, score):
        if(self.player_controller[1]!=None):
            server.send(self.player_controller[1], self.player_address[1],str(score))
        server.send(self.player_controller[0], self.player_address[0],str(score))

    # Function to send "Game Over" message
    def game_over_message(self):
        if(self.player_controller[1]!=None):
            server.send(self.player_controller[1], self.player_address[1],'Game Over')
        server.send(self.player_controller[0], self.player_address[0],'Game Over')
