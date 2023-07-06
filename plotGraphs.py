import chess.pgn
import matplotlib.pyplot as plt

pgn = open("pgn/output.pgn")
lst = []
while True:
    game = chess.pgn.read_game(pgn)
    if not game:
        break
    lst.append(game.headers.__getitem__("Opening"))

plt.hist(lst)
plt.show()
