import json
import time
import chess
import chess.engine
import asyncio

JSON_FILE_PATH = "game_data.json"
STOCKFISH_PATH = "stockfish/stockfish.exe"
currentmoves = 0

def initialize_board():
    try:
        engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
        board = chess.Board()
        return engine, board
    except Exception as e:
        print(f"Error initializing Stockfish engine: {e}")
        exit(1)

def square_to_chess_notation(square_id):
    """Converts square_id like '12' to proper chess notation."""
    file_map = "abcdefgh"
    rank = square_id[1]
    file = file_map[int(square_id[0]) - 1]  # Convert '1' to 'a', '2' to 'b', etc.
    return f"{file}{rank}"

def square_trans(gg):
    """Parses and converts game move strings."""
    try:
        g1 = gg.split('square')[1].split('-')[1]
        g2 = gg.split('square')[2].split('-')[1]
        first = square_to_chess_notation(g1)
        second = square_to_chess_notation(g2)
        return f"{first}{second}"
    except Exception as e:
        print(f"Error parsing move string '{gg}': {e}")
        return None

def load_game_data():
    """Loads game data from the JSON file."""
    try:
        with open(JSON_FILE_PATH, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return None

def reverse_move(chess_move):
    return chess_move[2:4] + chess_move[0:2]

async def make_move():
    print('move')


async def detect_new_moves(processed_moves, color):
    first_move = True
    global currentmoves
    while True:
        print('lol')
        game_data = load_game_data()
        if not game_data or not game_data.get("gameStarted"):
            time.sleep(1)
            continue
        moves = game_data.get("moves", [])
        for move in moves:
            first_move = False
            move_string = move.get("move")
            if move_string and move_string not in processed_moves:
                move_notation = square_trans(move_string)
                if move_notation:
                    if currentmoves % 2 <= 0:
                        new_notation = reverse_move(move_notation)
                        print(f"New move detected: {new_notation}")
                        print("Now White move") #black did the move
                    else:
                        print(f"New move detected: {move_notation}")
                        print("Now blacks move") #white did the move
                    currentmoves += 1
                    processed_moves.add(move_string)
        
        if first_move:
            if color == "white":
                currentmoves += 1
                print('our First move')
                first_move = False
                await make_move()

        time.sleep(1)

async def main():
    processed_moves = set()
    engine, board = initialize_board()
    await detect_new_moves(processed_moves, "black")

if __name__ == "__main__":
    asyncio.run(main())
