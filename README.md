# Smart Tic-Tac-Toe

A feature-rich, terminal-based Tic-Tac-Toe experience with adaptive game system, persistent win/loss tracking, and optional colorized output. Challenge the computer across three difficulty levels, request strategic hints powered by Minimax, and enjoy a polished user interface.

---

## 🚀 Features

- **Three System tiers**
  - *Easy*: purely random moves
  - *Medium*: strong play with occasional unpredictability
  - *Difficult*: optimal Minimax strategy you cannot beat
- **Interactive hints** to guide your strategy mid-game
- **Persistent scoreboard** stored in `tic_tac_toe_stats.json`
- **Colorized board rendering** (automatically enabled when supported)
- **Graceful quitting** at any prompt without losing progress
- **Robust error handling** and friendly messaging

---

## 📦 Requirements

- Python 3.8 or higher
- Optional: [`colorama`](https://pypi.org/project/colorama/) for colored output on all platforms
- Install it via:

    ```bash
    pip install colorama


## 🛠️ Installation

- Clone or download this repository.
- Ensure dependencies are installed (see above).
- Open a terminal in the project directory.
**▶️ Usage**
- Run the game with:

    ```bash
    python main.py

**Follow the on-screen prompts to**:

1. Choose your symbol (X or O).
2. Decide who moves first.
3. Select an System difficulty.
4. Enter moves using board positions (0–8).
5. Type h for an System-powered hint or q to quit immediately.
6. At the end of each round you can opt to play again, and your cumulative stats will be saved automatically.

## Game System Overview

- **Easy**: selects a random open square.
- **Medium**: evaluates moves with Minimax but occasionally picks a second-best move for variety.
- **Difficult**: uses full Minimax search with memoization (`lru_cache`) to ensure optimal play.

Hints leverage the same Minimax evaluation to recommend moves that maintain or improve your position.

## 💾 Persistance

Game results are stored in `tic_tac_toe_stats.json` in the current working directory. The file is loaded on startup and updated after each round. If the file becomes unreadable, the game will start fresh without crashing.

## 🧪 Testing & Extensibility

While this project focuses on interactive play, the modular design (dataclasses, pure functions for board checks, Minimax encapsulation) makes it straightforward to:

- Extend gameplay mechanics
- Add automated tests around `GameStats`, `check_winner`, `is_board_full`, and System logic
- mReplace the CLI with a GUI or web front-end if desired

## 🙌 Contributing

Suggestions and improvements are welcome. Feel free to open issues or submit pull requests with enhancements, bug fixes, or documentation updates.

## 📄 License

This project is released under the MIT License. See LICENSE for details.

Enjoy mastering Tic-Tac-Toe against your intelligent digital opponent! 🎉
