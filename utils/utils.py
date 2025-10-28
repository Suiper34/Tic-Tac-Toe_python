import sys
from enum import Enum
from pathlib import Path
from typing import Sequence, Tuple, TypeVar

from colorama import Fore, Style
from colorama import init as colorama_init

WINNING_COMBINATIONS: Tuple[Tuple[int, int, int], ...] = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)


def check_winner(board: Sequence[str], symbol: str) -> bool:
    """Returns True if the given symbol has a three-in-a-row."""

    return any(all(
        board[i] == symbol for i in combo) for combo in WINNING_COMBINATIONS
    )


def is_board_full(board: Sequence[str]) -> bool:
    """True if no empty squares remain on the board."""

    return all(cell != ' ' for cell in board)


BoardState = Tuple[str, ...]
T = TypeVar('T')
STATS_FILE: Path = Path.cwd() / 'tic_tac_toe_stats.json'
colorama_init(autoreset=True)
SUPPORTS_COLOR = sys.stdout.isatty() and Fore is not None and Style is not None
RESET = Style.RESET_ALL or ''
DIM = Style.DIM or ''
HUMAN_COLOR = Fore.CYAN or ''
SYSTEM_COLOR = Fore.MAGENTA or ''


class SystemDifficulty(str, Enum):
    """Supported Ggame System difficulty tiers."""

    EASY = 'easy'
    MEDIUM = 'medium'
    DIFFICULT = 'difficult'
