import json
import textwrap
from pathlib import Path
from typing import Dict, Optional

from exceptions import QuitGame
from game_stats import GameStats
from tic_tac_toe import TicTacToeGame
from utils.utils import SystemDifficulty, T
from utils.utils import check_winner as _check_winner
from utils.utils import is_board_full as _is_board_full

check_winner = _check_winner
is_board_full = _is_board_full


def load_stats(path: Path) -> GameStats:
    """Loads stats from the json file path with fallbacks."""

    try:
        if path.exists():
            stat_data = json.loads(path.read_text(encoding='utf-8'))
            return GameStats.from_dict(stat_data)

    except (json.JSONDecodeError, OSError, ValueError) as e:
        print(f'Could not load previous stats ({e})!\nStarting fresh...')

    return GameStats()


def save_stats(stats: GameStats, path: Path) -> None:
    """Persists stats to json file, swallowing IO errors."""

    try:
        path.write_text(json.dumps(
            stats.to_dict(), indent=2), encoding='utf-8'
        )

    except OSError as ose:
        print(
            f'Failed to save stats ({ose}). '
            'Your progress may not persist!'
        )


def prompt_choice(
    prompt: str,
    options: Dict[str, T],
    default: Optional[T] = None
) -> T:
    """
    General-purpose prompt that accepts multiple keyed options.

    Args:
        prompt: The message shown to the user.
        options: Mapping of accepted strings to their result.
        default: Value returned if the user presses Enter without input.

    Raises:
        QuitGame: If user interrupts input (Ctrl+C / Ctrl+D).
    """

    display_choices = ', '.join(dict.fromkeys(options.keys()))
    while True:
        try:
            raw = input(prompt).strip().lower()

        except (EOFError, KeyboardInterrupt) as eof_ki:
            raise QuitGame('Input interrupted by user.') from eof_ki

        if not raw and default is not None:
            return default

        if raw in options:
            return options[raw]

        print(f'Invalid choice!...Accepted options: {display_choices}.')


def configure_game(stats: GameStats, use_color: bool) -> TicTacToeGame:
    """Gathers game configuration from the player."""

    print('\n' + '=' * 60)
    print('🎮 Tic-Tac-Toe Configuration')
    print(f'Current scoreboard → {stats.legacy()}')

    symbol_options: Dict[str, str] = {'x': 'X', 'o': 'O'}
    human_symbol = prompt_choice(
        'Choose your symbol (X/O) [X]: ', symbol_options, default='X'
    )
    system_symbol = 'O' if human_symbol == 'X' else 'X'

    first_default = human_symbol == 'X'
    first_prompt = 'Do you want to move first? (y/n) [{}]: '.format(
        'y' if first_default else 'n'
    )
    first_choices: Dict[str, bool] = {
        'y': True,
        'yes': True,
        'n': False,
        'no': False,
    }
    human_starts = prompt_choice(
        first_prompt, first_choices, default=first_default
    )

    print(
        textwrap.dedent(
            """
            Difficulty levels:
              1) Easy        – Random moves (great for warming up)
              2) Medium – Smart play with a dash of unpredictability
              3) Difficult  – Perfect Minimax system you cannot beat
            """
        ).strip()
    )

    difficulty_options: Dict[str, SystemDifficulty] = {
        '1': SystemDifficulty.EASY,
        'easy': SystemDifficulty.EASY,
        'e': SystemDifficulty.EASY,

        '2': SystemDifficulty.MEDIUM,
        'medium': SystemDifficulty.MEDIUM,
        'm': SystemDifficulty.MEDIUM,
        'challenging': SystemDifficulty.MEDIUM,

        '3': SystemDifficulty.DIFFICULT,
        'hard': SystemDifficulty.DIFFICULT,
        'h': SystemDifficulty.DIFFICULT,
        'difficult': SystemDifficulty.DIFFICULT,
        'impossible': SystemDifficulty.DIFFICULT,
    }

    difficulty = prompt_choice(
        'Select difficulty (1/2/3) [2]: ',
        difficulty_options,
        default=SystemDifficulty.MEDIUM,
    )

    print('\n✅ Configuration complete!')
    print(f'   • You play as {human_symbol}')
    print(f'   • System plays as {system_symbol}')
    print(f'   • You {"will" if human_starts else "will not "} go first')
    print(f'   • Difficulty: {difficulty.value.title()}')

    return TicTacToeGame(
        human_symbol=human_symbol,
        system_symbol=system_symbol,
        human_starts=human_starts,
        system_difficulty=difficulty,
        use_color=use_color,
    )


def prompt_play_again() -> bool:
    """Returns True if the user wants another round."""

    choices: Dict[str, bool] = {
        'y': True,
        'yes': True,
        'n': False,
        'no': False,
    }

    return prompt_choice('Play again? (y/n) [y]: ', choices, default=True)
