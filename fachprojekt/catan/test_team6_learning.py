from ai_games.learn_settlers.ai.team6.team6_learning_player import Team6LearningPlayer
from ai_games.learn_settlers.game.learn_settlers import LearnSettlers
from ai_games.learn_settlers.game.player.random_player import RandomPlayer
from ai_games.learn_settlers.ai.team6.strategy_manager import StrategyManager


def run_game(id: int):

    # Create strategy manager and select a random strategy
    strategy_manager = StrategyManager()
    current_strategy = strategy_manager.choose_strategy()

    # Create the AI player with the selected strategy
    team6_player = Team6LearningPlayer(current_strategy, name="Team6AI")

    # Save strategy references for later stat update
    team6_player.current_strategy = current_strategy
    team6_player.strategy_manager = strategy_manager

    # Create game
    game = LearnSettlers(id, 5, logging_enabled=True)

    players = [
        team6_player,
        RandomPlayer("Random1"),
        RandomPlayer("Random2"),
        RandomPlayer("Random3")
    ]

    for p in players:
        game.add_player(p)

    results = game.run()

    max_points = max(results)
    winners = [i for i, points in enumerate(results) if points == max_points]
    winner_names = [players[i].player_name for i in winners]

    # Update strategy stats
    won = "Team6AI" in winner_names
    team6_player.strategy_manager.update_result(team6_player.current_strategy, won=won)

    # Print results
    print(f"Spiel {id} beendet:")
    for i, player in enumerate(players):
        print(f"{player.player_name}: {results[i]} Punkte")

    print(f"Gewinner: {', '.join(winner_names)}")
    print("-" * 40)

    return (results[0], won)


def main():
    num_games = 100
    total_points = 0
    wins = 0

    for i in range(num_games):
        points, is_winner = run_game(i)
        total_points += points
        if is_winner:
            wins += 1

    win_rate = (wins / num_games) * 100

    print(f"\nErgebnisse nach {num_games} Spielen:")
    print(f"Durchschnittliche Punkte: {total_points / num_games:.2f}")
    print(f"Siege: {wins}/{num_games} ({win_rate:.2f}%)")


if __name__ == "__main__":
    main()
