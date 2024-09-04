import numpy as np
import random
from collections import defaultdict

class agent:
    def __init__(self, alpha=0.1, gamma=0.1, eps=0.1, eps_decay=0.9):
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
        possible_actions = [a for a in self.actions if s[1][a[0]][a[1]] == "_"]
        if random.random() < self.eps:
            # choose random action
            action = possible_actions[random.randint(0, len(possible_actions) - 1)]
        else:
            # choose the actions that have the highest values
            values = np.array([self.Q[a][self.make_hash(s)]for a in possible_actions])
            ix_max = np.where(values == np.max(values))[0]
            if len(ix_max) > 1:
                ix_select = np.random.choice(ix_max, 1)[0]
            else:
                ix_select = ix_max[0]
            action = possible_actions[ix_select]
        
        # decay the epsilon parameter geometric decay 
        # self.eps = self.eps*self.eps_decay

        return action

    def update(self, s, s_, a, a_, r):
        # update the Q values after the action is performed and the next state is achieved after recieving the reward
        if s_ is not None:
            # import pdb; pdb.set_trace()
            # if the state is not terminal 
            possible_actions = [action for action in self.actions if s_[1][action[0]][action[1]]== "_"]
            Q_options = [self.Q[action][self.make_hash(s_)] for action in possible_actions]
            self.Q[a][self.make_hash(s)] += self.alpha*(r + self.gamma*max(Q_options)- self.Q[a][self.make_hash(s)])
        else:
            self.Q[a][self.make_hash(s)] += self.alpha*(r - self.Q[a][self.make_hash(s)])

    def make_hash(self, s):
        return tuple((s[0], tuple(map(tuple, s[1])))) 
