"""
UI created from Tkinter.
A thin layer calling game.py and ai.py.
"""

import tkinter as tk
from game import (
    create_initial_board,
    spawn_tile,
    move_left,
    move_right,
    move_up,
    move_down,
    won_game,
    lost_game,
    Direction,
)
from ai import suggest_move

COLOURS = {
    None: "#cdc1b4",
    2: "#eee4da",
    4: "#ede0c8",
    8: "#f2b179",
    16: "#f59563",
    32: "#f67c5f",
    64: "#f65e3b",
    128: "#edcf72",
    256: "#edcc61",
    512: "#edc850",
    1024: "#edc53f",
    2048: "#edc22e",
}

BG = "#faf8ef"

MOVE_FN = {
    Direction.LEFT: move_left,
    Direction.RIGHT: move_right,
    Direction.UP: move_up,
    Direction.DOWN: move_down,
}


def main() -> None:
    state = [create_initial_board()]

    # --- window ---
    root = tk.Tk()
    root.title("2048 game")
    root.config(bg=BG)

    # --- tile grid ---
    grid_frame = tk.Frame(root, bg="#bbada0", padx=4, pady=4)
    grid_frame.pack(padx=10, pady=10)

    tile_labels = []
    for r in range(4):
        row_labels = []
        for c in range(4):
            label = tk.Label(
                grid_frame,
                text="",
                width=4,
                height=2,
                font=("Helvetica", 32, "bold"),
                bg=COLOURS[None],
            )
            label.grid(row=r, column=c, padx=4, pady=4)
            row_labels.append(label)
        tile_labels.append(row_labels)

    # --- status banner ---
    status_label = tk.Label(root, text="", font=("Helvetica", 20, "bold"), bg=BG)
    status_label.pack()

    # --- redraw: sync labels to board state ---
    def redraw():
        board = state[0]
        for r in range(4):
            for c in range(4):
                value = board[r][c]
                tile_labels[r][c].config(
                    text=str(value) if value is not None else "",
                    bg=COLOURS[value],
                )
        if won_game(board):
            status_label.config(text="You win!")
        elif lost_game(board):
            status_label.config(text="Game over!")
        else:
            status_label.config(text="")

    # --- move handler ---
    def on_move(direction):
        board = state[0]
        if won_game(board) or lost_game(board):
            return
        new_board, changed = MOVE_FN[direction](board)
        if changed:
            state[0] = new_board
            spawn_tile(state[0])
        redraw()

    # --- key bindings ---
    root.bind("<Left>", lambda e: on_move(Direction.LEFT))
    root.bind("<Right>", lambda e: on_move(Direction.RIGHT))
    root.bind("<Up>", lambda e: on_move(Direction.UP))
    root.bind("<Down>", lambda e: on_move(Direction.DOWN))

    # --- buttons ---
    button_frame = tk.Frame(root, bg=BG)
    button_frame.pack(pady=6)

    def on_new_game():
        state[0] = create_initial_board()
        suggest_label.config(text="")
        redraw()

    def on_suggest():
        direction = suggest_move(state[0])
        if direction is None:
            suggest_label.config(text="Suggest: no moves left")
        else:
            suggest_label.config(text=f"Suggest: {direction.value.upper()}")

    tk.Button(
        button_frame,
        text="New Game",
        font=("Helvetica", 14),
        command=on_new_game,
    ).pack(side=tk.LEFT, padx=6)
    tk.Button(
        button_frame,
        text="Suggest",
        font=("Helvetica", 14),
        command=on_suggest,
    ).pack(side=tk.LEFT, padx=6)
    suggest_label = tk.Label(button_frame, text="", font=("Helvetica", 14), bg=BG)
    suggest_label.pack(side=tk.LEFT, padx=6)

    redraw()
    root.mainloop()


if __name__ == "__main__":
    main()
