import sys
import logging
sys.path.append('C:/Users/zulst/Desktop/origin monte_carlo')
import time
from chess import Board
from mctchess.players import Player
from threading import Thread
from mctchess.window.window import MainWindow
from PyQt5.QtWidgets import QApplication

class Game:
    def __init__(
        self,
        player_1: Player,
        player_2: Player,
        board: Board,
        verbose: bool = False,
    ):
        self.white_player = player_1
        self.black_player = player_2
        self.board = (
            board if board else Board()
        )  #  initial position if no speceific board is provided
        self.verbose = verbose
        self.game_history = list()
        

    def turn(self) -> bool:
        return self.board.turn
    
    def compute_next_move(self) -> str:
        player = self.white_player if self.turn() else self.black_player
        logging.debug("White go") if self.turn() else logging.debug("Black go")
        move = player.play(self.board)
        return move

    def save_move_in_history(self, move: str) -> None:
        self.game_history.append(move)
        logging.debug(move)

    def execute_next_move(self) -> None:
        move = self.compute_next_move()
        self.board.push_san(move)
        self.save_move_in_history(move)

    def is_finished(self) -> bool:
        return self.board.is_game_over()

    def play_n_moves(self, no_moves: int) -> None:
        for _ in range(no_moves):
            self.execute_next_move()

    def play_game(self) -> None:
        time_white = 0
        turn_white = 0
        time_black = 0
        turn_black = 0
        while not self.is_finished():
            start = time.time()
            # self.execute_next_move()
            # self.save_move_in_history(self.compute_next_move())
            # print("Next move can be: ", self.execute_next_move())
            self.execute_next_move()
            # print(self.execute_next_move())
            Time=(time.time()-start)
            if self.turn():
                time_black = (time_black * turn_black + Time) / (turn_black + 1)
                turn_black += 1
            else: 
                time_white = (time_white * turn_white + Time) / (turn_white + 1)
                turn_white += 1
            logging.debug("Time for this move: {}".format(Time))
            logging.debug("Time average of white: {}".format(time_white) )
            logging.debug("Time average of black: {}".format(time_black) )
            if self.verbose and self.board.ply() % 20 == 0:
                logging.debug(f"{self.board.ply()} turns played")

        if self.verbose:
            logging.debug(f"Game ended with result: {self.board.result()}")

    def run_game(self, showChoice: bool) -> None:
        app = QApplication([])
        window = MainWindow()
        window.chessboard = self.board
        if(showChoice):
            window.show()
        threadRunGame = Thread(target=self.play_game)
        threadRunGame.start()
        app.exec_()