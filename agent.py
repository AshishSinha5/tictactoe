import numpy as np
import random
from collections import defaultdict

class agent:
    def __init__(self, alpha, gamma, eps, eps_decay=0.1):
        self.alpha = alpha # learning rate 
        self.gamma = gamma # discount factor 
        self.eps = eps # epsilon explore vs exploit 
        self.eps_decay = eps_decay # decay rate of the epsilon 
        self.actions = []
        for i in range(3):
            for j in range(3):
                self.actions.append((i, j))
        self.Q = {}
        for action in self.actions:
            self.Q[action] = defaultdict(int)
        self.rewards = []

    def get_action(self, s):
        possible_actions = [a for a in self.actions if s[a[0]][a[1]] == "_"]
        if random.random < self.eps:
            # choose random action
            action = possible_actions[random.randint(0, len(possible_actions)) - 1]
        else:
            # choose the actions that have the highest values
            values = np.array([self.Q[a][s] for a in possible_actions])
            ix_max = np.where(values == np.max(values))
            if len(ix_max) > 1:
                ix_select = np.random.choice(ix_max, 1)[0]
            else:
                ix_select = ix_max[0]
            action = possible_actions[ix_select]
        
        # decay the epsilon parameter 
        self.eps = self.eps*self.eps_decay

        return action

    def update(self, s, s_, a, a_, r):
        # update the Q values after the action is performed and the next state is achieved after recieving the reward
        if s_ is not None:
            # if the state is not terminal 
            possible_actions = [a for a in self.actions if s_[a[0],a[1]]!= "_"]
            Q_options = [self.Q[a][s_] for a in possible_actions]
            self.Q[a][s] += self.alpha*(r + self.gamma*max(Q_options)- self.Q[a][s])
        else:
            self.Q[a][s] += self.alpha*(r - self.Q[a][s])
