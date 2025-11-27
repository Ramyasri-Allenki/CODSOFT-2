#!/usr/bin/env python3
"""
tic_tac_toe_ai.py
Unbeatable Tic-Tac-Toe using Minimax with Alpha-Beta pruning.
Single-file, console-based. Python 3.8+
"""
from typing import List, Optional, Tuple


class Board:
    def __init__(self):
        # cells indexed 0..8, row-major:
        # 0 1 2
        # 3 4 5
        # 6 7 8
        self.cells: List[str] = [' '] * 9

    def make_move(self, idx: int, player: str) -> bool:
        if 0 <= idx < 9 and self.cells[idx] == ' ':
            self.cells[idx] = player
            return True
        return False

    def available_moves(self) -> List[int]:
        return [i for i, v in enumerate(self.cells) if v == ' ']

    def is_full(self) -> bool:
        return all(c != ' ' for c in self.cells)

    def winner(self) -> Optional[str]:
        lines = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
            (0, 4, 8), (2, 4, 6)              # diags
        ]
        for a, b, c in lines:
            if self.cells[a] != ' ' and self.cells[a] == self.cells[b] == self.cells[c]:
                return self.cells[a]
        return None

    def clone(self) -> 'Board':
        b = Board()
        b.cells = self.cells.copy()
        return b

    def pretty(self) -> str:
        rows = [self.cells[i*3:(i+1)*3] for i in range(3)]
        lines = []
        for r in range(3):
            lines.append(f" {rows[r][0]} | {rows[r][1]} | {rows[r][2]} ")
            if r < 2:
                lines.append("---+---+---")
        return "\n".join(lines)

    def print_with_indices(self) -> None:
        print("Positions (index):")
        print(" 0 | 1 | 2 ")
        print("---+---+---")
        print(" 3 | 4 | 5 ")
        print("---+---+---")
        print(" 6 | 7 | 8 ")
        print()


class AI:
    def __init__(self, ai_player: str, human_player: str):
        self.ai = ai_player
        self.human = human_player

    def choose_move(self, board: Board) -> int:
        """Return best move index for ai_player on given board."""
        best_score = -float('inf')
        best_move = -1
        for move in board.available_moves():
            clone = board.clone()
            clone.make_move(move, self.ai)
            # we pass depth=1 because we've made one move
            score = self._minimax(clone, False, -float('inf'), float('inf'), depth=1)
            if score > best_score:
                best_score = score
                best_move = move
        # Fallback: choose first available if something odd happens
        return best_move if best_move != -1 else (board.available_moves() or [0])[0]

    def _minimax(self, board: Board, is_maximizing: bool, alpha: float, beta: float, depth: int) -> float:
        """
        Minimax with alpha-beta pruning.
        Scores: win = +10 - depth (prefer faster wins), loss = -10 + depth (prefer slower losses),
                draw = 0
        """
        winner = board.winner()
        if winner == self.ai:
            return 10 - depth
        if winner == self.human:
            return -10 + depth
        if board.is_full():
            return 0

        if is_maximizing:
            value = -float('inf')
            for move in board.available_moves():
                clone = board.clone()
                clone.make_move(move, self.ai)
                score = self._minimax(clone, False, alpha, beta, depth + 1)
                value = max(value, score)
                alpha = max(alpha, value)
                if alpha >= beta:
                    break  # beta cutoff
            return value
        else:
            value = float('inf')
            for move in board.available_moves():
                clone = board.clone()
                clone.make_move(move, self.human)
                score = self._minimax(clone, True, alpha, beta, depth + 1)
                value = min(value, score)
                beta = min(beta, value)
                if alpha >= beta:
                    break  # alpha cutoff
            return value


def choose_symbol() -> Tuple[str, str]:
    while True:
        choice = input("Choose your symbol (X/O). X goes first: ").strip().upper()
        if choice in ('X', 'O'):
            human = choice
            ai = 'O' if human == 'X' else 'X'
            return human, ai
        print("Invalid choice. Enter X or O.")


def human_move(board: Board, human_symbol: str) -> None:
    board.print_with_indices()
    while True:
        raw = input("Enter your move (0-8): ").strip()
        if not raw.isdigit():
            print("Please enter a number between 0 and 8.")
            continue
        idx = int(raw)
        if idx not in range(9):
            print("Index out of range. Use 0-8.")
            continue
        if board.cells[idx] != ' ':
            print("Cell already taken. Pick another.")
            continue
        board.make_move(idx, human_symbol)
        break


def main() -> None:
    print("Jai Shree Ram 🙏")
    print("Tic-Tac-Toe — Human vs Unbeatable AI (Minimax + Alpha-Beta)\n")
    human_symbol, ai_symbol = choose_symbol()
    board = Board()
    ai = AI(ai_symbol, human_symbol)

    current = 'X'  # X always goes first
    while True:
        print("\nCurrent board:")
        print(board.pretty())
        winner = board.winner()
        if winner or board.is_full():
            break

        if current == human_symbol:
            print("\nYour turn.")
            human_move(board, human_symbol)
        else:
            print("\nAI's turn. AI is thinking...")
            move = ai.choose_move(board)
            board.make_move(move, ai_symbol)
            print(f"AI chooses position {move}.")

        # check for end after the move
        winner = board.winner()
        if winner:
            print("\nFinal board:")
            print(board.pretty())
            if winner == human_symbol:
                print("\nCongratulations — you win!")
            else:
                print("\nAI wins. Better luck next time!")
            return

        if board.is_full():
            print("\nFinal board:")
            print(board.pretty())
            print("\nIt's a draw!")
            return

        # switch
        current = 'O' if current == 'X' else 'X'

    # final check (fallback)
    print("\nFinal board:")
    print(board.pretty())
    if board.winner() == human_symbol:
        print("\nCongratulations — you win!")
    elif board.winner() == ai_symbol:
        print("\nAI wins. Better luck next time!")
    else:
        print("\nIt's a draw!")


if __name__ == "__main__":
    main()
