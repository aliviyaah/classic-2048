# classic-2048

A Python implementation of the 2048 puzzle game, built with Tkinter.

## How to play

Use the arrow keys to slide the tiles. When two tiles with the same number collide, they merge into one. Reach the **2048 tile** to win. Press **New Game** to reset, or **Suggest** to ask the AI for its recommended move.

![2048 game screenshot](2048-ss.png)

## Run

```powershell
python ui.py
```

Tkinter is bundled with Python — no extra install needed to run the game.

## Test

```powershell
pip install -e ".[dev]"
pytest
```

Tests cover all four move functions using the input/output examples from the spec, plus edge cases (all-empty row, all-same tile row, win, lose, AI suggestion). To verify moves interactively, run the game with `python ui.py`.

## Architecture

```
game.py   pure game logic — types, board, moves, win/lose
ai.py     greedy AI suggester, 1-step lookahead (depends on game.py)
ui.py     Tkinter front-end (depends on game.py and ai.py)
```

`game.py` has no side effects — all functions take a board and return a new one. This makes the logic easy to test in isolation and easy to reuse.

## Move logic

Each move is decomposed into **compress → merge → compress** on rows. Right, up, and down are implemented by reversing or transposing the board, applying the left-move primitive, then inverting.

## AI

The AI uses a greedy 1-step lookahead: it tries all four moves and picks whichever leaves the most empty cells. No external dependencies, no credentials.

## Assumptions

- Board is 4×4.
- Initial board: a random number of `2`s (between 2 and 8) placed at random cells. The spec says "a random number" without specifying a range — this felt like the most faithful reading.
- New-tile spawn: 90% `2`, 10% `4`.
- Win: any cell reaches 2048.
- Loss: board is full and no move in any direction changes it.

## With more time

- Animations, score tracking, undo
- Replace greedy heuristic with expectimax for stronger AI