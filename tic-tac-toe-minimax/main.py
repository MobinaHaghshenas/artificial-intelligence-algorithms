
# Tic-Tac-Toe AI: Minimax and Alpha-Beta Pruning

POSITIONS = {
    1: (0, 0), 2: (0, 1), 3: (0, 2),
    4: (1, 0), 5: (1, 1), 6: (1, 2),
    7: (2, 0), 8: (2, 1), 9: (2, 2),
}


class Game:
    def __init__(self):
        self.counter = 0
        self.initialize_game()

    def initialize_game(self):
        self.current_state = [
            ['.', '.', '.'],
            ['.', '.', '.'],
            ['.', '.', '.']
        ]
        self.player_turn = 'X'

    def draw_board(self):
        print("\n  1   2   3")
        for i, row in enumerate(self.current_state):
            print(f"{i + 1} " + " | ".join(row))
            if i < 2:
                print("  ---------")
        print()

    def is_valid(self, row, col):
        return (
            0 <= row < 3
            and 0 <= col < 3
            and self.current_state[row][col] == '.'
        )

    def is_end(self):
        board = self.current_state

        # Check rows
        for row in board:
            if row[0] != '.' and row[0] == row[1] == row[2]:
                return row[0]

        # Check columns
        for col in range(3):
            if (
                board[0][col] != '.'
                and board[0][col] == board[1][col] == board[2][col]
            ):
                return board[0][col]

        # Check diagonals
        if (
            board[0][0] != '.'
            and board[0][0] == board[1][1] == board[2][2]
        ):
            return board[0][0]

        if (
            board[0][2] != '.'
            and board[0][2] == board[1][1] == board[2][0]
        ):
            return board[0][2]

        # Check for an empty cell
        if any('.' in row for row in board):
            return None

        # A full board with no winner is a draw
        return '.'

    def evaluate(self):
        """Return +1 for an O win, -1 for an X win, and 0 for a draw."""
        result = self.is_end()

        if result == 'O':
            return 1
        if result == 'X':
            return -1
        return 0

    def minimax(self):
        """Return (score, row, col) using Minimax."""
        self.counter += 1

        result = self.is_end()

        if result is not None:
            return self.evaluate(), None, None

        if self.player_turn == 'O':
            best_score = float('-inf')
            best_move = (None, None)

            for row in range(3):
                for col in range(3):
                    if self.current_state[row][col] == '.':
                        self.current_state[row][col] = 'O'
                        self.player_turn = 'X'

                        score, _, _ = self.minimax()

                        self.current_state[row][col] = '.'
                        self.player_turn = 'O'

                        if score > best_score:
                            best_score = score
                            best_move = (row, col)

            return best_score, best_move[0], best_move[1]

        best_score = float('inf')
        best_move = (None, None)

        for row in range(3):
            for col in range(3):
                if self.current_state[row][col] == '.':
                    self.current_state[row][col] = 'X'
                    self.player_turn = 'O'

                    score, _, _ = self.minimax()

                    self.current_state[row][col] = '.'
                    self.player_turn = 'X'

                    if score < best_score:
                        best_score = score
                        best_move = (row, col)

        return best_score, best_move[0], best_move[1]

    def minimax_alpha_beta(self, alpha=float('-inf'), beta=float('inf')):
        """Return (score, row, col) using Minimax with Alpha-Beta Pruning."""
        self.counter += 1

        result = self.is_end()

        if result is not None:
            return self.evaluate(), None, None

        if self.player_turn == 'O':
            best_score = float('-inf')
            best_move = (None, None)

            for row in range(3):
                for col in range(3):
                    if self.current_state[row][col] == '.':
                        self.current_state[row][col] = 'O'
                        self.player_turn = 'X'

                        score, _, _ = self.minimax_alpha_beta(alpha, beta)

                        self.current_state[row][col] = '.'
                        self.player_turn = 'O'

                        if score > best_score:
                            best_score = score
                            best_move = (row, col)

                        alpha = max(alpha, best_score)

                        if alpha >= beta:
                            return best_score, best_move[0], best_move[1]

            return best_score, best_move[0], best_move[1]

        best_score = float('inf')
        best_move = (None, None)

        for row in range(3):
            for col in range(3):
                if self.current_state[row][col] == '.':
                    self.current_state[row][col] = 'X'
                    self.player_turn = 'O'

                    score, _, _ = self.minimax_alpha_beta(alpha, beta)

                    self.current_state[row][col] = '.'
                    self.player_turn = 'X'

                    if score < best_score:
                        best_score = score
                        best_move = (row, col)

                    beta = min(beta, best_score)

                    if beta <= alpha:
                        return best_score, best_move[0], best_move[1]

        return best_score, best_move[0], best_move[1]

    def get_human_move(self):
        while True:
            try:
                position = int(input("Choose a position (1-9): "))
            except ValueError:
                print("Invalid input. Please enter an integer from 1 to 9.")
                continue

            if position not in POSITIONS:
                print("Invalid position. Choose a number from 1 to 9.")
                continue

            row, col = POSITIONS[position]

            if not self.is_valid(row, col):
                print("That position is occupied. Choose an empty position.")
                continue

            return row, col

    def play(self, use_alpha_beta=False):
        self.initialize_game()
        self.counter = 0

        algorithm_name = (
            "Minimax with Alpha-Beta Pruning"
            if use_alpha_beta
            else "Minimax"
        )

        print(f"\nTic-Tac-Toe AI - {algorithm_name}")
        print("You are X. The AI is O.")
        print("Choose positions using the numbered board.")

        while True:
            self.draw_board()
            result = self.is_end()

            if result is not None:
                if result == 'X':
                    print("You win!")
                elif result == 'O':
                    print("The AI wins!")
                else:
                    print("It's a draw!")

                print(f"Search function calls: {self.counter}")
                break

            if self.player_turn == 'X':
                row, col = self.get_human_move()
                self.current_state[row][col] = 'X'
                self.player_turn = 'O'

            else:
                self.counter = 0

                if use_alpha_beta:
                    score, row, col = self.minimax_alpha_beta()
                else:
                    score, row, col = self.minimax()

                if row is None or col is None:
                    print("No valid move was found.")
                    break

                position = row * 3 + col + 1
                print(
                    f"AI recommends position {position} "
                    f"(score: {score})."
                )

                self.current_state[row][col] = 'O'
                self.player_turn = 'X'

                print(f"Search function calls for this move: {self.counter}")


def main():
    game = Game()

    while True:
        print("\nSelect an algorithm:")
        print("0 - Minimax")
        print("1 - Minimax with Alpha-Beta Pruning")
        print("q - Quit")

        choice = input("Your choice: ").strip().lower()

        if choice == 'q':
            print("Goodbye!")
            break
        elif choice == '0':
            game.play(use_alpha_beta=False)
        elif choice == '1':
            game.play(use_alpha_beta=True)
        else:
            print("Invalid choice. Enter 0, 1, or q.")


if __name__ == "__main__":
    main()
