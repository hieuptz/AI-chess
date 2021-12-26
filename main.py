import sys
sys.path.append('C:/Users/zulst/Desktop/origin monte_carlo')

from time import time
from chess import Board

from mctchess.game.game import Game
from mctchess.players import Player
from mctchess.players.minimax_player import MiniMaxPlayer
from mctchess.players.random_player import RandomPlayer
from mctchess.players.monte_carlo_player import MCPlayer

def test_n_games(p1: Player, p2: Player, n_games: int, verbose: bool = False) -> list:
    t0 = time()
    results = list()
    for i in range(n_games):
        board = Board()
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
            print(f"Finished {i} games in {(time() - t0) / 60:.2f} mins")
            print(
                f"\nPlayer 1: {results.count('p1')}\nTied games: {results.count('tie')}\nPlayer 2: {results.count('p2')}"
            )
        results.append(winner)
    if verbose:
        print(f"Finished in {(time() - t0)/60:.3f} mins")
        print(
                f"\nFinal Stats:\n\tPlayer 1: {results.count('p1')}\n\tTied games: {results.count('tie')}\n\tPlayer 2: {results.count('p2')}"
            )
    return results

if __name__ == "__main__":

    p1 = MiniMaxPlayer(depth=3, add_mobility=False, ab_pruning=True)
    p2 = RandomPlayer()
    p3 = MCPlayer(n_simulations=20, no_pools=1)
    results = test_n_games(p3, p1, n_games=1, verbose=True)