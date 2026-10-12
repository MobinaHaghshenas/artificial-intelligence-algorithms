# Tic-Tac-Toe AI: Minimax and Alpha-Beta Pruning

## Overview

This project is a command-line implementation of Tic-Tac-Toe in Python. A human player uses **X**, and the AI plays as **O**. The program lets the user choose between two adversarial search algorithms:

- **Minimax**
- **Minimax with Alpha-Beta Pruning**

The project demonstrates recursive game-tree search, terminal-state evaluation, move selection, and a simple way to inspect search effort.

## Features

- Play Tic-Tac-Toe against an AI in the terminal.
- Choose Minimax or Minimax with Alpha-Beta Pruning at launch.
- Detect wins, losses, and draws.
- Reject non-integer input, positions outside `1–9`, and occupied cells.
- Display the AI's selected move and its evaluation score.
- Count calls to the search function for each AI move.

## Algorithms

### Minimax

Minimax explores possible future game states recursively. In this implementation, the AI (`O`) is the maximizing player and the human (`X`) is the minimizing player.

Terminal states are scored from the AI's perspective:

| Outcome | Score |
|---|---:|
| AI (`O`) wins | `+1` |
| Draw | `0` |
| Human (`X`) wins | `-1` |

The AI selects a move with the highest score, assuming both players make optimal decisions.

### Alpha-Beta Pruning

Alpha-Beta Pruning uses the same Minimax evaluation but maintains two bounds:

- **Alpha** is the best score found so far for the maximizing player.
- **Beta** is the best score found so far for the minimizing player.

When a branch cannot affect the final decision, the algorithm stops exploring that branch. This can reduce the number of search calls while preserving the Minimax result.

## Requirements

- Python 3
- No third-party packages are required.

## How to Run

1. Clone or download this repository.
2. Open a terminal in the project directory.
3. Run:

   ```bash
   python main.py
   ```

4. Choose an algorithm:
   - Enter `0` for Minimax.
   - Enter `1` for Minimax with Alpha-Beta Pruning.
   - Enter `q` to quit.
5. When prompted, enter a board position from **1 to 9**.

The positions correspond to this layout:

```text
1 | 2 | 3
---------
4 | 5 | 6
---------
7 | 8 | 9
```

The human plays as **X** and the AI plays as **O**.

## Search Call Counter

The program resets its counter before each AI move and reports the number of calls made to the selected search function. This provides a basic way to compare the two implementations.

For a meaningful comparison, run both algorithms from the same board states. The counter measures search-function calls; it should not be described as a timing benchmark or as a count of every individual operation.

## Implementation Notes

- The board is represented as a 3 × 3 nested Python list.
- Empty cells are represented by `.`.
- The search functions temporarily place a mark, evaluate the resulting states recursively, and restore the board before exploring another move.
- The game ends when a player completes a row, column, or diagonal, or when the board is full with no winner.

## Skills Demonstrated

- Python and object-oriented programming
- Recursion and game-tree search
- Minimax decision-making
- Alpha-Beta Pruning
- Game-state evaluation
- Input validation and command-line interaction
- Basic algorithm-effort comparison

## Scope

This is a small educational project focused on classical adversarial search. It uses a terminal interface and does not include a graphical user interface or a separate automated benchmarking suite.
