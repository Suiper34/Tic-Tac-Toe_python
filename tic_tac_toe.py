import random
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Dict, List

from config.game_configuration import QuitGame
from utils.utils import (DIM, HUMAN_COLOR, RESET, SYSTEM_COLOR, BoardState,
                         SystemDifficulty, check_winner, is_board_full)


@dataclass
class TicTacToeGame:
    """Encapsulates a complete Tic-Tac-Toe match."""

    human_symbol: str
    system_symbol: str
    human_starts: bool
    system_difficulty: SystemDifficulty
    use_color: bool
    board: List[str] = field(default_factory=lambda: [' '] * 9)

    def reset_board(self) -> None:
        self.board = [' '] * 9

    def get_available_moves(self) -> List[int]:
        return [idx for idx, cell in enumerate(self.board) if cell == ' ']

    def display_board(self) -> None:
        print('\nCurrent board:')
        print(self._board_to_string())

    def _board_to_string(self) -> str:
        rows = []
        for row_start in range(0, 9, 3):
            cells = []
            for idx in range(row_start, row_start + 3):
                value = self.board[idx]
                if value == ' ':
                    placeholder = str(idx)
                    cell_display = f'{DIM}{placeholder}{RESET}' if self.use_color else placeholder
                else:
                    coloured = value
                    if self.use_color:
                        colour = HUMAN_COLOR if value == self.human_symbol else SYSTEM_COLOR
                        coloured = f'{colour}{value}{RESET}'
                    cell_display = coloured
                cells.append(cell_display)
            rows.append(' | '.join(cells))
        separator = '\n' + '-' * 9 + '\n'
        return separator.join(rows)

    def play_round(self) -> str:
        """
        Runs a single round of Tic-Tac-Toe.

        Returns:
            'human', 'system', or 'tie' depending on the outcome.
        """

        self.reset_board()
        current_player = 'human' if self.human_starts else 'system'
        print('\n✨ New round started! Good luck!')
        self.display_board()

        while True:
            if current_player == 'human':
                move = self.prompt_player_move()
                self.board[move] = self.human_symbol

                if check_winner(self.board, self.human_symbol):
                    self.display_board()
                    return 'human'

                if is_board_full(self.board):
                    self.display_board()
                    return 'tie'

                current_player = 'system'
            else:
                move = self.compute_system_move()
                print(
                    f'\n🤖 System ({self.ai_symbol}) chooses position {move}.'
                )
                self.board[move] = self.ai_symbol
                self.display_board()

                if check_winner(self.board, self.ai_symbol):
                    return 'system'

                if is_board_full(self.board):
                    return 'tie'

                current_player = 'human'

    def prompt_player_move(self) -> int:
        """
        Solicits a move from the player, handling commands (hint, quit) and
        errors.
        """

        valid_moves = self.get_available_moves()
        prompt = (
            f'Your move ({self.human_symbol}). Enter a position {valid_moves},'
            " or type 'h' for a hint, 'q' to quit: "
        )

        while True:
            try:
                raw_input = input(prompt).strip().lower()
            except (EOFError, KeyboardInterrupt) as eof_ki:
                raise QuitGame('Input interrupted by user!') from eof_ki

            if raw_input in {'q', 'quit', 'exit'}:
                raise QuitGame('Player requested exit...')

            if raw_input in {'h', 'hint'}:
                self.provide_hint()
                continue

            if not raw_input.isdigit():
                print('Please enter a number or a supported command.')
                continue

            move = int(raw_input)
            if move not in range(9):
                print('Move out of range!...Choose between 0 and 8.')
                continue
            if self.board[move] != ' ':
                print('That square is already taken!...Try another one.')
                continue

            return move

    def provide_hint(self) -> None:
        """Offers a hint based on the Minimax evaluation of available moves."""

        try:
            scores = self._score_moves()

        except RecursionError:
            print('🔍 Hint unavailable right now (search depth exceeded).')
            return

        if not scores:
            print('🔍 No hint available (no remaining moves).')
            return

        best_score: int = max(scores.values())
        best_moves: list[int] = [
            move for move, score in scores.items()
            if score == best_score
        ]

        if best_score > 0:
            message = 'These move(s) set you up to win or force a win:'
        elif best_score == 0:
            message = 'These move(s) should secure at least a draw:'
        else:
            message = 'No winning path—block wisely or hope for a mistake:'

        moves_str: str = ', '.join(str(move) for move in sorted(best_moves))
        print(f'🔍 Hint → {message} {moves_str}')

    def compute_system_move(self) -> int:
        """
        Determines the System's move based on the selected difficulty.
        """

        try:
            if self.system_difficulty == SystemDifficulty.EASY:
                return self._get_system_move_easy()

            if self.system_difficulty == SystemDifficulty.MEDIUM:
                return self._get_system_move_medium()

            return self._get_system_move_difficult()

        except RecursionError:
            print('System fell back to a random move due to recursion depth.')
            return self._get_system_move_easy()

        except Exception as e:
            print(
                f'System encountered an unexpected error: {e}. '
                'Using random move.'
            )
            return self._get_system_move_easy()

    def _get_system_move_easy(self) -> int:
        """Random legal move."""

        moves = self.get_available_moves()
        return random.choice(moves)

    def _get_system_move_medium(self) -> int:
        """
        Strong play with occasional variety to feel less predictable.
        """

        scores = self._score_moves()
        if not scores:
            return self._get_system_move_easy()

        ranked_moves = sorted(
            scores.items(), key=lambda item: item[1], reverse=True
        )
        top_score = ranked_moves[0][1]
        top_moves = [move for move,
                     score in ranked_moves if score == top_score]

        # 30% chance to pick second-best move if available
        if len(ranked_moves) > 1 and random.random() < 0.30:
            return ranked_moves[1][0]

        return random.choice(top_moves)

    def _get_system_move_difficult(self) -> int:
        """Flawless Minimax play."""

        scores = self._score_moves()
        if not scores:
            return self._get_system_move_easy()

        best_score: int = max(scores.values())
        best_moves: list[int] = [
            move for move, score in scores.items()
            if score == best_score
        ]

        return random.choice(best_moves)

    def _score_moves(self) -> Dict[int, int]:
        """
        Evaluates all possible AI moves using Minimax with memoization.

        Returns:
            A mapping of move index to its Minimax score.
        """

        system_symbol = self.system_symbol
        human_symbol = self.human_symbol

        @lru_cache(maxsize=None)
        def minimax(board_state: BoardState,
                    current_symbol: str,
                    depth: int
                    ) -> int:

            board_list = list(board_state)

            if check_winner(board_list, system_symbol):
                return 10 - depth

            if check_winner(board_list, human_symbol):
                return depth - 10

            if is_board_full(board_list):
                return 0

            next_symbol = human_symbol if current_symbol == system_symbol else system_symbol
            if current_symbol == system_symbol:
                best_val = -float('inf')

                for idx, cell in enumerate(board_list):
                    if cell == ' ':
                        board_list[idx] = current_symbol
                        score = minimax(tuple(board_list),
                                        next_symbol, depth + 1)
                        board_list[idx] = ' '
                        best_val = max(best_val, score)

                return best_val

            best_val = float('inf')
            for idx, cell in enumerate(board_list):

                if cell == ' ':
                    board_list[idx] = current_symbol
                    score = minimax(tuple(board_list), next_symbol, depth + 1)
                    board_list[idx] = ' '
                    best_val = min(best_val, score)

            return best_val

        scores: Dict[int, int] = {}
        for move in self.get_available_moves():
            self.board[move] = system_symbol
            score = minimax(tuple(self.board), self.human_symbol, 1)
            self.board[move] = ' '
            scores[move] = score

        return scores
