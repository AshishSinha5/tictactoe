import numpy as np

class ttt:
    def __init__(self):
        self.reset_board()
        self.possible_actions  = ["X", "O"]
        self.current_player = 0
        self.current_index = (None, None)

    def reset_board(self):
        self.board = np.full((3, 3), "_")
        self.current_player = 0
        self.current_index = (None, None)
    
    def do_move(self):
        # do the move at the current possition
        r, c = self.current_index
        self.board[r][c] = self.possible_actions[self.current_player]

    def update_player(self):
        self.current_player = (1 + self.current_player)%2

    def play(self,r ,c):
        #        while True:
        #            self.print_board()
        #            inp = input(f"You are {self.possible_actions[self.current_player]}, Where do you want to play?\n")
        #            try:
        #                r, c  = inp.split(" ")
        #                r, c = int(r), int(c)
        #                self.current_index = (r,c)
        #                if not self.check_valid_move():
        #                    print("Invalid Move, try again")
        #                    continue
        #                else:
        #                    break
        #            except:
        #                print("Invalid Move, try again, enter <row> <col>")
        #                continue
        # recieve action, do move
        self.current_index = (r,c)
        self.do_move()
        terminated, reason, reward = self.check_termination()
        self.update_player()
        return (self.current_player, self.board), reward, terminated, reason

    def check_valid_move(self):
        r,c  = self.current_index
        if r < 0 or c < 0 or r > 2 or c > 2 or self.board[r][c] != "_":
            return False
        return True
    
    def check_termination(self):
        # take the current state of the board, check if ewe have reacjed the termination 
        if self.check_win():
            # print(f"Player {self.possible_actions[self.current_player]} wins")
            return True,f"{self.possible_actions[self.current_player]} wins", 10
        if self.check_end():
            # print(f"Game ended - Its a draw")
            return True, "game draw", 5
        return False, "", -1

    def check_win(self):
        r,c = self.current_index
        # column is marked 
        if not ("_" in [self.board[i][c] for i in range(3)]) and self.board[0][c] == self.board[1][c] == self.board[2][c]:
            return True 
            
        # row is marked -> if no _ in row and all the marks are same
        if not ("_" in self.board[r]) and self.board[r][0] == self.board[r][1] == self.board[r][2]:
            return True

        # diagonal is marked 
        diagonal_indexes =[(0, 0), (2, 0), (1, 1), (0, 2), (2,2)]
        if (r,c) in diagonal_indexes and not any([self.board[r][c] == "_" for r, c in diagonal_indexes]):
            if self.board[0][0] == self.board[1][1] == self.board[2][2] or self.board[0][2] == self.board[1][1] == self.board[2][0]:
                return True

        return False

    def check_end(self):
        if any(["_" in row for row in self.board]):
            return False
        return True
    
    def print_board(self):
        for r in range(3):
            for c in range(3):
                print(self.board[r][c], end = "\t")
            print("\n")

    
def main():
    game = ttt()
    game.play()

if __name__ == "__main__":
    main()
