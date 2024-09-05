# Tic-Tac-Toe with Reinforcement Learning Bot

This project implements a Tic-Tac-Toe game where you can play against a bot trained using reinforcement learning, specifically the Q-learning algorithm.

## Project Structure

- `agent.py`: Defines the RL agent using Q-learning.
- `env.py`: Implements the Tic-Tac-Toe environment.
- `play.py`: Contains the GUI for playing against the trained bot.
- `train.py`: Script for training the RL agent.
- `q_table.pkl`: Pickle file storing the trained Q-table.
- `requirements.txt`: List of Python dependencies.

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/AshishSinha5/tictactoe
   cd tictactoe
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Training the Bot

To train the RL agent, run:

```
python train.py
```

You can specify the number of training episodes:

```
python train.py --ep 1000000
```

### Playing Against the Bot

To play against the trained bot, run:

```
python play.py
```

You can adjust the exploration rate of the bot:

```
python play.py --eps 0.1
```

## How It Works

- The bot uses Q-learning, a model-free reinforcement learning algorithm.
- During training, it learns to make optimal moves by playing against itself.
- The learned strategy is stored in the `q_table.pkl` file.
- When playing, the bot uses this Q-table to choose its moves.

## Q-Learning Algorithm

Q-learning is a value-based reinforcement learning algorithm that aims to learn a policy that tells an agent what action to take under specific circumstances. It was introduced by Watkins in 1989 and has since become one of the most popular reinforcement learning methods.

Key aspects of Q-learning:

1. **Q-Table**: The algorithm maintains a table (Q-table) where each cell represents the expected future reward of taking a specific action in a given state.

2. **Exploration vs Exploitation**: The agent balances between exploring new actions and exploiting known good actions using an epsilon-greedy strategy.

3. **Update Rule**: After each action, the Q-value is updated based on the reward received and the maximum Q-value of the next state:

   Q(s,a) = Q(s,a) + α * (r + γ * max(Q(s',a')) - Q(s,a))

   Where:
   - s, a are the current state and action
   - s', a' are the next state and action
   - r is the reward
   - α is the learning rate
   - γ is the discount factor

4. **Model-Free**: Q-learning doesn't require a model of the environment, making it adaptable to various problems.

In this Tic-Tac-Toe implementation, the agent learns to play by repeatedly playing games against itself and updating its Q-table based on the outcomes.

For more details on Q-learning, refer to the original paper:
Watkins, C.J.C.H., Dayan, P. Q-learning. Mach Learn 8, 279–292 (1992). https://doi.org/10.1007/BF00992698

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
