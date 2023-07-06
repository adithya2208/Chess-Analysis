from chess import Move
import chess.pgn
import chess.engine
import logging
import os
import time

INPUT_PGN_PATH = r"pgn/lichess_mipola_2023-07-05.pgn"
OUTPUT_PGN_PATH = r"pgn/output.pgn"
LOG_OUTPUT = r"chess.log"

DEPTH = 15
GAME_LIMIT = 5
MOVE_LIMIT = 10
PLAYER_NAME = "mipola"

ENGINE_PATH = r"/usr/local/bin/stockfish"
ENGINE_OPTIONS = {"Threads": 2}


def checkWrongMove(prevScore, curScore, move):
    if curScore.is_mate():
        return [True, float("inf")]
    if prevScore.turn:
        cpLost = prevScore.white().score() - curScore.white().score()
    else:
        cpLost = prevScore.black().score() - curScore.black().score()

    if cpLost > 50:
        return [True, cpLost]

    return [False, cpLost]


def pgnCleanup(pgnPath):
    pgn = open(pgnPath)
    outputPgn = pgnPath.replace(".pgn", "_parsed.pgn")
    if os.path.exists(outputPgn):
        return outputPgn
    while True:
        game = chess.pgn.read_game(pgn)
        if not game:
            break
        new_pgn = open(outputPgn, "a", encoding="utf-8")
        exporter = chess.pgn.FileExporter(new_pgn, comments=False, variations=False)
        game.accept(exporter)

    return outputPgn


def main():
    startTime = time.time()

    # Setup logging
    logging.basicConfig(
        filename=LOG_OUTPUT, encoding="utf-8", level=logging.INFO, filemode="w"
    )

    # Setup engine
    engine = chess.engine.SimpleEngine.popen_uci(ENGINE_PATH)
    engine.configure(ENGINE_OPTIONS)

    # Clean the PGN file and remove existing annotations
    parsedPgnPath = pgnCleanup(INPUT_PGN_PATH)
    pgn = open(parsedPgnPath)

    # Remove existing output PGN file
    if os.path.exists(OUTPUT_PGN_PATH):
        os.remove(OUTPUT_PGN_PATH)

    gameCount = 0

    while True:
        game = chess.pgn.read_game(pgn)

        if not game:
            break

        gameCount += 1
        if gameCount > GAME_LIMIT:
            break

        logging.info("gameCount:" + str(gameCount))
        board = game.board()
        info = engine.analyse(
            board, chess.engine.Limit(depth=DEPTH), options=ENGINE_OPTIONS
        )
        prevScore = info["score"]
        nextNode = game
        writeGameToOutput = 0
        playerColor = (
            False if game.headers.__getitem__("Black") == PLAYER_NAME else True
        )
        while True:
            nextNode = nextNode.next()
            if not nextNode:
                break
            if nextNode.ply() > MOVE_LIMIT * 2:
                break

            board = nextNode.board()
            info = engine.analyse(board, chess.engine.Limit(depth=DEPTH))
            nextNode.set_eval(info["score"])
            if not board.is_checkmate():
                mistakeMade, cpLost = checkWrongMove(
                    prevScore, info["score"], nextNode.move.uci()
                )
            if mistakeMade:
                # I am white and it's black's turn now or I am black and it's white's turn
                # Which means I made a mistake
                if (playerColor and nextNode.turn() == False) or (
                    playerColor == False and nextNode.turn()
                ):
                    logging.info("Mistake found!")
                    writeGameToOutput = 1
                    if cpLost > 200:
                        nextNode.nags.add(chess.pgn.NAG_BLUNDER)
                    elif cpLost > 100:
                        nextNode.nags.add(chess.pgn.NAG_MISTAKE)
                    elif cpLost > 50:
                        nextNode.nags.add(chess.pgn.NAG_DUBIOUS_MOVE)

                    # Erase all remaining moves
                    nextNode.variations = []

            prevScore = info["score"]

        if writeGameToOutput:
            new_pgn = open(OUTPUT_PGN_PATH, "a", encoding="utf-8")
            exporter = chess.pgn.FileExporter(new_pgn, comments=True, variations=True)
            game.accept(exporter)

    engine.quit()
    endTime = time.time()
    logging.info("Time elapsed:" + str(endTime - startTime))


main()
