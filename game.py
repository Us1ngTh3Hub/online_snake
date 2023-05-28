import socket
import pygame
import random
import server

# Initialize Pygame
pygame.init()

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
            #send segment
            pygame.draw.rect(window, self.color, (segment[0], segment[1], block_size, block_size))


class Food:
    def __init__(self):
        self.x = random.randint(0, (window_width - block_size) // block_size) * block_size
        self.y = random.randint(0, (window_height - block_size) // block_size) * block_size

    def draw(self):
        #send food
        pygame.draw.rect(window, red, (self.x, self.y, block_size, block_size))


# Function to display score on the game window
def display_score(score):
    #send score
    font = pygame.font.SysFont(None, 40)
    text = font.render("Score: " + str(score), True, white)
    window.blit(text, (10, 10))


# Function to display "Game Over" message
def game_over_message():
    #send game over
    font = pygame.font.SysFont(None, 60)
    text1 = font.render("Game Over!", True, red)
    text2 = font.render("Press Q to Quit", True, white)
    window.blit(text1, (window_width // 2 - 150, window_height // 2 - 30))
    window.blit(text2, (window_width // 2 - 140, window_height // 2 + 30))


def game_loop():
    # Game variables
    game_over = False
    game_quit = False
    score = 0

    # Create the snake(s)
    player1_snake = Snake(0, 0, green)
    #player1_controller = server.udpserver(address1,port1)
    player2_snake = None
    #player2_controller = server.udpserver(address2,port2)

    # Create the food
    food = Food()

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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game_quit = True
                elif event.key == pygame.K_w and player1_snake.direction != "DOWN":
                    player1_snake.change_direction("UP")
                elif event.key == pygame.K_s and player1_snake.direction != "UP":
                    player1_snake.change_direction("DOWN")
                elif event.key == pygame.K_a and player1_snake.direction != "RIGHT":
                    player1_snake.change_direction("LEFT")
                elif event.key == pygame.K_d and player1_snake.direction != "LEFT":
                    player1_snake.change_direction("RIGHT")
                elif event.key == pygame.K_UP and player2_snake and player2_snake.direction != "DOWN":
                    player2_snake.change_direction("UP")
                elif event.key == pygame.K_DOWN and player2_snake and player2_snake.direction != "UP":
                    player2_snake.change_direction("DOWN")
                elif event.key == pygame.K_LEFT and player2_snake and player2_snake.direction != "RIGHT":
                    player2_snake.change_direction("LEFT")
                elif event.key == pygame.K_RIGHT and player2_snake and player2_snake.direction != "LEFT":
                    player2_snake.change_direction("RIGHT")

        # Move the snake(s)
        player1_snake.move()
        if player2_snake:
            player2_snake.move()

        # Check if the snake(s) collided with the boundaries or themselves
        if any(segment in player1_snake.snake_segments[1:] for segment in player1_snake.snake_segments[0]) or \
                player1_snake.snake_segments[0][0] < 0 or \
                player1_snake.snake_segments[0][0] >= window_width or \
                player1_snake.snake_segments[0][1] < 0 or \
                player1_snake.snake_segments[0][1] >= window_height:
            game_over = True

        if player2_snake and (
                any(segment in player2_snake.snake_segments[1:] for segment in player2_snake.snake_segments[0]) or
                player2_snake.snake_segments[0][0] < 0 or
                player2_snake.snake_segments[0][0] >= window_width or
                player2_snake.snake_segments[0][1] < 0 or
                player2_snake.snake_segments[0][1] >= window_height):
            game_over = True

        # Check if the snake(s) ate the food
        if player1_snake.snake_segments[0][0] == food.x and player1_snake.snake_segments[0][1] == food.y:
            player1_snake.snake_segments.append((food.x, food.y))
            score += 1
            food = Food()

        if player2_snake and player2_snake.snake_segments[0][0] == food.x and player2_snake.snake_segments[0][1] == food.y:
            player2_snake.snake_segments.append((food.x, food.y))
            score += 1
            food = Food()

        # Update the game window
        window.fill