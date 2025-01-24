import json
import time
import chess
import chess.engine
import asyncio
import random
import pyautogui

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
    file_map = "abcdefgh"
    rank = square_id[1]
    file = file_map[int(square_id[0]) - 1]
    return f"{file}{rank}"

def square_trans(gg):
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
    try:
        with open(JSON_FILE_PATH, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return None

def reverse_move(chess_move):
    return chess_move[2:4] + chess_move[0:2]

def generate_square_coordinates(a1, h8):
    coordinates = {}
    square_width = (h8[0] - a1[0]) / 7
    square_height = (a1[1] - h8[1]) / 7

    files = "abcdefgh"
    for rank in range(8): 
        for file_index in range(8): 
            square = f"{files[file_index]}{8 - rank}" 
            x = a1[0] + file_index * square_width
            y = a1[1] - rank * square_height
            coordinates[square] = (int(x), int(y))
    
    return coordinates

a1_coords = (291,902) 
h8_coords = (913,278) 

square_coordinates = generate_square_coordinates(a1_coords, h8_coords)

for square, coord in square_coordinates.items():
    print(f"{square}: {coord}")

async def make_move(engine, board):
    result = engine.play(board, chess.engine.Limit(time=2.0))
    stockfish_move = result.move
    from_square = chess.square_name(stockfish_move.from_square)
    to_square = chess.square_name(stockfish_move.to_square)

    if from_square in square_coordinates and to_square in square_coordinates:
        #pyautogui.click(square_coordinates[from_square])  # Click source square
        #time.sleep(random.randint(1,5))                                   # Add delay
        #pyautogui.click(square_coordinates[to_square])    # Click destination square
        print(f"Clicked from {from_square} to {to_square}.")
    else:
        print(f"Coordinates for {from_square} or {to_square} not found.")


async def next_move(color):
    if color == "white":
        return "black"
    if color == "black":
        return "white"


async def detect_new_moves(processed_moves, color, engine, board):
    global currentmoves
    first_move = True
    whos_move = ""
    to_reverse = await next_move(color)
    print(f'color {color}  to rev {to_reverse}')

    while True:
        game_data = load_game_data()
        if not game_data or not game_data.get("gamestate"):
            time.sleep(1)
            continue
        moves = game_data.get("moves", [])
        for move in moves:
            first_move = False
            move_string = move.get("move")
            if move_string and move_string not in processed_moves:
                move_notation = square_trans(move_string)
                if move_notation:
                    print(move_notation)
                    if currentmoves % 2 > 0:
                        whos_move = "black"
                        if to_reverse == whos_move:
                            move_notation = reverse_move(move_notation)
                    else:
                        whos_move = "white"
                        if to_reverse == whos_move:
                            move_notation = reverse_move(move_notation)

                    print(f"{whos_move} Moved: {move_notation}")
                    board.push_san(move_notation)
                    print('----------------------------------------')
                    print(f'Now {await next_move(whos_move)} Turn:')
                    if color == await next_move(whos_move):
                        print('Our Turn:')
                        await make_move(engine, board)

                    currentmoves += 1
                    processed_moves.add(move_string)
        
        if first_move:
            if color == "white":
                print('our First move')
                first_move = False
                await make_move(engine,board)

        time.sleep(1)

async def main():
    processed_moves = set()
    engine, board = initialize_board()
    await detect_new_moves(processed_moves, "black", engine, board)

if __name__ == "__main__":
    asyncio.run(main())
