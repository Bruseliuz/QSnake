# Grupp 10
# Nils Bruzelius
# Einar Edberg
# Philip Rönnmark
#
# Grundsystemet är taget från https://github.com/python-engineer/snake-ai-pytorch
#

import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font('arial.ttf', 12)

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
    
    def __init__(self, w=80, h=80):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('QSnake')
        self.clock = pygame.time.Clock()
        self.game_reset()
        
    # Initeiera spelet
    def game_reset(self):
        self.direction = Direction.RIGHT
        
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0    
    
    # Placera ut mat
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
        
    # Agenten utför en action
    def play_step(self, action):
        self.frame_iteration += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 1. Gå
        self._move(action) # update the head
        self.snake.insert(0, self.head)
        
        # 2. Kolla om spelet är över pga krock eller för lång tid går i samma försök
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            reward = -10
            game_over = True
            return reward, game_over, self.score
            
        
        
        previous_head_location = self.head
        # 3. placera ny mat eller bara gå
        if self.head == self.food:
            reward = 10
            self.score += 1
            try:
                self._place_food()
            except:
                self.game_reset()
        # Jämför absolutvärdet mellan ormens huvud's tidigare position och ormens huvud's nuvarande position och maten
        elif(abs((previous_head_location.x + previous_head_location.y) - (self.food.x + self.food.y)) > abs((self.head.x + self.head.y) - (self.food.x + self.food.y))):
            reward = 1
            self.snake.pop()
        else:
            reward = -1
            self.snake.pop()
        
        
        # 4. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 5. return game over and score
        return reward, game_over, self.score
    
    # Kollar om en Point är på kollisionskurs
    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # Träffar kanten
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # Träffar Sig själv
        if pt in self.snake[1:]:
            return True
        
        return False
    
    # Uppdaterar grafiken
    def _update_ui(self):
        self.display.fill(BLACK)
        
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
    
    # Beräkna vilket håll ormen skall röra sig baserat på en action
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
            