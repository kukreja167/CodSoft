"""
Tic-Tac-Toe Game (Human vs AI)

Highlights:
- 3x3 ASCII board display
- Human vs AI gameplay
- Smart AI (Minimax with Alpha-Beta Pruning)
- Input validation and replay option
"""

import math

# Constants
BLANK = ' '
X_PLAYER = 'X'
O_PLAYER = 'O'


class Board:
    def __init__(self):
        self.cells = [BLANK] * 9

    def show(self):
        b = self.cells
        layout = [
            f" {b[0]} | {b[1]} | {b[2]} ",
            "---+---+---",
            f" {b[3]} | {b[4]} | {b[5]} ",
            "---+---+---",
            f" {b[6]} | {b[7]} | {b[8]} "
        ]
        print("\n".join(layout))

    def available_moves(self):
        return [i for i, c in enumerate(self.cells) if c == BLANK]

    def make_move(self, index, player):
        if self.cells[index] != BLANK:
            raise ValueError("Cell already occupied.")
        self.cells[index] = player

    def undo_move(self, index):
        self.cells[index] = BLANK

    def get_result(self):
        c = self.cells
        combos = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for a, b, d in combos:
            if c[a] == c[b] == c[d] and c[a] != BLANK:
                return c[a]
        if BLANK not in c:
            return 'Draw'
        return None

    def is_finished(self):
        return self.get_result() is not None


# Minimax Algorithm with Alpha-Beta Pruning
def minimax(board, depth, is_max_turn, ai, human, alpha=-math.inf, beta=math.inf):
    result = board.get_result()

    if result == ai:
        return 10 - depth, None
    elif result == human:
        return depth - 10, None
    elif result == 'Draw':
        return 0, None

    if is_max_turn:
        best_val = -math.inf
        best_move = None
        for move in board.available_moves():
            board.make_move(move, ai)
            value, _ = minimax(board, depth + 1, False, ai, human, alpha, beta)
            board.undo_move(move)
            if value > best_val:
                best_val = value
                best_move = move
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return best_val, best_move
    else:
        best_val = math.inf
        best_move = None
        for move in board.available_moves():
            board.make_move(move, human)
            value, _ = minimax(board, depth + 1, True, ai, human, alpha, beta)
            board.undo_move(move)
            if value < best_val:
                best_val = value
                best_move = move
            beta = min(beta, value)
            if beta <= alpha:
                break
        return best_val, best_move


def get_ai_move(board, ai, human):
    _, move = minimax(board, 0, True, ai, human)
    return move


def parse_move(inp, valid_moves):
    inp = inp.strip()
    if inp.isdigit():
        pos = int(inp) - 1
        if pos in valid_moves:
            return pos
    return None


def play():
    print("=== Welcome to Tic-Tac-Toe ===\n")

    game = Board()

    # Choose symbol
    while True:
        choice = input("Pick your symbol (X/O): ").strip().upper()
        if choice in ('X', 'O'):
            human = choice
            ai = O_PLAYER if human == X_PLAYER else X_PLAYER
            break
        print("Please choose X or O.")

    # Choose who starts
    while True:
        first = input("Who goes first? (H for Human / A for AI) [Default: H]: ").strip().upper()
        if first == '' or first.startswith('H'):
            turn = 'H'
            break
        elif first.startswith('A'):
            turn = 'A'
            break
        else:
            print("Enter H or A.")

    print("\nPositions are numbered as follows:")
    print(" 1 | 2 | 3\n---+---+---\n 4 | 5 | 6\n---+---+---\n 7 | 8 | 9")
    print("\nLet's begin!\n")

    while True:
        game.show()

        if game.is_finished():
            result = game.get_result()
            if result == 'Draw':
                print("\nIt's a draw!")
            else:
                print(f"\n{result} wins the game!")
            break

        if turn == 'H':
            while True:
                move = parse_move(input("Your move (1–9): "), game.available_moves())
                if move is not None:
                    try:
                        game.make_move(move, human)
                        break
                    except ValueError:
                        print("That spot’s taken, try again.")
                else:
                    print("Invalid input. Choose a valid number 1–9.")
            turn = 'A'
        else:
            print("\nAI is calculating its move...")
            move = get_ai_move(game, ai, human)
            if move is None:
                move = game.available_moves()[0]
            game.make_move(move, ai)
            print(f"AI chose position {move + 1}\n")
            turn = 'H'

    print("\nFinal Board:")
    game.show()
    print("\nThanks for playing!")


if __name__ == "__main__":
    play()