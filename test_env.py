import numpy as np
import random
from collections import defaultdict

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def make_move(self, position):
        if self.board[position] == ' ':
            self.board[position] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def check_winner(self):
        winning_combos = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        for combo in winning_combos:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                return self.board[combo[0]]
        if ' ' not in self.board:
            return 'Tie'
        return None

    def get_state(self):
        return ''.join(self.board)

class QLearningAgent:
    def __init__(self, epsilon=0.1, alpha=0.1, gamma=0.9):
        self.q_table = {'X': defaultdict(lambda: defaultdict(float)),
                        'O': defaultdict(lambda: defaultdict(float))}
        self.epsilon = epsilon  # Exploration rate
        self.alpha = alpha      # Learning rate
        self.gamma = gamma      # Discount factor

    def get_q_value(self, state, action, player):
        return self.q_table[player][state][action]

    def choose_action(self, state, available_actions, player):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(available_actions)
        else:
            q_values = [self.get_q_value(state, action, player) for action in available_actions]
            max_q = max(q_values)
            best_actions = [action for action, q_value in zip(available_actions, q_values) if q_value == max_q]
            return random.choice(best_actions)

    def learn(self, state, action, reward, next_state, done, player):
        old_q = self.get_q_value(state, action, player)
        if done:
            new_q = old_q + self.alpha * (reward - old_q)
        else:
            next_player = 'O' if player == 'X' else 'X'
            next_max_q = max([self.get_q_value(next_state, a, next_player) for a in range(9) if next_state[a] == ' '])
            new_q = old_q + self.alpha * (reward + self.gamma * -next_max_q - old_q)  # Note the negative next_max_q
        self.q_table[player][state][action] = new_q

def play_game(agent, game):
    state = game.get_state()
    while True:
        current_player = game.current_player
        available_actions = game.available_moves()
        action = agent.choose_action(state, available_actions, current_player)
        
        game.make_move(action)
        next_state = game.get_state()
        winner = game.check_winner()
        
        if winner:
            if winner == 'Tie':
                reward = 0
            else:
                reward = 1 if winner == current_player else -1
            agent.learn(state, action, reward, next_state, done=True, player=current_player)
            return winner
        else:
            reward = 0
            agent.learn(state, action, reward, next_state, done=False, player=current_player)
        
        state = next_state

# Training
agent = QLearningAgent(epsilon=0.1, alpha=0.1, gamma=0.9)
num_episodes = 500000

for episode in range(num_episodes):
    game = TicTacToe()
    winner = play_game(agent, game)
    if episode % 50000 == 0:
        print(f"Episode {episode}, Winner: {winner}")

    # Decay epsilon
    agent.epsilon = max(0.01, agent.epsilon * 0.9999)

# Test the trained agent
def play_optimal_move(agent, game):
    state = game.get_state()
    available_actions = game.available_moves()
    return agent.choose_action(state, available_actions, game.current_player)

print("\nPlaying a test game:")
game = TicTacToe()
while True:
    move = play_optimal_move(agent, game)
    game.make_move(move)
    print(f"Player {game.current_player} makes move: {move}")
    print(game.board[0:3])
    print(game.board[3:6])
    print(game.board[6:9])
    print()
    winner = game.check_winner()
    if winner:
        print(f"Game Over. Winner: {winner}")
        break

# Print statistics
x_wins = o_wins = ties = 0
num_test_games = 10000

for _ in range(num_test_games):
    game = TicTacToe()
    winner = play_game(agent, game)
    if winner == 'X':
        x_wins += 1
    elif winner == 'O':
        o_wins += 1
    else:
        ties += 1

print(f"\nAfter {num_test_games} test games:")
print(f"X wins: {x_wins} ({x_wins/num_test_games*100:.2f}%)")
print(f"O wins: {o_wins} ({o_wins/num_test_games*100:.2f}%)")
print(f"Ties: {ties} ({ties/num_test_games*100:.2f}%)")
