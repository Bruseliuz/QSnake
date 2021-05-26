import torch
import random
import numpy as np
from collections import deque
from snake_game_human import SnakeGame, Direction, Point

epsilon = 0.8
q_values = np.zeros((2**11,3))
gamma = 0.99
num_episodes = 1000
discount = 0.8
learn_rate = 0.9

class Agent:

    def __init__(self):
        pass

    def get_state(self, game):
        head = game.snake[0]
        head_left = Point(head.x - 20, head.y)
        head_right = Point(head.x + 20, head.y)
        head_up = Point(head.x, head.y -20)
        head_down = Point(head.x, head.y + 20)
    
        

        direction_left = (game.direction == Direction.LEFT)
        direction_right = (game.direction == Direction.RIGHT)
        direction_up = (game.direction == Direction.UP)
        direction_down = (game.direction == Direction.DOWN)


        state = [
            #Danger straight
            (direction_right and game.is_collision(head_right)) or
            (direction_left and game.is_collision(head_left)) or
            (direction_up and game.is_collision(head_up)) or
            (direction_down and game.is_collision(head_down)),
        
            #Danger right
            (direction_right and game.is_collision(head_down)) or
            (direction_left and game.is_collision(head_up)) or
            (direction_up and game.is_collision(head_right)) or
            (direction_down and game.is_collision(head_left)),

            #Danger Left
            (direction_right and game.is_collision(head_up)) or
            (direction_left and game.is_collision(head_down)) or
            (direction_up and game.is_collision(head_left)) or
            (direction_down and game.is_collision(head_right)),

            #Move direction
            direction_left,
            direction_right,
            direction_up,
            direction_down,
            
            #Food location

            game.food.x < game.head.x,
            game.food.x > game.head.x,
            game.food.y < game.head.y,
            game.food.y > game.head.y
        ]
        return np.array(state)

    def get_state_number(self, game):
        state_number = 0
        for i in range(11):
            state_number += 2**i*self.get_state(game)[i]
        #print(state_number)
        return state_number

    # Returnerar bästa action baserat på q_values-värden, om random är mindre än epsilon: returnera random action.
    def get_next_action(self, game, state):
        return_move = [0,0,0]
        if np.random.random() < epsilon:
            #print(np.argmax(q_values[self.get_state(game),:]))
            possible_qs = q_values[state,:]
            print(np.argmax(possible_qs))
            return_move[np.argmax(possible_qs)] = 1
            
            #return_move[np.argmax(q_values[self.get_state(game),:])] = 1
        else: 
            return_move = random.randint(0,2)

        return np.array(return_move)

    def train_memory(self, state, action, reward, next_state, done):
        pass

def train():
    game = SnakeGame()
    agent = Agent()

    state = agent.get_state_number(game)

    while True:
       
       # Hämta gamla statet
        

        # Hämta nästa action
        move = agent.get_next_action(game, state)

        # Utför action
        reward, done, score = game.play_step(move)

        # Hämta nya statet
        state_new = agent.get_state_number(game)
        
        #print(reward)
        q_values[state, move] = reward + discount * np.max(q_values[state_new, :])
        
        #print(q_values[state, move])
        state = state_new
        
        #td = reward + (discount * np.max(q_values[state_new])) - previous_q_value
#
        #new_q_values =  previous_q_value + (learn_rate * td)
        #
        #q_values[old_state][move] = new_q_values
#
        #agent.train_memory(old_state, move, reward, state_new, done)


        if done:
            game.game_reset()
         
    
if __name__ == '__main__':
    train()
        


 