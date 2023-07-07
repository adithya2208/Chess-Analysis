from re import split
import chess.pgn
import os

INPUT_PGN_PATH = "pgn/ytd_mipola_parsed.pgn"

def getNumberOfGames(pgnPath):
    pgn = open(pgnPath)
    count = 0
    while True:
        game = chess.pgn.read_game(pgn)
        if not game:
            break
        count+=1    
    return count

def getGame(pgnPath,number):
    pgn = open(pgnPath)
    count = 0
    while True:
        game = chess.pgn.read_game(pgn)
        if not game:
            break
        count+=1  
        if count == number:
            return game  
    
    return None
    
def splitPgn(pgnPath,number):
    OUTPUT_PGN_1 = "split1.pgn"
    OUTPUT_PGN_2 = "split2.pgn"
    PGN_TO_WRITE_TO = OUTPUT_PGN_1
    
    if os.path.exists(OUTPUT_PGN_1):
        os.remove(OUTPUT_PGN_1)
    if os.path.exists(OUTPUT_PGN_2):
        os.remove(OUTPUT_PGN_2)
    
    pgn = open(pgnPath)
    count = 0
    while True:
        game = chess.pgn.read_game(pgn)
        if not game:
            break
        count+=1
        if count>number:
            PGN_TO_WRITE_TO = OUTPUT_PGN_2
        outputPgn = open(PGN_TO_WRITE_TO, "a", encoding="utf-8")
        exporter = chess.pgn.FileExporter(outputPgn, comments=True, variations=True)
        game.accept(exporter)
        

print(getNumberOfGames('split1.pgn'))
print(getNumberOfGames('split2.pgn'))
print(getNumberOfGames(INPUT_PGN_PATH))