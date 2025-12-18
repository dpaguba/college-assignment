import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List
import json
from datetime import datetime

from ai_games.learn_settlers.game.learn_settlers import LearnSettlers
from ai_games.learn_settlers.game.player.random_player import RandomPlayer
from ai_games.learn_settlers.ai.team6.team6_player import Team6Player
from ai_games.learn_settlers.ai.team6.team6_ml_player import Team6MLPlayer

class CatanEvaluator:
    """
    Umfassende Evaluation der Catan ML-Player
    """
    
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.results = {}
        
        # Initialize ML player
        if os.path.exists(model_path):
            self.ml_player = Team6MLPlayer(name="Team6ML", model_path=model_path, training_mode=False)
            print(f"Loaded model from {model_path}")
        else:
            print(f"Model not found at {model_path}")
            raise FileNotFoundError(f"Model not found: {model_path}")
    
    def run_comprehensive_evaluation(self, games_per_config: int = 100) -> Dict:
        """
        Führt umfassende Evaluation gegen verschiedene Gegner-Konfigurationen durch
        """
        print(f"Starting comprehensive evaluation with {games_per_config} games per configuration")
        
        # Verschiedene Gegner-Konfigurationen
        configurations = {
            "vs_3_random": {
                "description": "Against 3 Random Players",
                "opponents": [RandomPlayer(f"Random{i}") for i in range(3)]
            },
            "vs_3_team6": {
                "description": "Against 3 Team6 Players", 
                "opponents": [Team6Player(f"Team6-{i}") for i in range(3)]
            },
            "vs_mixed_easy": {
                "description": "Against 2 Random + 1 Team6",
                "opponents": [RandomPlayer("Random1"), RandomPlayer("Random2"), Team6Player("Team6")]
            },
            "vs_mixed_hard": {
                "description": "Against 1 Random + 2 Team6",
                "opponents": [RandomPlayer("Random"), Team6Player("Team6-1"), Team6Player("Team6-2")]
            },
            "vs_1v1_team6": {
                "description": "1v1 against Team6 (with 2 randoms)",
                "opponents": [Team6Player("Team6-Rival"), RandomPlayer("Random1"), RandomPlayer("Random2")]
            }
        }
        
        evaluation_results = {}
        
        for config_name, config in configurations.items():
            print(f"\n Evaluating: {config['description']}")
            
            results = self._evaluate_configuration(
                config_name, 
                config['opponents'], 
                games_per_config
            )
            
            evaluation_results[config_name] = results
            
            # Print intermediate results
            win_rate = results['wins'] / results['games'] * 100
            avg_score = np.mean(results['scores'])
            print(f"   Win Rate: {win_rate:.1f}% ({results['wins']}/{results['games']})")
            print(f"   Avg Score: {avg_score:.1f}")
        
        # Generate summary report
        self._generate_evaluation_report(evaluation_results)
        
        return evaluation_results
    
    def _evaluate_configuration(self, config_name: str, opponents: List, games: int) -> Dict:
        """
        Evaluiert eine spezifische Gegner-Konfiguration
        """
        results = {
            'games': 0,
            'wins': 0, 
            'scores': [],
            'positions': [],  # 1st, 2nd, 3rd, 4th place
            'game_details': []
        }
        
        for game_idx in range(games):
            # Progress indicator
            if (game_idx + 1) % 20 == 0:
                current_wr = results['wins'] / results['games'] * 100 if results['games'] > 0 else 0
                print(f"   Progress: {game_idx + 1}/{games} games ({current_wr:.1f}% win rate)")
            
            game_result = self._run_single_evaluation_game(game_idx, opponents.copy())
            
            if game_result:
                results['games'] += 1
                results['scores'].append(game_result['ml_score'])
                results['positions'].append(game_result['position'])
                results['game_details'].append(game_result)
                
                if game_result['won']:
                    results['wins'] += 1
        
        return results
    
    def _run_single_evaluation_game(self, game_id: int, opponents: List) -> Dict:
        """
        Führt ein einzelnes Evaluations-Spiel aus
        """
        try:
            game = LearnSettlers(game_id, 5, logging_enabled=False)
            
            # Create fresh instances of opponents
            fresh_opponents = []
            for opp in opponents:
                if isinstance(opp, RandomPlayer):
                    fresh_opponents.append(RandomPlayer(opp.player_name))
                elif isinstance(opp, Team6Player):
                    fresh_opponents.append(Team6Player(opp.player_name))
            
            # Create fresh ML player for each game to avoid state issues
            ml_player = Team6MLPlayer(
                name="Team6ML-Eval", 
                model_path=self.model_path, 
                training_mode=False
            )
            
            all_players = [ml_player] + fresh_opponents
            np.random.shuffle(all_players)
            
            # Find ML player index after shuffle
            ml_player_index = None
            for i, player in enumerate(all_players):
                if isinstance(player, Team6MLPlayer):
                    ml_player_index = i
                    break
            
            # Add players to game
            for player in all_players:
                game.add_player(player)
            
            # Run game
            scores = game.run()
            
            # Analyze results
            ml_score = scores[ml_player_index]
            sorted_scores = sorted(scores, reverse=True)
            position = sorted_scores.index(ml_score) + 1  # 1st, 2nd, 3rd, 4th
            max_score = max(scores)
            won = ml_score == max_score
            
            return {
                'ml_score': ml_score,
                'all_scores': scores,
                'position': position,
                'won': won,
                'max_score': max_score,
                'ml_player_index': ml_player_index
            }
            
        except Exception as e:
            print(f"Error in evaluation game {game_id}: {e}")
            return None
    
    def _generate_evaluation_report(self, results: Dict):
        """
        Generiert einen umfassenden Evaluations-Report
        """
        print("\n" + "="*80)
        print(" COMPREHENSIVE EVALUATION REPORT")
        print("="*80)
        
        # Overall statistics
        total_games = sum(r['games'] for r in results.values())
        total_wins = sum(r['wins'] for r in results.values())
        overall_win_rate = total_wins / total_games * 100 if total_games > 0 else 0
        
        all_scores = [score for r in results.values() for score in r['scores']]
        overall_avg_score = np.mean(all_scores) if all_scores else 0
        
        print(f"OVERALL PERFORMANCE:")
        print(f"   Total Games: {total_games}")
        print(f"   Total Wins: {total_wins}")
        print(f"   Overall Win Rate: {overall_win_rate:.1f}%")
        print(f"   Average Score: {overall_avg_score:.1f}")
        print()
        
        # Detailed breakdown by configuration
        print("DETAILED BREAKDOWN:")
        print("-" * 80)
        
        for config_name, result in results.items():
            if result['games'] == 0:
                continue
                
            win_rate = result['wins'] / result['games'] * 100
            avg_score = np.mean(result['scores'])
            std_score = np.std(result['scores'])
            
            # Position analysis
            positions = result['positions']
            pos_1st = positions.count(1)
            pos_2nd = positions.count(2) 
            pos_3rd = positions.count(3)
            pos_4th = positions.count(4)
            
            print(f"{config_name.upper()}")
            print(f"   Win Rate: {win_rate:.1f}% ({result['wins']}/{result['games']})")
            print(f"   Avg Score: {avg_score:.1f} ± {std_score:.1f}")
            print(f"   Positions: 1st: {pos_1st}, 2nd: {pos_2nd}, 3rd: {pos_3rd}, 4th: {pos_4th}")
            print(f"   Score Range: {min(result['scores']):.0f} - {max(result['scores']):.0f}")
            print()
        
        # Performance comparison with baselines
        self._compare_with_baselines(results)
        
        # Save detailed results
        self._save_evaluation_results(results)
        
        # Generate plots
        self._plot_evaluation_results(results)
    
    def _compare_with_baselines(self, results: Dict):
        """
        Vergleicht Performance mit bekannten Baselines
        """
        print("🏆 BASELINE COMPARISON:")
        print("-" * 40)
        
        # Bekannte Baseline-Performances (aus früheren Tests)
        baselines = {
            "Random Player": {"vs_3_random": 25.0, "vs_3_team6": 10.0, "vs_mixed_easy": 20.0},
            "Team6 Player": {"vs_3_random": 45.0, "vs_3_team6": 25.0, "vs_mixed_easy": 35.0}
        }
        
        for config_name, result in results.items():
            if result['games'] == 0:
                continue
                
            ml_win_rate = result['wins'] / result['games'] * 100
            print(f"{config_name}:")
            print(f"   Team6ML:     {ml_win_rate:.1f}%")
            
            for baseline_name, baseline_rates in baselines.items():
                if config_name in baseline_rates:
                    baseline_rate = baseline_rates[config_name]
                    improvement = ml_win_rate - baseline_rate
                    print(f"   {baseline_name}: {baseline_rate:.1f}% (Δ {improvement:+.1f}%)")
            print()
    
    def _save_evaluation_results(self, results: Dict):
        """
        Speichert detaillierte Evaluations-Ergebnisse
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # JSON format für maschinelle Verarbeitung
        results_file = f"evaluation_results_{timestamp}.json"
        
        # Convert numpy types to native Python types for JSON serialization
        json_results = {}
        for config_name, result in results.items():
            json_results[config_name] = {
                'games': result['games'],
                'wins': result['wins'],
                'scores': [float(s) for s in result['scores']],
                'positions': result['positions'],
                'win_rate': result['wins'] / result['games'] * 100 if result['games'] > 0 else 0,
                'avg_score': float(np.mean(result['scores'])) if result['scores'] else 0,
                'std_score': float(np.std(result['scores'])) if result['scores'] else 0
            }
        
        with open(results_file, 'w') as f:
            json.dump(json_results, f, indent=2)
        
        print(f" Detailed results saved to: {results_file}")
        
        # CSV format für Excel/Analytics
        csv_data = []
        for config_name, result in results.items():
            for i, score in enumerate(result['scores']):
                csv_data.append({
                    'configuration': config_name,
                    'game_id': i,
                    'score': score,
                    'position': result['positions'][i],
                    'won': result['positions'][i] == 1
                })
        
        if csv_data:
            df = pd.DataFrame(csv_data)
            csv_file = f"evaluation_games_{timestamp}.csv"
            df.to_csv(csv_file, index=False)
            print(f" Game-by-game data saved to: {csv_file}")
    
    def _plot_evaluation_results(self, results: Dict):
        """
        Erstellt Visualisierungen der Evaluations-Ergebnisse
        """
        if not results:
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Team6ML Player Evaluation Results', fontsize=16, fontweight='bold')
        
        # 1. Win rates by configuration
        configs = list(results.keys())
        win_rates = [results[config]['wins'] / results[config]['games'] * 100 
                    if results[config]['games'] > 0 else 0 for config in configs]
        
        bars1 = axes[0, 0].bar(range(len(configs)), win_rates, 
                              color=['#2E8B57', '#4169E1', '#FF6347', '#FFD700', '#9370DB'])
        axes[0, 0].set_title('Win Rates by Configuration', fontweight='bold')
        axes[0, 0].set_ylabel('Win Rate (%)')
        axes[0, 0].set_xticks(range(len(configs)))
        axes[0, 0].set_xticklabels([c.replace('_', '\n') for c in configs], rotation=45)
        axes[0, 0].grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, rate in zip(bars1, win_rates):
            axes[0, 0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                           f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        # 2. Score distributions
        all_scores = [results[config]['scores'] for config in configs if results[config]['scores']]
        if all_scores:
            axes[0, 1].boxplot(all_scores, labels=[c.replace('_', '\n') for c in configs])
            axes[0, 1].set_title('Score Distributions', fontweight='bold')
            axes[0, 1].set_ylabel('Victory Points')
            axes[0, 1].grid(True, alpha=0.3)
            plt.setp(axes[0, 1].get_xticklabels(), rotation=45)
        
        # 3. Position frequencies
        position_data = {1: [], 2: [], 3: [], 4: []}
        for config in configs:
            positions = results[config]['positions']
            total = len(positions)
            for pos in [1, 2, 3, 4]:
                count = positions.count(pos) if positions else 0
                percentage = count / total * 100 if total > 0 else 0
                position_data[pos].append(percentage)
        
        x = range(len(configs))
        width = 0.2
        colors = ['#FFD700', '#C0C0C0', '#CD7F32', '#696969']  # Gold, Silver, Bronze, Gray
        
        for i, (pos, percentages) in enumerate(position_data.items()):
            offset = (i - 1.5) * width
            axes[1, 0].bar([xi + offset for xi in x], percentages, width, 
                          label=f'{pos}{"st" if pos==1 else "nd" if pos==2 else "rd" if pos==3 else "th"} place',
                          color=colors[i-1])
        
        axes[1, 0].set_title('Finish Position Distribution', fontweight='bold')
        axes[1, 0].set_ylabel('Percentage (%)')
        axes[1, 0].set_xticks(x)
        axes[1, 0].set_xticklabels([c.replace('_', '\n') for c in configs], rotation=45)
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Performance vs difficulty
        difficulty_order = ['vs_3_random', 'vs_mixed_easy', 'vs_mixed_hard', 'vs_3_team6', 'vs_1v1_team6']
        difficulty_win_rates = []
        difficulty_labels = []
        
        for config in difficulty_order:
            if config in results and results[config]['games'] > 0:
                win_rate = results[config]['wins'] / results[config]['games'] * 100
                difficulty_win_rates.append(win_rate)
                difficulty_labels.append(config.replace('vs_', '').replace('_', '\n'))
        
        if difficulty_win_rates:
            line = axes[1, 1].plot(range(len(difficulty_win_rates)), difficulty_win_rates, 
                                  'o-', linewidth=3, markersize=8, color='#2E8B57')
            axes[1, 1].set_title('Performance vs Difficulty', fontweight='bold')
            axes[1, 1].set_ylabel('Win Rate (%)')
            axes[1, 1].set_xlabel('Difficulty Level')
            axes[1, 1].set_xticks(range(len(difficulty_labels)))
            axes[1, 1].set_xticklabels(difficulty_labels)
            axes[1, 1].grid(True, alpha=0.3)
            
            # Add value labels
            for i, rate in enumerate(difficulty_win_rates):
                axes[1, 1].text(i, rate + 2, f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plot_file = f"evaluation_plots_{timestamp}.png"
        plt.savefig(plot_file, dpi=300, bbox_inches='tight')
        print(f"Evaluation plots saved to: {plot_file}")
        
        plt.show()
    
    def run_head_to_head_comparison(self, opponent_type: str = "team6", games: int = 50):
        """
        Direkter 1-gegen-1 Vergleich (mit 2 Random-Fillern)
        """
        print(f"\n  HEAD-TO-HEAD: Team6ML vs {opponent_type.upper()}")
        print("=" * 50)
        
        if opponent_type.lower() == "team6":
            opponent = Team6Player("Team6-Rival")
        else:
            opponent = RandomPlayer("Random-Rival")
        
        wins_ml = 0
        wins_opponent = 0
        scores_ml = []
        scores_opponent = []
        
        for game_idx in range(games):
            game = LearnSettlers(game_idx, 5, logging_enabled=False)
            
            # Create fresh players
            ml_player = Team6MLPlayer(name="Team6ML", model_path=self.model_path, training_mode=False)
            fresh_opponent = Team6Player("Team6-Rival") if opponent_type.lower() == "team6" else RandomPlayer("Random-Rival")
            
            # Add random fillers
            filler1 = RandomPlayer("Filler1")
            filler2 = RandomPlayer("Filler2")
            
            all_players = [ml_player, fresh_opponent, filler1, filler2]
            np.random.shuffle(all_players)
            
            # Track positions of main competitors
            ml_idx = None
            opp_idx = None
            for i, player in enumerate(all_players):
                if isinstance(player, Team6MLPlayer):
                    ml_idx = i
                elif (isinstance(player, Team6Player) and opponent_type.lower() == "team6") or \
                     (isinstance(player, RandomPlayer) and opponent_type.lower() == "random" and player.player_name == "Random-Rival"):
                    opp_idx = i
            
            for player in all_players:
                game.add_player(player)
            
            try:
                scores = game.run()
                
                ml_score = scores[ml_idx]
                opp_score = scores[opp_idx]
                
                scores_ml.append(ml_score)
                scores_opponent.append(opp_score)
                
                if ml_score > opp_score:
                    wins_ml += 1
                elif opp_score > ml_score:
                    wins_opponent += 1
                # Tie = no winner
                
                if (game_idx + 1) % 10 == 0:
                    current_ml_wr = wins_ml / (game_idx + 1) * 100
                    print(f"   Progress: {game_idx + 1}/{games} ({current_ml_wr:.1f}% Team6ML wins)")
                    
            except Exception as e:
                print(f"Error in head-to-head game {game_idx}: {e}")
        
        # Results
        total_decided = wins_ml + wins_opponent
        ml_win_rate = wins_ml / total_decided * 100 if total_decided > 0 else 0
        
        print(f"\n HEAD-TO-HEAD RESULTS:")
        print(f"   Team6ML wins: {wins_ml}")
        print(f"   {opponent_type.upper()} wins: {wins_opponent}")
        print(f"   Ties: {games - total_decided}")
        print(f"   Team6ML win rate: {ml_win_rate:.1f}%")
        print(f"   Avg scores - Team6ML: {np.mean(scores_ml):.1f}, {opponent_type.upper()}: {np.mean(scores_opponent):.1f}")

def main():
    """
    Hauptfunktion für die Evaluation
    """
    print("Catan ML Player Evaluation")
    print("=" * 50)
    
    # Model path
    model_path = "models/best_model.pth"  # oder "models/final_model.pth"
    
    if not os.path.exists(model_path):
        print(f"Model not found at {model_path}")
        print("Available models:")
        if os.path.exists("models"):
            for f in os.listdir("models"):
                if f.endswith(".pth"):
                    print(f"   - models/{f}")
        return
    
    # Initialize evaluator
    evaluator = CatanEvaluator(model_path)
    
    # Run comprehensive evaluation
    results = evaluator.run_comprehensive_evaluation(games_per_config=100)
    
    # Run head-to-head comparison
    evaluator.run_head_to_head_comparison("team6", games=50)
    
    print("\nEvaluation completed!")

if __name__ == "__main__":
    main()