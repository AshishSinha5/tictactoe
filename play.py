import tkinter as tk
from tkinter import messagebox
import pickle 
from env import ticTacToe 
from agent import agent
import numpy as np


class ttt_gui:
    def __init__(self, master : tk.Tk):
        self.master = master
        self.master.title("Tic-Tac-Toe with bot")
        self.game = ticTacToe()
        self.bot = agent(eps=0)
        self.load_q_weights()

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_board()

        self.reset_button = tk.Button(master, text="New Game", command=self.reset_game)
        self.reset_button.grid(row = 3, column=0, columnspan=3)
        self.player_turn = np.random.uniform() <= 0.5
        if not self.player_turn:
            self.bot_move()
            self.player_turn = True

    def load_q_weights(self):
        with open('q_table.pkl', 'rb') as f:
            self.bot.q_table = pickle.load(f)

    def create_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.master, text="", font=('normal', 20), width=5, height=2,
                                               command=lambda row=i, col=j: self.on_click(row, col))
                self.buttons[i][j].grid(row=i, column=j)

    def on_click(self, r, c):
        print(self.game.board)
        print(self.player_turn)
        print(r, c)
        if self.player_turn and self.game.board[r*3 + c] == "-":
            self.make_move(r, c, self.game.current_player)
            if not self.check_game_over():
                self.player_turn = False
                self.master.after(500, self.bot_move)

    def bot_move(self):
        state = self.game.get_state()
        player = self.game.current_player
        print(f"bot player = {player}")
        action = self.bot.choose_action(state, player)
        r = action//3
        c = action - 3*r
        self.make_move(r, c, player)
        if not self.check_game_over():
            self.player_turn = True

    def make_move(self, r, c, player):
        self.game.make_move(r*3 + c)
        self.buttons[r][c].config(text=player)
        self.game.switch_player()

    def check_game_over(self):
        _, terminated, reason= self.game.check_state()
        print(f"{terminated = }")
        if terminated:
            print(reason)
            messagebox.showinfo(message = reason)
            self.reset_game()
            return True
        return False

    def reset_game(self):
        self.game.reset_board()
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="")
        self.player_turn = np.random.random() <= 0.5
        if not self.player_turn:
            self.bot_move()
            self.player_turn = True

def main():
    root = tk.Tk()
    ttt_gui(root)
    root.mainloop()

if __name__ == "__main__":
    main()

