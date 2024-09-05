from env import ticTacToe
from agent import agent  

class simulation:
    def __init__(self, num_episodes = 200000):
        self.agent = agent()
        self.env = ticTacToe()
        self.num_episodes = num_episodes

    def play_game(self):
        state = self.env.get_state()
        while True:
            current_player = self.env.current_player
            action = self.agent.choose_action(state, current_player)
            self.env.make_move(action)
            next_state= self.env.get_state()
            reward, termination,winner = self.env.check_state()
            if termination:
                self.agent.learn(state, action,reward, None, True, current_player) 
                break
            else:
                self.agent.learn(state, action,reward, next_state,False, current_player)
            state = next_state
            self.env.switch_player()
        self.env.reset_board()
        return winner 
    
    def simulate(self):
        for ep in range(self.num_episodes):
            winner = self.play_game()
            if ep % 50000 == 0:
                print(f"Episode={ep}, Winner={winner}")

            self.agent.eps = max(0.01, self.agent.eps*0.9999)
        self.agent.save_q_weights()


def main():
    train = simulation()
    train.simulate()

if __name__ == "__main__":
    main()