"""
This is the environment file 
Recieves the action 
Returns the observation/state and the reward recieved for the action
"""

class ticTacToe:
    def __init__(self):
        self.reset_board()
        
    def reset_board(self):
        self.board = ["-" for _ in range(9)]
        self.current_player = "x"
    
    def make_move(self, pos):
        """
        Recieves only valid moves
        """
        if self.board[pos] == "-":
            self.board[pos] = self.current_player
            return True
        return False

    def switch_player(self):
        self.current_player = "o" if self.current_player == "x" else "x"

    def check_state(self):
        """
        Checks the state of the board afte the move:w
        """
        winning_combos = [[0,1,2], [3,4,5], [6,7,8], [0,4,8], [2,4,6]]
        for combo in winning_combos:
            if ("-" not in [self.board[combo[0]], self.board[combo[1]], self.board[combo[2]]]) and (self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]]):
                if self.current_player == self.board[combo[0]]:
                    reward = 1
                    termination = True
                    reason = f"{self.current_player}"
                else:
                    reward = -1
                    termination = True
                    reason = "o" if self.current_player == "x" else "o"
                return reward, termination, reason
        if "-" not in self.board:
            reward = 0
            termination = True
            reason = "tie!"
            return reward, termination, reason        
        return 0, False, None

    def get_state(self):
        return "".join(self.board)

    def available_moves(self):
        return [i for i in range(9) if self.board[i] == "-"]

