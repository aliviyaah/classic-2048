# classic-2048

A Python implementation of 2048.

## Run

```powershell
python ui.py
```

## Test

```powershell
pip install -e ".[dev]"
pytest
```

## Controls

- Arrow keys: move
- `New Game` button: reset
- `Suggest` button: highlights the AI's recommended move

## Architecture

This project has been split into three parts.

```
game.py   pure game logic — types, board, moves, status
ai.py     greedy suggester, 1-step lookahead (depends on game.py)
ui.py     Tkinter front-end (depends on game.py and ai.py)
``` 

## Move logic
Each move is decomposed into compress → merge → compress on rows; right/up/down are implemented by reversing or transposing the board, applying the left move, and inverting. This is the standard decomposition.

## Assumptions

- Board is 4x4.
- Initial board: a random number of `2`s (between 2 and 8) placed at random cells.
- New-tile spawn ratio: 90% `2`, 10% `4`.
- Win condition: any cell reaches 2048.
- Loss condition: board is full AND no move in any direction would change it.

## With more time

- Animations, score + best-score tracking, undo,
  swap heuristic for a learned model (i.e. expectimax)