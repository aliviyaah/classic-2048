"""
Greedy AI suggester — offline, no dependencies.

Strategy: try each of the four moves; pick the one that leaves the most
empty cells. Optimise for the most immediate empty space.
"""
from typing import Optional

from game import Board, Direction, move_left, move_right, move_up, move_down


moves = {
    Direction.LEFT: move_left,
    Direction.RIGHT: move_right,
    Direction.UP: move_up,
    Direction.DOWN: move_down,
}


def suggest_move(board: Board) -> Optional[Direction]:
    """
    Return the direction whose resulting board has the most empty cells.
    Returns None if no move would change the board (game over).
    """
    best_direction = None
    best_score = -1

    for direction, move in moves.items():
        new_board, changed = move(board)
        if changed:
            score = 0
            for row in new_board:
                for cell in row:
                    if cell is None:
                        score += 1
            
            if score > best_score:
                best_score = score 
                best_direction = direction
    
    return best_direction