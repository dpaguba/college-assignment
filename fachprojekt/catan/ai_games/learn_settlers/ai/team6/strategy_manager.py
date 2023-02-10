import json
import os
import random

class StrategyManager:

    """
    Handles AI Strategy selection and performance tracking
    """

    def __init__(self, stats_file="strategy_scores.json"):
        self.stats_file = stats_file

        # Initialize strategies with building_priorities, resource_values, dev_card_priorities
        self.strategies = [
            {
                "building_priorities": {"settlement": 5, "city": 4, "road": 2, "card": 1},
                "resource_values":      {0: 0.3, 1: 0.3, 2: 0.1, 3: 0.2, 4: 0.1},
                "dev_card_priorities": {
                    "KNIGHT": 8,
                    "ROAD_BUILDING": 7,
                    "YEAR_OF_PLENTY": 6,
                    "MONOPOLY": 5
                }
            },
            {
                "building_priorities": {"settlement": 2, "city": 3, "road": 1, "card": 4},
                "resource_values":      {0: 0.2, 1: 0.2, 2: 0.15, 3: 0.25, 4: 0.2},
                "dev_card_priorities": {
                    "KNIGHT": 6,
                    "ROAD_BUILDING": 5,
                    "YEAR_OF_PLENTY": 8,
                    "MONOPOLY": 7
                }
            },
            {
                "building_priorities": {"settlement": 4, "city": 4, "road": 1, "card": 1},
                "resource_values":      {0: 0.25, 1: 0.25, 2: 0.1, 3: 0.25, 4: 0.15},
                "dev_card_priorities": {
                    "KNIGHT": 7,
                    "ROAD_BUILDING": 6,
                    "YEAR_OF_PLENTY": 5,
                    "MONOPOLY": 6
                }
            }
            
        ]

        self.strategy_stats = self.load_stats()

    def load_stats(self):

        """Loads strategy statistics from starategy_scores.json"""
        if os.path.exists(self.stats_file):
            with open(self.stats_file, "r") as f:
                return json.load(f)
        else:
            return []

    def save_stats(self):

        """Saves the current strategy statistics to starategy_scores.json"""
        with open(self.stats_file, "w") as f:
            json.dump(self.strategy_stats, f, indent=2)

    def choose_strategy(self) -> dict:

        """Randomly selects one of the predefined strategies."""
        return random.choice(self.strategies)
    

    def update_result(self, strategy: dict, won: bool):

        """Updates the statistics of a given strategy based on the game result."""
        strategy_str = json.dumps(strategy, sort_keys=True)

        for entry in self.strategy_stats:
            if json.dumps(entry["strategy"], sort_keys=True) == strategy_str:
                entry["games"] += 1
                if won:
                    entry["wins"] += 1
                self.save_stats()
                return

        self.strategy_stats.append({
            "strategy": strategy,
            "games": 1,
            "wins": 1 if won else 0
        })
        self.save_stats()
