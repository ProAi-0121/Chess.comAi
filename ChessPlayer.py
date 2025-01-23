import json
import time
import chess
import chess.engine

JSON_FILE_PATH = "game_data.json"
STOCKFISH_PATH = "stockfish/stockfish.exe"

def initialize_board():
    engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
    board = chess.Board()
    return engine, board

# Use your provided conversion function
def square_to_chess_notation(square_id):
    if square_id[0] == "1":
        result = f"a{square_id[1]}"
    elif square_id[0] == "2":
        result = f"b{square_id[1]}"
    elif square_id[0] == "3":
        result = f"c{square_id[1]}"
    elif square_id[0] == "4":
        result = f"d{square_id[1]}"
    elif square_id[0] == "5":
        result = f"e{square_id[1]}"
    elif square_id[0] == "6":
        result = f"f{square_id[1]}"
    elif square_id[0] == "7":
        result = f"g{square_id[1]}"
    elif square_id[0] == "8":
        result = f"h{square_id[1]}"
    return result

# Convert move to chess notation (e.g., "square-57square-56" to "e7e6")
def convert_to_chess_move(from_square, to_square):
    from_square_chess = square_to_chess_notation(from_square)
    to_square_chess = square_to_chess_notation(to_square)
    return f"{from_square_chess}{to_square_chess}"

# Load game data from the JSON file
def load_game_data():
    try:
        with open(JSON_FILE_PATH, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return None

# Reverse a move for the opponent
def reverse_move(chess_move):
    return chess_move[2:4] + chess_move[0:2]

# Process the moves from JSON and push them to the board
def process_moves_and_push(engine, board, processed_moves, player_color):
    game_data = load_game_data()
    if not game_data:
        print("No game data found.")
        return processed_moves  # Return unprocessed moves set

    if game_data.get("gameStarted"):
        # Get the moves list from the JSON
        moves = game_data.get("moves", [])
        
        move_count = len(moves)  # Number of moves detected

        # For each move, check whether it's the player's turn or opponent's turn
        for move in moves:
            move_string = move["move"]
            from_square = move_string.split("square-")[1].split("square-")[0]
            to_square = move_string.split("square-")[2]

            # Convert move to chess notation
            chess_move = convert_to_chess_move(from_square, to_square)
            print(f"Detected move: {chess_move}")
            
            # Determine whose turn it is based on the move count
            if (move_count % 2 == 0 and player_color == "white") or (move_count % 2 == 1 and player_color == "black"):
                # It's the player's turn to move
                if chess_move not in processed_moves:
                    try:
                        if board.is_legal(chess.Move.from_uci(chess_move)):
                            board.push(chess.Move.from_uci(chess_move))
                            processed_moves.add(chess_move)  # Add to processed moves
                            print(f"Move pushed: {chess_move}")
                        else:
                            print(f"Illegal move detected: {chess_move}")
                    except Exception as e:
                        print(f"Error processing move: {e}")
            else:
                # It's the opponent's turn, reverse the move
                reversed_move = reverse_move(chess_move)
                if reversed_move not in processed_moves:
                    try:
                        if board.is_legal(chess.Move.from_uci(reversed_move)):
                            board.push(chess.Move.from_uci(reversed_move))
                            processed_moves.add(reversed_move)  # Add to processed moves
                            print(f"Opponent's move reversed and pushed: {reversed_move}")
                        else:
                            print(f"Illegal reversed move detected: {reversed_move}")
                    except Exception as e:
                        print(f"Error processing reversed move: {e}")

    return processed_moves  # Return updated set of processed moves

def main():
    engine, board = initialize_board()
    
    processed_moves = set()  # To track moves that have already been processed
    player_color = None  # We'll determine this from the JSON file

    while True:
        game_data = load_game_data()
        if game_data and "playerColor" in game_data:
            player_color = game_data["playerColor"]
            print(f"Your color: {player_color}")

        # Process moves from JSON and push them to the board
        processed_moves = process_moves_and_push(engine, board, processed_moves, player_color)
        
        # If no new moves detected, print a message and wait for the next update
        print("Waiting for the next update...")
        
        time.sleep(1)  # Check the JSON file every 1 second

if __name__ == "__main__":
    main()
