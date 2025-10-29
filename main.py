from __future__ import annotations

import textwrap

from config.game_configuration import (GameStats, configure_game, load_stats,
                                       prompt_play_again, save_stats)
from exceptions import QuitGame
from utils.utils import STATS_FILE, SUPPORTS_COLOR


def print_intro(stats: GameStats) -> None:
    """Prints the welcome game's intro."""

    game_intro = textwrap.dedent(
        f"""
        ============================================================
        Welcome to Smart Tic-Tac-Toe!
        ------------------------------------------------------------
        • Enter positions 0–8 to make your move.
        • Type 'h' at any time for a strategy hint.
        • Type 'q' to quit instantly without losing progress.
        • Your performance is saved automatically between sessions.
        ------------------------------------------------------------
        Current scoreboard → {stats.legacy()}
        ============================================================
        """
    ).strip()
    print(game_intro)


def main() -> None:
    stats = load_stats(STATS_FILE)
    print_intro(stats)

    try:
        while True:
            try:
                game = configure_game(stats, use_color=SUPPORTS_COLOR)
                outcome = game.play_round()

            except QuitGame:
                print('\n👋 Thanks for playing! See you next time.')
                break

            except Exception as e:
                print(f'\nAn unexpected error occurred: {e}')
                continue

            if outcome == 'human':
                stats.record_win()
                print('\n🎉 Congratulations! You won this round.')
            elif outcome == 'system':
                stats.record_loss()
                print('\nThe System prevailed this time. Keep practicing!')
            else:
                stats.record_tie()
                print('\n🤝 It\'s a balanced draw.')

            save_stats(stats, STATS_FILE)
            print(f'Updated scoreboard → {stats.legacy()}')

            try:
                if not prompt_play_again():
                    print('\nFinal scoreboard:', stats.legacy())
                    print('👋 Thanks for playing...Goodbye!')
                    break

            except QuitGame:
                print('\n👋 Exiting...Thanks for playing!')
                break

    except QuitGame:
        print('\n👋 Exiting...Until next time!')

    except KeyboardInterrupt:
        print('\n⌨ Keyboard interrupt detected.\n👋 Exiting gracefully...')

    finally:
        save_stats(stats, STATS_FILE)
