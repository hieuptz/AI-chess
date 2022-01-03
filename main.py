import sys
import logging

from PyQt5.QtWidgets import QApplication

from mctchess import window
from mctchess.window.window import MainWindow
sys.path.append('C:/Users/zulst/Desktop/origin monte_carlo')

from time import time
from chess import Board

from mctchess.game.game import Game
from mctchess.players import Player
from mctchess.players.minimax_player import MiniMaxPlayer
from mctchess.players.random_player import RandomPlayer
from mctchess.players.monte_carlo_player import MCPlayer

from threading import Thread


def test_n_games(p1: Player, p2: Player, n_games: int, logfile: str, verbose: bool = False, board: Board = Board()) -> list:
    logging.basicConfig(filename=logfile, level=logging.DEBUG, format='%(message)s')
    t0 = time()
    results = list()
    for i in range(n_games):
        game = (
            Game(p1, p2, board, verbose=False)
            if i % 2 == 0
            else Game(p2, p1, board, verbose=False)
        )
        game.play_game()
        outcome = board.outcome().winner
        if outcome is None:
            winner = "tie"
        elif i % 2 == 0 and outcome is True:
            winner = "p1"
        else:
            winner = "p2"
        if verbose and (i + 1) % 2 == 0:
            logging.debug(f"Finished {i} games in {(time() - t0) / 60:.2f} mins")
            logging.debug(
                f"\nPlayer 1: {results.count('p1')}\nTied games: {results.count('tie')}\nPlayer 2: {results.count('p2')}"
            )
        results.append(winner)
    if verbose:
        logging.debug(f"Finished in {(time() - t0)/60:.3f} mins")
        logging.debug(
                f"\nFinal Stats:\n\tPlayer 1: {results.count('p1')}\n\tTied games: {results.count('tie')}\n\tPlayer 2: {results.count('p2')}"
            )
    return results

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    
    p1 = MiniMaxPlayer(depth=3, add_mobility=False, ab_pruning=True)
    p2 = RandomPlayer()
    p3 = MCPlayer(n_simulations=20, no_pools=1)
    board = Board()
    window.chessboard = board
    val = input("You want to show board (Y/N): ")
    logfile = "a.txt"
    if(val == 'Y'):
        window.show()
    threadStartGame = Thread(target=test_n_games, args=(p2, p1,1, logfile,True, board))
    threadStartGame.start()
    app.exec_()
    