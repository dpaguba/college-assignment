import os
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict
import json
from datetime import datetime

from ai_games.learn_settlers.game.learn_settlers import LearnSettlers
from ai_games.learn_settlers.game.player.random_player import RandomPlayer
from ai_games.learn_settlers.ai.team6.team6_player import Team6Player
from ai_games.learn_settlers.ai.team6.team6_ml_player import Team6MLPlayer

class CatanTrainingPipeline:
    """
    Training Pipeline für Team6 ML Player
    """
    
    def __init__(self, model_save_dir: str = "models", log_dir: str = "training_logs"):
        self.model_save_dir = model_save_dir
        self.log_dir = log_dir
        
        # Create directories
        os.makedirs(model_save_dir, exist_ok=True)
        os.makedirs(log_dir, exist_ok=True)
        
        # Training statistics
        self.training_stats = {
            'episodes': [],
            'wins': [],
            'avg_scores': [],
            'losses': [],
            'epsilons': [],
            'win_rates': []
        }
    
    def train(self, episodes: int = 1000, save_interval: int = 100, 
              eval_interval: int = 50, eval_games: int = 20):
        """
        Haupttraining-Loop
        
        Args:
            episodes: Anzahl Training-Episoden
            save_interval: Modell-Speicher-Intervall
            eval_interval: Evaluations-Intervall
            eval_games: Anzahl Evaluations-Spiele
        """
        print(f"🚀 Starting Catan DQN Training for {episodes} episodes")
        print(f"📁 Models will be saved to: {self.model_save_dir}")
        
        # Initialize ML player
        ml_player = Team6MLPlayer(name="Team6ML-Training", training_mode=True)
        
        # Training loop
        for episode in range(episodes):
            # Run single training game
            results = self._run_training_game(ml_player, episode)
            
            # Log results
            self._log_training_results(episode, results, ml_player)
            
            # Save model periodically
            if (episode + 1) % save_interval == 0:
                model_path = os.path.join(self.model_save_dir, f"catan_dqn_episode_{episode + 1}.pth")
                ml_player.save_model(model_path)
                print(f"💾 Model saved at episode {episode + 1}")
            
            # Evaluate periodically
            if (episode + 1) % eval_interval == 0:
                eval_results = self._evaluate_model(ml_player, eval_games)
                self._log_evaluation_results(episode, eval_results)
                
                # Save best model
                if eval_results['win_rate'] > max(self.training_stats['win_rates'], default=0):
                    best_model_path = os.path.join(self.model_save_dir, "best_model.pth")
                    ml_player.save_model(best_model_path)
                    print(f"🏆 New best model! Win rate: {eval_results['win_rate']:.2%}")
            
            # Print progress
            if (episode + 1) % 25 == 0:
                recent_wins = sum(self.training_stats['wins'][-25:])
                print(f"Episode {episode + 1}/{episodes} - Recent wins: {recent_wins}/25 ({recent_wins/25:.2%})")
        
        # Final save and evaluation
        final_model_path = os.path.join(self.model_save_dir, "final_model.pth")
        ml_player.save_model(final_model_path)
        
        final_eval = self._evaluate_model(ml_player, eval_games * 2)
        print(f"Final evaluation: {final_eval['win_rate']:.2%} win rate")
        
        # Save training statistics
        self._save_training_stats()
        self._plot_training_progress()
        
        print("Training completed!")
        
        return ml_player
    
    def _run_training_game(self, ml_player: Team6MLPlayer, episode: int) -> Dict:
        """
        Führt ein einzelnes Training-Spiel aus
        """
        game = LearnSettlers(episode, 5, logging_enabled=False)
        
        # Create opponents (mix of Random and Team6 players)
        opponents = [
            RandomPlayer("Random1"),
            RandomPlayer("Random2"), 
            Team6Player("Team6-Baseline")
        ]
        
        # Randomize player order
        all_players = [ml_player] + opponents
        np.random.shuffle(all_players)
        
        # Add players to game
        for player in all_players:
            game.add_player(player)
        
        # Run game
        try:
            scores = game.run()
            
            # Find ML player's results
            ml_player_index = None
            for i, player in enumerate(all_players):
                if isinstance(player, Team6MLPlayer):
                    ml_player_index = i
                    break
            
            ml_score = scores[ml_player_index]
            max_score = max(scores)
            won = ml_score == max_score
            
            return {
                'score': ml_score,
                'won': won,
                'max_score': max_score,
                'all_scores': scores
            }
            
        except Exception as e:
            print(f"Error in training game {episode}: {e}")
            return {
                'score': 0,
                'won': False,
                'max_score': 10,
                'all_scores': [0, 0, 0, 0]
            }
    
    def _evaluate_model(self, ml_player: Team6MLPlayer, eval_games: int) -> Dict:
        """
        Evaluiert das aktuelle Modell gegen verschiedene Gegner
        """
        print(f"📊 Evaluating model over {eval_games} games...")
        
        # Temporarily switch to inference mode
        ml_player.set_training_mode(False)
        
        results = {
            'vs_random': {'wins': 0, 'games': 0, 'scores': []},
            'vs_team6': {'wins': 0, 'games': 0, 'scores': []},
            'vs_mixed': {'wins': 0, 'games': 0, 'scores': []}
        }
        
        # Evaluate against different opponent configurations
        eval_configs = [
            ('vs_random', [RandomPlayer(f"Random{i}") for i in range(3)]),
            ('vs_team6', [Team6Player(f"Team6-{i}") for i in range(3)]),
            ('vs_mixed', [RandomPlayer("Random"), Team6Player("Team6"), RandomPlayer("Random2")])
        ]
        
        games_per_config = eval_games // len(eval_configs)
        
        for config_name, opponents in eval_configs:
            for game_idx in range(games_per_config):
                game = LearnSettlers(game_idx, 5, logging_enabled=False)
                
                # Create fresh opponents for each game
                fresh_opponents = []
                for opp in opponents:
                    if isinstance(opp, RandomPlayer):
                        fresh_opponents.append(RandomPlayer(opp.player_name))
                    else:
                        fresh_opponents.append(Team6Player(opp.player_name))
                
                all_players = [ml_player] + fresh_opponents
                np.random.shuffle(all_players)
                
                for player in all_players:
                    game.add_player(player)
                
                try:
                    scores = game.run()
                    
                    # Find ML player results
                    ml_player_index = None
                    for i, player in enumerate(all_players):
                        if isinstance(player, Team6MLPlayer):
                            ml_player_index = i
                            break
                    
                    ml_score = scores[ml_player_index]
                    max_score = max(scores)
                    won = ml_score == max_score
                    
                    results[config_name]['games'] += 1
                    results[config_name]['scores'].append(ml_score)
                    if won:
                        results[config_name]['wins'] += 1
                        
                except Exception as e:
                    print(f"Error in evaluation game: {e}")
        
        # Calculate overall statistics
        total_wins = sum(r['wins'] for r in results.values())
        total_games = sum(r['games'] for r in results.values())
        win_rate = total_wins / total_games if total_games > 0 else 0.0
        
        avg_score = np.mean([score for r in results.values() for score in r['scores']])
        
        # Switch back to training mode
        ml_player.set_training_mode(True)
        
        print(f"Evaluation results: {win_rate:.2%} win rate, {avg_score:.1f} avg score")
        
        return {
            'win_rate': win_rate,
            'avg_score': avg_score,
            'detailed_results': results
        }
    
    def _log_training_results(self, episode: int, results: Dict, ml_player: Team6MLPlayer):
        """
        Loggt Training-Ergebnisse
        """
        stats = ml_player.get_training_stats()
        
        self.training_stats['episodes'].append(episode)
        self.training_stats['wins'].append(1 if results['won'] else 0)
        self.training_stats['avg_scores'].append(results['score'])
        self.training_stats['losses'].append(stats['avg_loss'])
        self.training_stats['epsilons'].append(stats['epsilon'])
    
    def _log_evaluation_results(self, episode: int, eval_results: Dict):
        """
        Loggt Evaluations-Ergebnisse
        """
        self.training_stats['win_rates'].append(eval_results['win_rate'])
    
    def _save_training_stats(self):
        """
        Speichert Training-Statistiken
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        stats_file = os.path.join(self.log_dir, f"training_stats_{timestamp}.json")
        
        with open(stats_file, 'w') as f:
            json.dump(self.training_stats, f, indent=2)
        
        print(f"📊 Training statistics saved to {stats_file}")
    
    def _plot_training_progress(self):
        """
        Erstellt Plots der Training-Progress
        """
        if not self.training_stats['episodes']:
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Catan DQN Training Progress', fontsize=16)
        
        # Win rate over time (moving average)
        episodes = self.training_stats['episodes']
        wins = self.training_stats['wins']
        
        # Calculate moving average win rate
        window_size = 50
        if len(wins) >= window_size:
            moving_avg_wins = []
            for i in range(window_size - 1, len(wins)):
                avg = np.mean(wins[i - window_size + 1:i + 1])
                moving_avg_wins.append(avg)
            
            axes[0, 0].plot(episodes[window_size - 1:], moving_avg_wins)
            axes[0, 0].set_title(f'Win Rate (Moving Average, window={window_size})')
            axes[0, 0].set_xlabel('Episode')
            axes[0, 0].set_ylabel('Win Rate')
            axes[0, 0].grid(True)
        
        # Average scores
        axes[0, 1].plot(episodes, self.training_stats['avg_scores'])
        axes[0, 1].set_title('Average Score per Game')
        axes[0, 1].set_xlabel('Episode')
        axes[0, 1].set_ylabel('Score')
        axes[0, 1].grid(True)
        
        # Training loss
        if self.training_stats['losses']:
            axes[1, 0].plot(episodes, self.training_stats['losses'])
            axes[1, 0].set_title('Training Loss')
            axes[1, 0].set_xlabel('Episode')
            axes[1, 0].set_ylabel('Loss')
            axes[1, 0].grid(True)
        
        # Epsilon decay
        axes[1, 1].plot(episodes, self.training_stats['epsilons'])
        axes[1, 1].set_title('Epsilon (Exploration Rate)')
        axes[1, 1].set_xlabel('Episode')
        axes[1, 1].set_ylabel('Epsilon')
        axes[1, 1].grid(True)
        
        plt.tight_layout()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plot_file = os.path.join(self.log_dir, f"training_progress_{timestamp}.png")
        plt.savefig(plot_file, dpi=300, bbox_inches='tight')
        print(f"Training plots saved to {plot_file}")
        
        plt.show()

def main():
    """
    Startet das Training
    """
    print("Catan Deep Q-Learning Training")
    print("=" * 50)
    
    # Initialize training pipeline
    trainer = CatanTrainingPipeline()
    
    # Start training
    trained_model = trainer.train(
        episodes=3000,       # Anzahl Training-Episoden
        save_interval=50,   # Speichere Modell alle 50 Episoden
        eval_interval=25,   # Evaluiere alle 25 Episoden
        eval_games=20       # 20 Spiele pro Evaluation
    )
    
    print("🏁 Training finished!")
    return trained_model

if __name__ == "__main__":
    main()