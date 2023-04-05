import cProfile
from ai_games.learn_settlers.game.learn_settlers import LearnSettlers
from ai_games.learn_settlers.game.player.random_player import RandomPlayer
from ai_games.learn_settlers.ai.team6.team6_player import Team6Player

def run_game(id: int):
    # Erstelle ein neues Spiel
    game = LearnSettlers(id, 5, logging_enabled=True)
    
    # Erstelle die Spieler
    team6_player = Team6Player("Team6AI")
    players = [
        team6_player,
        RandomPlayer("Random1"),
        RandomPlayer("Random2"),
        RandomPlayer("Random3")
    ]
    
    # Füge Spieler hinzu
    for p in players:
        game.add_player(p)
    
    # Führe das Spiel aus
    results = game.run()
    
    # Ermittle den Gewinner
    max_points = max(results)
    winners = [i for i, points in enumerate(results) if points == max_points]
    winner_names = [players[i].player_name for i in winners]
    
    # Gib Ergebnisse aus
    print(f"Spiel {id} beendet:")
    for i, player in enumerate(players):
        print(f"{player.player_name}: {results[i]} Punkte")
    
    print(f"Gewinner: {', '.join(winner_names)}")
    print("-" * 40)
    
    return (results[0], "Team6AI" in winner_names)

def main():
    num_games = 1000
    total_points = 0
    wins = 0
    
    for i in range(num_games):
        points, is_winner = run_game(i)
        total_points += points
        if is_winner:
            wins += 1
    
    win_rate = (wins / num_games) * 100
    
    print(f"\nErgebnisse nach {num_games} Spielen:")
    print(f"Durchschnittliche Punkte: {total_points/num_games:.2f}")
    print(f"Siege: {wins}/{num_games} ({win_rate:.2f}%)")

if __name__ == "__main__":
    main()