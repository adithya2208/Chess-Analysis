import chess.pgn



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
    
print(getNumberOfGames("pgn/ytd_mipola_parsed.pgn"))
print(getGame("pgn/ytd_mipola_parsed.pgn",550))