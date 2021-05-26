import torch
import random
import numpy as np
from collections import deque
from snake_game_human import SnakeGame, Direction, Point

epsilon = 0.2
q_values = np.zeros((11,3), dtype=int)
gamma = 0.99
num_episodes = 1000
discount = 0.8
learn_rate = 0.9

class Agent:

    def __init__(self):
        pass
        #print(np.argmax(q_values[self.get_state()]))

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
        return np.array(state, dtype=int)
    # Returnerar bästa action baserat på Q-värden, om random är mindre än epsilon: returnera random action.
    def get_next_action(self, game):
        return_move = [0,0,0]
        if np.random.random() < epsilon:
            print(np.argmax(q_values[self.get_state(game),:]))
            return_move[np.argmax(q_values[self.get_state(game),:])] = 1
        else: 
            return_move[random.randint(0,2)] = 1

        return np.array(return_move)

    def train_memory(self, state, action, reward, next_state, done):
        pass

def train():
    game = SnakeGame()
    agent = Agent()
    print(q_values.shape)

    while True:
       
       # Hämta gamla statet
        old_state = agent.get_state(game)

        # Hämta nästa action
        move = agent.get_next_action(game)

        # Utför action
        reward, done, score = game.play_step(move)


        # Hämta nya statet
        state_new = agent.get_state(game)
        previous_q_value = q_values[old_state][move]
        print(previous_q_value)
        
        td = reward + (discount * np.max(q_values[state_new])) - previous_q_value

        new_q_values =  previous_q_value + (learn_rate * td)
        
        q_values[old_state][move] = new_q_values

        agent.train_memory(old_state, move, reward, state_new, done)

        if done:
            game.game_reset()
         
    
if __name__ == '__main__':
    train()
        


 