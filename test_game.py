"""
All tests in one file.
"""

import copy
from game import (
    _collapse_row_left,
    move_left,
    move_right,
    move_up,
    move_down,
    spawn_tile,
    won_game,
    lost_game,
    create_initial_board,
    Direction,
)
from ai import suggest_move


def test_create_initial_board():
    board = create_initial_board(size=4)
    tiles = []
    for r in range(len(board)):
        for c in range(len(board)):
            if board[r][c] is not None:
                tiles.append(board[r][c])
    assert 2 <= len(tiles) <= 8
    assert all(t == 2 for t in tiles)


def test_spawn_tile_places_one_tile():
    board = [[None] * 4 for _ in range(4)]
    spawn_tile(board)
    tiles = []
    for row in board:
        for cell in row:
            if cell is not None:
                tiles.append(cell)
    assert len(tiles) == 1
    assert tiles[0] in (2, 4)


def test_spawn_tile_does_nothing_when_full():
    board = [
        [2, 4, 2, 4],
        [4, 2, 4, 2],
        [2, 4, 2, 4],
        [4, 2, 4, 2],
    ]
    original = copy.deepcopy(board)
    spawn_tile(board)
    assert board == original


def test_collapse_row_left_one():
    assert _collapse_row_left([2, None, 2, 4]) == [4, 4, None, None]


def test_collapse_row_left_two():
    empty = [None, None, None, None]
    assert _collapse_row_left(empty) == [None, None, None, None]


def test_collapse_row_left_three():
    assert _collapse_row_left([None, 2, None, 2]) == [4, None, None, None]


def test_collapse_row_left_four():
    assert _collapse_row_left([2, 2, 2, 2]) == [4, 4, None, None]


def test_collapse_row_left_five():
    assert _collapse_row_left([None, 2, 2, 4]) == [4, 4, None, None]


def test_collapse_row_left_six():
    assert _collapse_row_left([4, 2, 2, 4]) == [4, 4, 4, None]


def test_move_left():
    board = [
        [None, 8, 2, 2],
        [4, 2, None, 2],
        [None, None, None, None],
        [None, None, None, 2],
    ]
    new_board, changed = move_left(board)
    assert new_board == [
        [8, 4, None, None],
        [4, 4, None, None],
        [None, None, None, None],
        [2, None, None, None],
    ]
    assert changed


def test_move_right():
    board = [
        [None, 8, 2, 2],
        [4, 2, None, 2],
        [None, None, None, None],
        [None, None, None, 2],
    ]
    new_board, changed = move_right(board)
    assert new_board == [
        [None, None, 8, 4],
        [None, None, 4, 4],
        [None, None, None, None],
        [None, None, None, 2],
    ]
    assert changed


def test_move_up():
    board = [
        [None, 8, 2, 2],
        [4, 2, None, 2],
        [None, None, None, None],
        [None, None, None, 2],
    ]
    new_board, changed = move_up(board)
    assert new_board == [
        [4, 8, 2, 4],
        [None, 2, None, 2],
        [None, None, None, None],
        [None, None, None, None],
    ]
    assert changed


def test_move_down():
    board = [
        [None, 8, 2, 2],
        [4, 2, None, 2],
        [None, None, None, None],
        [None, None, None, 2],
    ]
    new_board, changed = move_down(board)
    assert new_board == [
        [None, None, None, None],
        [None, None, None, None],
        [None, 8, None, 2],
        [4, 2, 2, 4],
    ]
    assert changed


def test_win():
    board = [
        [2048, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
    ]
    assert won_game(board)


def test_lose():
    board = [
        [2, 4, 2, 4],
        [4, 2, 4, 2],
        [2, 4, 2, 4],
        [4, 2, 4, 2],
    ]
    _, changed = move_left(board)

    assert not changed
    assert lost_game(board)


def test_suggest_move_returns_a_direction():
    # Any board with possible merges
    # AI should prompt any direction
    board = [
        [2, 2, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
    ]
    result = suggest_move(board)
    assert result in (
        Direction.LEFT,
        Direction.RIGHT,
        Direction.UP,
        Direction.DOWN,
    )


def test_suggest_move_returns_none_when_stuck():
    # Alternating board. No two adjacent tiles are equal so no move possible
    # AI cannot give any suggestions
    board = [
        [2, 4, 2, 4],
        [4, 2, 4, 2],
        [2, 4, 2, 4],
        [4, 2, 4, 2],
    ]
    assert suggest_move(board) is None


def test_suggest_move_picks_best_direction():
    # Left/right each merge 4 pairs - 8 empty cells
    # Up/down can't merge - fewer empty cells
    # AI should pick left or right
    board = [
        [2, 2, None, None],
        [2, 2, None, None],
        [2, 2, None, None],
        [2, 2, None, None],
    ]
    assert suggest_move(board) in (Direction.LEFT, Direction.RIGHT)
