from matplotlib import pyplot as plt 
import random
import numpy as np

from collections import deque
from snake_game_human import SnakeGame, Direction, Point

gamma = 0.99
num_episodes = 1000
discount = 0.8
learn_rate = 0.9

class Agent:

    def __init__(self, counts=None):
        self.q_values = np.zeros((2**11,3))
        self.epsilon = 0.1
        self.epsilon_decay = 0.9

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

    def get_state_number(self, game):
        state_number = 0
        for i in range(11):
            state_number += 2**i*self.get_state(game)[i]
        return state_number

    # Returnerar bästa action baserat på q_values-värden, om random är mindre än epsilon: returnera random action.
    def get_next_action(self, game, state):
        return_move = 0
        if random.uniform(0,1) > self.epsilon:
            possible_qs = self.q_values[state,:]
            #print(possible_qs)
            return_move = np.argmax(possible_qs)

            #return_move[np.argmax(q_values[self.get_state(game),:])] = 1
        else: 
            print("GOING RANDOM")
            return_move = random.randint(0,2)

        return return_move

    def train_memory(self, state, action, reward, next_state, done):
        pass
        

def train():
    highest_score = 0
    
    scoreArray = np.array([0,0,0,0,0,0,0,0,0,0])
    sessionScore = np.zeros(100, dtype=int)
    sessionCounter = 0
    counter = 0
    plot_tenths = 0
    #for i in range(num_episodes):

    agent = Agent()

    for i in range(num_episodes):

        done = False
        game = SnakeGame()
        state = agent.get_state_number(game)
        #done = False
        while not done:
        # Hämta gamla statet
            # Hämta nästa action
            move = agent.get_next_action(game, state)

            # Utför action
            reward, done, score = game.play_step(move)

            if (score > highest_score):
                highest_score = score

            # Hämta nya statet
            state_new = agent.get_state_number(game)
            agent.q_values[state, move] = reward + discount * np.max(agent.q_values[state_new, :])
            #print(reward + discount * np.max(q_values[state_new, :]))
            
            #print(q_values[state_new, move])
            state = state_new


        print(i)
        sessionScore[sessionCounter] = score
        print(score, " Added to session")
        sessionCounter += 1
        
        if i % 100 == 0:
            agent.epsilon_decay -= 0.01

            if agent.epsilon > 0:
                agent.epsilon = agent.epsilon * agent.epsilon_decay
                
            total = 0
            for x in sessionScore:
                total += x
            sessionScore = np.zeros(100, dtype=int)
            sessionCounter = 0;
            means = total/100
            
            scoreArray[plot_tenths] = means
            plot_tenths += 1
            counter = 0
        sessionScore[counter] = score
        counter += 1
        game.game_reset()
    
    # X = försök
    x = np.array([100,200,300,400,500,600,700,800,900,1000])

    #
    y = scoreArray
    
    # plotting the points 
    plt.plot(x, y)
    
    # naming the x axis
    plt.xlabel('Attempts')
    # naming the y axis
    plt.ylabel('Average points')
    
    # giving a title to my graph
    plt.title('Snake god')
    
    # function to show the plot
    plt.show()
         
    
if __name__ == '__main__':
    train()
        


 