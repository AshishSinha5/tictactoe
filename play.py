"""
Algorthm Overview
- Intitalize the agent 
- State - {"X", current_state}
- Take action using the Q learning algorithm
- Recieve the reward for the action
- Recieve the updated state - {"O", updated_state}
- Update the Q function using the bellman equation 
- Keep playing till the terminal state is reached 

Reward Model 
- Loss = -10 
- Draw = 0
- Win = +10
- For every other move = -1
"""

from tqdm import tqdm
from ttt import ttt 
from agent import agent 
import matplotlib.pyplot as plt

class play:
    def __init__(self, num_episodes = 100000):
        self.ttt = ttt()
        self.agent = agent(eps_decay=0.95)
        self.num_episodes = num_episodes
        self.cummulative_reward = []

    def step(self, action):
        s, r, t, inf = self.ttt.play(action[0], action[1])
        return s, r, t, inf

    def simulate(self):
        self.cummulative_reward = []
        for _ in tqdm(range(self.num_episodes)):
            # get actions
            self.ttt.reset_board()
            s = (0, self.ttt.board)
            t = False
            ep_reward = 0
            iter = 0
            while not t:
                iter+=1
                action = self.agent.get_action(s)   
                new_s, r, t, _ = self.step(action)
                ep_reward += r
                if t:
                    self.agent.update(s, None, action, None, r)
                    break
                self.agent.update(s, new_s, action, None, r)
                s = new_s
            self.cummulative_reward.append(ep_reward/iter)

        
    def plot_rewards(self):
        plt.plot(self.cummulative_reward)
        plt.title("Cummulative Reward Plot")
        plt.xlabel("Episodes")
        plt.ylabel("Average Cummulative Rewards")
        plt.savefig("reward_plot.png")
        plt.show()


def main():
    learn_game = play()
    learn_game.simulate()
    learn_game.plot_rewards()

if __name__ == "__main__":
    main()
            
                
            

