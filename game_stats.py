from dataclasses import dataclass
from typing import Dict


@dataclass
class GameStats:
    """Tracks game results across sessions."""

    wins: int = 0
    losses: int = 0
    ties: int = 0

    def record_win(self) -> None:
        self.wins += 1

    def record_loss(self) -> None:
        self.losses += 1

    def record_tie(self) -> None:
        self.ties += 1

    def to_dict(self) -> Dict[str, int]:
        return {'wins': self.wins, 'losses': self.losses, 'ties': self.ties}

    @classmethod
    def from_dict(the_class, results: Dict[str, int]) -> 'GameStats':
        return the_class(
            wins=int(results.get('wins', 0)),
            losses=int(results.get('losses', 0)),
            ties=int(results.get('ties', 0)),
        )

    def legacy(self) -> str:
        return f'Wins: {self.wins} • Losses: {self.losses} • Ties: {self.ties}'
