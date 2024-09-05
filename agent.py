import random 
import pickle
from collections import defaultdict
def create_int_default_dict():
    return defaultdict(int)
class agent:
    def __init__(self, eps = 0.1, alpha = 0.1, gamma = 0.9):
        self.eps = eps
        self.alpha = alpha
        self.gamma = gamma 
        self.q_table = {'x' : defaultdict(create_int_default_dict),
                        'o' : defaultdict(create_int_default_dict)}

    def get_q_values(self, state, action, player):
        return self.q_table[player][state][action]

    def choose_action(self, state, player):
        available_actions = [i for i, spot in enumerate(state) if spot == '-']
        if random.uniform(0, 1) < self.eps:
            return random.choice(available_actions)
        else:
            q_values = [self.get_q_values(state, action, player) for action in available_actions]
            max_q = max(q_values)
            best_actions = [action for action, q_values in zip(available_actions, q_values) if q_values == max_q]
            return random.choice(best_actions)
        
    def learn(self, state, action, reward, next_state, done, player):
        old_q = self.get_q_values(state, action, player)
        if done:
            new_q = old_q + self.alpha*(reward - old_q)
        else:
            next_player = 'o' if player == 'x' else 'x'
            next_max_q = max([self.get_q_values(next_state, a, next_player) for a in range(9) if next_state[a] == '-'])
            new_q = old_q + self.alpha * (reward + self.gamma * -next_max_q - old_q)
        self.q_table[player][state][action] = new_q

    def save_q_weights(self):
        with open("q_table.pkl", 'wb') as f:
            pickle.dump(self.q_table, f, protocol=pickle.HIGHEST_PROTOCOL)
