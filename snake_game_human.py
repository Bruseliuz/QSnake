import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.Font('arial.ttf', 12)
#font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (100, 0, 255)
BLUE2 = (200, 100, 255)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SPEED = 20



class SnakeGame:
    
    def __init__(self, w=240, h=240):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.game_reset()
        
       
    def game_reset(self):
        # init game state
        self.direction = Direction.RIGHT
        
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0    
        
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
        
    def play_step(self, action):
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            #if event.type == pygame.KEYDOWN:
            #    if event.key == pygame.K_LEFT:
            #        self.direction = Direction.LEFT
            #    elif event.key == pygame.K_RIGHT:
            #        self.direction = Direction.RIGHT
            #    elif event.key == pygame.K_UP:
            #        self.direction = Direction.UP
            #    elif event.key == pygame.K_DOWN:
            #        self.direction = Direction.DOWN
        
        previous_head_location = self.head
        # 2. move
        self._move(action) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision():
            reward = -10
            game_over = True
            return reward, game_over, self.score
            
        
        #print(self.food - self.head)  
        
        # 4. place new food or just move
        if self.head == self.food:
            reward = 10
            self.score += 1
            self._place_food()
        elif(abs((previous_head_location.x + previous_head_location.y) - (self.food.x + self.food.y)) > abs((self.head.x + self.head.y) - (self.food.x + self.food.y))):
            reward += 1
            self.snake.pop()
        else:
            reward -= 1
            self.snake.pop()
        
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return reward, game_over, self.score
    
    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True
        
        return False
        
    def _update_ui(self):
        self.display.fill(BLACK)
        
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        text = font.render("Score: " + str(self.score) + " Iterations: " + str(self.frame_iteration), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        
    def _move(self, action):
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        index = clock_wise.index(self.direction)

        if action == 0:
            new_direction = clock_wise[index]
        elif action == 1:
            next_index = (index + 1) % 4
            new_direction = clock_wise[next_index]
        else:
            next_index = (index - 1) % 4
            new_direction = clock_wise[next_index]

        self.direction = new_direction    
        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            #print("DIRECTION RIGHT")
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            #print("DIRECTION LEFT")
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            #print("DIRECTION DOWN")
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            #print("DIRECTION UP")
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)
            