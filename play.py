import tkinter as tk
from tkinter import messagebox
import pickle 
from ttt import ttt
from agent import agent
import numpy as np


class ttt_gui:
    def __init__(self, master : tk.Tk):
        self.master = master
        self.master.title("Tic-Tac-Toe with bot")
        self.game = ttt()
        self.bot = agent(eps=0)
        self.load_q_weights()

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_board()

        self.reset_button = tk.Button(master, text="New Game", command=self.reset_game)
        self.reset_button.grid(row = 3, column=0, columnspan=3)
        self.player_turn = True


    def load_q_weights(self):
        with open('q_weights.pkl', 'rb') as f:
            self.bot.Q = pickle.load(f)

    def create_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.master, text="", font=('normal', 20), width=5, height=2,
                                               command=lambda row=i, col=j: self.on_click(row, col))
                self.buttons[i][j].grid(row=i, column=j)

    def on_click(self, r, c):
        if self.player_turn and self.game.board[r][c] == "_":
            self.make_move(r, c, "X")
            if not self.check_game_over():
                self.player_turn = False
                self.master.after(500, self.bot_move)

    def bot_move(self):
        state = (1, self.game.board)
        action = self.bot.get_action(state)
        self.make_move(action[0], action[1], "0")
        if not self.check_game_over():
            self.player_turn = True

    def make_move(self, r, c, player):
        self.game.current_index = (r, c)
        self.game.current_player = 0 if player == 'X' else 1
        self.game.do_move()
        self.buttons[r][c].config(text=player)
        
    def check_game_over(self):
        terminated, reason, _ = self.game.check_termination()
        if terminated:
            messagebox.showinfo(reason)
            self.reset_game()
            return True
        return False

    def reset_game(self):
        self.game.reset_board()
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="")
        self.player_turn = True

def main():
    root = tk.Tk()
    ttt_gui(root)
    root.mainloop()

if __name__ == "__main__":
    main()

