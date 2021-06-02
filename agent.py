from matplotlib import pyplot as plt 
import random
import numpy as np
from snake_game import SnakeGame, Direction, Point

# Antal episoder ormen kör
num_episodes = 500

# Discount värde för Bellman's ekvation
discount = 0.8

class Agent:

    def __init__(self):
        self.q_values = np.zeros((2**11,3))

        # Epsilon för epsilon-greedy
        self.epsilon = 0.1
        self.epsilon_decay = 0.9

    # Hämta tillståndet. Tillstånd baserat på https://github.com/python-engineer/snake-ai-pytorch
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
            #Fara rakt fram
            (direction_right and game.is_collision(head_right)) or
            (direction_left and game.is_collision(head_left)) or
            (direction_up and game.is_collision(head_up)) or
            (direction_down and game.is_collision(head_down)),
        
            #Fara till höger
            (direction_right and game.is_collision(head_down)) or
            (direction_left and game.is_collision(head_up)) or
            (direction_up and game.is_collision(head_right)) or
            (direction_down and game.is_collision(head_left)),

            #Fara till vänster
            (direction_right and game.is_collision(head_up)) or
            (direction_left and game.is_collision(head_down)) or
            (direction_up and game.is_collision(head_left)) or
            (direction_down and game.is_collision(head_right)),

            #Vilket håll är agenten påväg
            direction_left,
            direction_right,
            direction_up,
            direction_down,
            
            #Var är maten
            game.food.x < game.head.x,
            game.food.x > game.head.x,
            game.food.y < game.head.y,
            game.food.y > game.head.y
        ]
        return np.array(state, dtype=int)

    # Generera och returnera unika nummer för varje tillstånd
    def get_state_number(self, game):
        state_number = 0
        for i in range(11):
            state_number += 2**i*self.get_state(game)[i]
        return state_number

    # Epsilon-greedy
    # Returnerar bästa action baserat på q_values-värden, om random är mindre än epsilon: returnera random action.
    def get_next_action(self, state):
        return_move = 0
        if random.uniform(0,1) > self.epsilon:
            possible_qs = self.q_values[state,:]
            return_move = np.argmax(possible_qs)
        else: 
            return_move = random.randint(0,2)

        return return_move

# Denna metod är delvis inspirerad av https://github.com/python-engineer/snake-ai-pytorch/blob/main/agent.py
def train():

    scoreArray = np.zeros(50, dtype=np.double)
    sessionScore = np.zeros(20, dtype=int)
    sessionCounter = 0
    counter = 0
    plot_tenths = 0
    agent = Agent()

    for i in range(num_episodes):

        done = False

        # Initiera SnakeGame-objektet
        game = SnakeGame()

        # Hämta gamla statet
        state = agent.get_state_number(game)

        while not done:

            # Hämta nästa action
            move = agent.get_next_action(state)

            # Utför action
            reward, done, score = game.play_step(move)

            # Hämta nya statet
            state_new = agent.get_state_number(game)

            # Räkna ut och lagra Q för det state-action paret
            agent.q_values[state, move] = reward + discount * np.max(agent.q_values[state_new, :])

            # Gå vidare med nästa tillstånd
            state = state_new
        
        # Lagra score för plottning
        sessionScore[sessionCounter] = score
        sessionCounter += 1
        
        # Plotting uträkningar
        if i % 20 == 0:     
            total = 0
            for x in sessionScore:
                total += x
            sessionScore = np.zeros(20, dtype=int)
            sessionCounter = 0;
            means = total/20
            
            scoreArray[plot_tenths] = means
            plot_tenths += 1
            counter = 0
        sessionScore[counter] = score
        counter += 1

        # Sänk epsilon-värdet ju mer agenten har kört för att minska "randomness" i val av action
        if agent.epsilon > 0 and i % 25 == 0:
                agent.epsilon = agent.epsilon * agent.epsilon_decay

        game.game_reset()
    
    # Visa plot
    plot_score(scoreArray)


def plot_score(scoreArray):

    plt.plot(np.array([20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500]), scoreArray)
    
    plt.xlabel('Attempts')
    plt.ylabel('Average points')
    plt.title('QSnake')
    plt.show()
         
    
if __name__ == '__main__':
    train()
        


 