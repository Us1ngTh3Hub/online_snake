import socket
import pygame
import random
import server

# Initialize Pygame
pygame.init()
player1_controller = server.udpserver()
player2_controller = server.udpserver()

# Game window dimensions
window_width = 800
window_height = 600

# Snake settings
block_size = 20
snake_speed = 10

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Create the game window
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Snake Game")

# Clock for controlling the game's frame rate
clock = pygame.time.Clock()


class Snake:
    def __init__(self, x, y, color):
        self.snake_segments = [(x, y)]
        self.direction = "RIGHT"
        self.color = color

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

    def change_direction(self, new_direction):
        if (new_direction == "UP" and self.direction != "DOWN") or \
                (new_direction == "DOWN" and self.direction != "UP") or \
                (new_direction == "LEFT" and self.direction != "RIGHT") or \
                (new_direction == "RIGHT" and self.direction != "LEFT"):
            self.direction = new_direction

    def draw(self):
        for segment in self.snake_segments:
            if(self.color == blue):
                player2_controller.send(str(segment))
            else:
                player1_controller.send(str(segment))

class Food:
    def __init__(self):
        self.x = random.randint(0, (window_width - block_size) // block_size) * block_size
        self.y = random.randint(0, (window_height - block_size) // block_size) * block_size

    def draw(self):
        if(player2_controller!=None):
            player2_controller.send(str(self.x)+str(self.y))
        player1_controller.send(str(self.x)+str(self.y))

class Snakegame:
    def __init__(self):
        self.food = Food()


    def startgame(self):
        self.message = [None, None]
        while not game_quit:
            while game_over:
                window.fill(black)
                game_over_message()
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_quit = True
                        game_over = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_quit = True
                            game_over = False
                        elif event.key == pygame.K_r:
                            game_loop()

            if(self.message[1] == b'UP' and self.player1_snake.direction != "DOWN"):
                self.player1_snake.change_direction("UP")
            elif(self.message[1] == b'DOWN' and self.player1_snake.direction != "UP"):
                self.player1_snake.change_direction("DOWN")
            elif(self.message[1] == b'LEFT' and self.player1_snake.direction != "RIGHT"):
                self.player1_snake.change_direction("LEFT")
            elif(self.message[1] == b'RIGHT' and self.player1_snake.direction != "LEFT"):
                self.player1_snake.change_direction("RIGHT")
            elif(self.message[1] == b'quit'):
                game_quit = True

            if(player2_controller):
                if(self.message[2] == b'UP' and self.player2_snake.direction != "DOWN"):
                    self.player2_snake.change_direction("UP")
                elif(self.message[2] == b'DOWN' and self.player2_snake.direction != "UP"):
                    self.player2_snake.change_direction("DOWN")
                elif(self.message[2] == b'LEFT' and self.player2_snake.direction != "RIGHT"):
                    self.player2_snake.change_direction("LEFT")
                elif(self.message[2] == b'RIGHT' and self.player2_snake.direction != "LEFT"):
                    self.player2_snake.change_direction("RIGHT")
                elif(self.message[2] == b'quit'):
                    game_quit = True

            # Move the snake(s)
            self.player1_snake.move()
            if self.player2_snake:
                self.player2_snake.move()

            # Check if the snake(s) collided with the boundaries or themselves
            if any(segment in self.player1_snake.snake_segments[1:] for segment in self.player1_snake.snake_segments[0]) or \
                    self.player1_snake.snake_segments[0][0] < 0 or \
                    self.player1_snake.snake_segments[0][0] >= window_width or \
                    self.player1_snake.snake_segments[0][1] < 0 or \
                    self.player1_snake.snake_segments[0][1] >= window_height:
                game_over = True

            if self.player2_snake and (
                    any(segment in self.player2_snake.snake_segments[1:] for segment in self.player2_snake.snake_segments[0]) or
                    self.player2_snake.snake_segments[0][0] < 0 or
                    self.player2_snake.snake_segments[0][0] >= window_width or
                    self.player2_snake.snake_segments[0][1] < 0 or
                    self.player2_snake.snake_segments[0][1] >= window_height):
                game_over = True

            # Check if the snake(s) ate the food
            if self.player1_snake.snake_segments[0][0] == self.food.x and self.player1_snake.snake_segments[0][1] == self.food.y:
                self.player1_snake.snake_segments.append((self.food.x, self.food.y))
                score += 1
                self.food = Food()

            if self.player2_snake and self.player2_snake.snake_segments[0][0] == self.food.x and self.player2_snake.snake_segments[0][1] == self.food.y:
                self.player2_snake.snake_segments.append((self.food.x, self.food.y))
                score += 1
                self.food = Food()
        

# Function to display score on the game window
def display_score(score):
    if(player2_controller!=None):
        player2_controller.send(str(score))
    player1_controller.send(str(score))

# Function to display "Game Over" message
def game_over_message():
    if(player2_controller!=None):
        player2_controller.send('Game Over')
    player1_controller.send('Game Over')

def game_loop():
    # Game variables
    game_over = False
    game_quit = False
    score = 0

    # Create the snake(s) and the connection to the playing clients
    if(player1_controller.connect() == -1):
        exit()
    player1_snake = Snake(0, 0, green)
    if(player2_controller.connect() == -1):
        exit()
    player2_snake = Snake(0, 3, blue)

    # Create the food
    food = Food()

    
        