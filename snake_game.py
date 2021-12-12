import pygame, sys
import random
from pygame.math import Vector2
import numpy as np
from collections import deque

pygame.init()

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

APPLE = (200,0,0)
HEAD_OUTSIDE = (0,0,0)
BODY_OUTSIDE = (0,0,255)
INSIDE = (0,100,255)

font = pygame.font.SysFont('arial',20)

#game speed
SPEED = 5
BLOCK_SIZE = 20

class SnakeGame:
    def __init__(self):
        self.width = 640
        self.height = 480

        self.column_count = self.width//BLOCK_SIZE
        self.row_count = self.height//BLOCK_SIZE

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        self.direction = RIGHT
        self.score = 0

        self.head = Vector2(self.width/2, self.height/2)
        self.snake = [self.head,
                        Vector2(self.head.x-BLOCK_SIZE, self.head.y),
                        Vector2(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        self.x = int(self.width / BLOCK_SIZE)
        self.y = int(self.height / BLOCK_SIZE)
        self.apple = None

        self.viss = 0

        self._place_apple()
    
    def alter_map(self):
        self.MAP = np.zeros((self.x,self.y))
       
        for i in range(len(self.snake)):
            self.MAP[int(self.snake[i][0] / BLOCK_SIZE)][int(self.snake[i][1] / BLOCK_SIZE)] = 1

    def path_find(self):
        head_x = int(self.snake[0][0] / BLOCK_SIZE)
        head_y = int(self.snake[0][1] / BLOCK_SIZE)
        apple_x = int(self.apple[0] / BLOCK_SIZE)
        apple_y = int(self.apple[1] / BLOCK_SIZE)
        
        if(apple_x > head_x and apple_y == head_y and self.MAP[head_x+1][head_y] == 0):
            self.direction = RIGHT
        elif(apple_x < head_x and apple_y == head_y and self.MAP[head_x-1][head_y] == 0):
            self.direction = LEFT
        elif(apple_x == head_x and apple_y < head_y and self.MAP[head_x][head_y-1] == 0):
            self.direction = UP
        elif(apple_x == head_x and apple_y > head_y and self.MAP[head_x][head_y+1] == 0):
            self.direction = DOWN
            
        elif(self.direction == RIGHT):
            if(head_y+1 == 24):
                if(self.MAP[head_x][head_y-1] == 0):
                    self.direction = UP
                elif(self.MAP[head_x+1][head_y] == 0):
                    self.direction = RIGHT

            elif(apple_x < head_x and apple_y < head_y):
                if(self.MAP[head_x][head_y-1] == 0):
                    self.direction = UP
                elif(self.MAP[head_x][head_y+1] == 0):
                    self.direction = DOWN
            elif(apple_x > head_x and apple_y < head_y):
                if(self.MAP[head_x][head_y-1] == 0):
                    self.direction = UP
                elif(self.MAP[head_x][head_y+1] == 0):
                    self.direction = DOWN
            elif(apple_x < head_x and apple_y > head_y):
                if(self.MAP[head_x][head_y+1] == 0):
                    self.direction = DOWN
                elif(self.MAP[head_x][head_y-1] == 0):
                    self.direction = UP
            else:
                if(self.MAP[head_x][head_y+1] == 0):
                    self.direction = DOWN
                elif(self.MAP[head_x][head_y-1] == 0):
                    self.direction = UP
                
                

        elif(self.direction == LEFT):
            if(head_y+1 == 24):
                if(self.MAP[head_x][head_y-1] == 0):
                    self.direction = UP
                elif(self.MAP[head_x-1][head_y] == 0):
                    self.direction = LEFT

            elif(apple_x < head_x and apple_y < head_y):
                if(self.MAP[head_x][head_y-1] == 0):
                    self.direction = UP
                elif(self.MAP[head_x][head_y+1] == 0):
                    self.direction = DOWN
            elif(apple_x > head_x and apple_y < head_y):
                if(self.MAP[head_x][head_y-1] == 0):
                    self.direction = UP
                elif(self.MAP[head_x][head_y+1] == 0):
                    self.direction = DOWN
            elif(apple_x < head_x and apple_y > head_y):
                if(self.MAP[head_x][head_y+1] == 0):
                    self.direction = DOWN
                elif(self.MAP[head_x][head_y-1] == 0):
                    self.direction = UP
            else:
                if(self.MAP[head_x][head_y+1] == 0):
                    self.direction = DOWN
                elif(self.MAP[head_x][head_y-1] == 0):
                    self.direction = UP

        elif(self.direction == UP):
            if(head_x+1 == 32):
                if(self.MAP[head_x-1][head_y] == 0):
                    self.direction = LEFT
                elif(self.MAP[head_x][head_y-1] == 0):
                    self.direction = UP
                
            elif(apple_x < head_x and apple_y < head_y):
                if(self.MAP[head_x-1][head_y] == 0):
                    self.direction = LEFT
                elif(self.MAP[head_x+1][head_y] == 0):
                    self.direction = RIGHT
            elif(apple_x > head_x and apple_y < head_y):
                if(self.MAP[head_x+1][head_y] == 0):
                    self.direction = RIGHT
                elif(self.MAP[head_x-1][head_y] == 0):
                    self.direction = LEFT
            elif(apple_x < head_x and apple_y > head_y):
                if(self.MAP[head_x - 1][head_y] == 0):
                    self.direction = LEFT
                elif(self.MAP[head_x + 1][head_y] == 0):
                    self.direction = RIGHT
            else:
                if(self.MAP[head_x + 1][head_y] == 0):
                    self.direction = RIGHT
                elif(self.MAP[head_x - 1][head_y] == 0):
                    self.direction = LEFT
            
        else:
            if(head_x+1 == 32):
                if(self.MAP[head_x-1][head_y] == 0):
                    self.direction = LEFT
                elif(self.MAP[head_x][head_y+1] == 0):
                    self.direction = DOWN
            
            elif(head_y+1 == 24):
                if(self.MAP[head_x-1][head_y] == 0):
                    self.direction = LEFT
                elif(self.MAP[head_x+1][head_y] == 0):
                    self.direction = RIGHT

            elif(apple_x < head_x and apple_y < head_y):
                if(self.MAP[head_x-1][head_y] == 0):
                    self.direction = LEFT
                elif(self.MAP[head_x+1][head_y] == 0):
                    self.direction = RIGHT
            elif(apple_x > head_x and apple_y < head_y):
                if(self.MAP[head_x+1][head_y] == 0):
                    self.direction = RIGHT
                elif(self.MAP[head_x-1][head_y] == 0):
                    self.direction = LEFT
            elif(apple_x < head_x and apple_y > head_y):
                if(self.MAP[head_x - 1][head_y] == 0):
                    self.direction = LEFT
                elif(self.MAP[head_x + 1][head_y] == 0):
                    self.direction = RIGHT
            else:
                if(self.MAP[head_x + 1][head_y] == 0):
                    self.direction = RIGHT
                elif(self.MAP[head_x - 1][head_y] == 0):
                    self.direction = LEFT                

                   
    def play_scene(self):
        self.alter_map()
        self.path_find()
        self._move_snake()
        game_over = self._is_game_over()
        if game_over:
            return game_over, self.score

        if self.head == self.apple:
            self.score += 1
            self._place_apple()
        else:
            self.snake.pop()

        self._update_ui()
        self.clock.tick(SPEED)

        return game_over, self.score


    def _place_apple(self):
        x = random.randint(0, self.column_count-1)*BLOCK_SIZE
        y = random.randint(0, self.row_count-1)*BLOCK_SIZE

        self.apple = Vector2(x, y)
        if self.apple in self.snake:
            self._place_apple()

    def _move_snake(self):
        x = self.head.x
        y = self.head.y
        
        if self.direction == RIGHT:
            x += BLOCK_SIZE
        elif self.direction == LEFT:
            x -= BLOCK_SIZE
        elif self.direction == DOWN:
            y += BLOCK_SIZE
        elif self.direction == UP:
            y -= BLOCK_SIZE

        self.head = Vector2(x, y)
        self.snake.insert(0, self.head)

    def _is_game_over(self):
        if self.head.x>self.width-BLOCK_SIZE or self.head.x<0 or self.head.y>self.height-BLOCK_SIZE or self.head.y<0:
            return True
        
        if self.head in self.snake[1:]:
            return True

        return False

    def _update_ui(self):
        self._draw_background()
        self._draw_snake()
        self._draw_apple()

        score_board = font.render("Score: " + str(self.score), True, (0, 0, 0))
        self.screen.blit(score_board, [0, 0])

        pygame.display.update()

    def _draw_background(self):
        self.screen.fill((175,215,70))
        
        grass_color = (167,209,61)
        
        for row in range(self.row_count):
            for col in range(self.column_count):
                if (row % 2 == 0 and col % 2 == 0) or (row % 2 != 0 and col % 2 != 0):
                    grass_rect = pygame.Rect(col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    pygame.draw.rect(self.screen, grass_color, grass_rect)

    def _draw_snake(self):
        for vec2 in self.snake:
            if vec2 == self.head:
                pygame.draw.rect(self.screen, HEAD_OUTSIDE, pygame.Rect(vec2.x, vec2.y, BLOCK_SIZE, BLOCK_SIZE))
            else:
                pygame.draw.rect(self.screen, BODY_OUTSIDE, pygame.Rect(vec2.x, vec2.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.screen, INSIDE, pygame.Rect(vec2.x+4, vec2.y+4, 12, 12))

    def _draw_apple(self):
        pygame.draw.rect(self.screen, APPLE, pygame.Rect(self.apple.x, self.apple.y, BLOCK_SIZE, BLOCK_SIZE))
        
game = []
score_sum = 0
low_score = 100
high_score = 0
# for i in range(100):
#     game.append(SnakeGame())
#     # game loop
#     while True:
#         is_game_over, score = game[i].play_scene()

#         if is_game_over:
#             break
#     if(low_score > score):
#         low_score = score
#     if(high_score < score):
#         high_score = score
#     score_sum += score

# print('Final score:', str(score_sum/100))
# print('High score: ',str(high_score))
# print('Low score: ',str(low_score))

game = SnakeGame()
    # game loop
while True:
    is_game_over, score = game.play_scene()

    if is_game_over:
        break


print('Final score:', str(score))

    
pygame.quit()
sys.exit()