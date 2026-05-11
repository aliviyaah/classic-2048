"""
Core 2048 game logic — types, board, moves, status.

Pure functions only.
"""
import random
from enum import Enum
from typing import Optional


Board = list[list[Optional[int]]]

WIN_TILE = 2048

class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"


# ---------- board construction ----------

def create_initial_board(size: int = 4) -> Board:
    """
    Initial game state.
    Return a fresh 4x4 board with two `2`s placed at random cells.
    """
    matrix = [[None for _ in range(size)] for _ in range(size)]
    all_cells = [(r, c) for r in range(size) for c in range(size)]
    chosen = random.sample(all_cells, 2)
    for r, c in chosen:
        matrix[r][c] = 2

    return matrix


def spawn_tile(board: Board) -> Board:
    """
    Add one tile to board at a random empty cell.
    Tile is `2` with probability 0.9, `4` with probability 0.1.
    """

    empty = []
    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c] is None:
                empty.append((r, c))

    if empty:
        chosen = random.sample(empty, 1)
        for r, c in chosen:
            values = [2, 4]
            proba = [0.9, 0.1]
            board[r][c] = random.choices(values, weights=proba, k=1)[0]

    return board


# ---------- moves ----------

def _compress_row_left(row: list[Optional[int]]) -> list[Optional[int]]:
    """
    Slide tiles to the left without merging — just remove the Nones and
    pad with Nones on the right. ADD THIS TO WORD DOCUMENT DEL FROM HERE

    Examples:
      [2, None, 2, 4]    -> [2, 2, 4, None]
      [None, None, 4, 2] -> [4, 2, None, None]
      [2, 2, 2, 2]       -> [2, 2, 2, 2]
    """
    n_none = sum([1 for n in row if n is None])
    exists = [r for r in row if r is not None]
    exists = exists + (n_none * [None])

    return exists


def _merge_row_left(row: list[Optional[int]]) -> list[Optional[int]]:
    """
    Merge adjacent equal pairs in a row left-to-right.
    Assumes the row has already been compressed (no Nones between tiles).
    Each tile merges at most once. Leaves Nones where merges happened;
    re-compress afterwards to push them right.

    Examples:
      [2, 2, 4, None]    -> [4, None, 4, None]
      [2, 2, 2, 2]       -> [4, None, 4, None]
      [4, 2, 2, 4]       -> [4, 4, None, 4]
    """
    i = 0
    while i < len(row) - 1:
        if row[i] is not None and row[i] == row[i+1]:
            row[i] = 2 * row[i]
            row[i+1] = None
            i += 2 #Each tile merges at most once per move. Defensive.
        else:
            i += 1

    return row


def _collapse_row_left(row: list[Optional[int]]) -> list[Optional[int]]:
    """
    Full left-collapse: compress, merge, compress again.

    Examples:
      [2, 2, None, None] -> [4, None, None, None]
      [2, 2, 2, 2]       -> [4, 4, None, None]
      [2, None, 2, 4]    -> [4, 4, None, None]
      [4, 2, 2, 4]       -> [4, 4, 4, None]
    """
    return _compress_row_left(_merge_row_left(_compress_row_left(row)))


def _transpose(board: Board) -> Board:
    s = len(board)
    transposed = [[None for _ in range(s)] for _ in range(s)]

    for r in range(len(board)):
        for c in range(len(board)):
            transposed[r][c] = board[c][r]

    return transposed 


def move_left(board: Board) -> tuple[Board, bool]:
    """
    Collapse every row to the left.
    """
    new_board = [_collapse_row_left(r) for r in board]
    changed = False
    if new_board != board:
        changed = True

    return (new_board, changed)
 

def move_right(board: Board) -> tuple[Board, bool]:
    """
    Collapse each row to the right.  
    """
    reversed_board = [r[::-1] for r in board]
    new_board = [_collapse_row_left(r)[::-1] for r in reversed_board]
    changed = False
    if new_board != board:
        changed = True

    return (new_board, changed)


def move_up(board: Board) -> tuple[Board, bool]:
    """
    Collapse every column up.
    """
    transposed_board = _transpose(board)
    rows_left = [_collapse_row_left(r) for r in transposed_board]
    new_board = _transpose(rows_left)
    changed = False
    if new_board != board:
        changed = True

    return (new_board, changed)


def move_down(board: Board) -> tuple[Board, bool]:
    """
    Collapse every column down.
    """
    transposed_board = _transpose(board)
    reversed_transpose = [r[::-1] for r in transposed_board]
    rows_right = [_collapse_row_left(r)[::-1] for r in reversed_transpose]
    new_board = _transpose(rows_right)
    changed = False
    if new_board != board:
        changed = True

    return (new_board, changed)

# ---------- status ----------

def won_game(board: Board) -> bool:
    """Game over if a cell reaches the win tile value."""

    return any(cell == 2048 for row in board for cell in row)


def lost_game(board: Board) -> bool:
    """
    Game over if no move in any direction would change the board.
    """
    _, left_moves = move_left(board)
    _, right_moves = move_right(board)
    _, up_moves = move_up(board)
    _, down_moves = move_down(board)

    # De Morgan's law
    return not (left_moves or right_moves or up_moves or down_moves)