import numpy as np
from typing import List, Optional
import os

from ai_games.learn_settlers.game.objects.building import BuildingType
from ai_games.learn_settlers.game.player.player import Player, PlayerType
from ai_games.learn_settlers.com.message_type import MessageType
from ai_games.learn_settlers.game.objects.actions import Action
from ai_games.learn_settlers.game.objects.actions.phase_action import PhaseAction, GamePhase
from ai_games.learn_settlers.game.objects.game_state import GameState

from ai_games.learn_settlers.ai.team6.feature_extractor import CatanFeatureExtractor
from ai_games.learn_settlers.ai.team6.dqn_model import CatanDQNAgent
from ai_games.learn_settlers.ai.team6.team6_player import Team6Player

class Team6MLPlayer(Player):
    """
    ML-basierter Catan-Spieler mit DQN + Feature Engineering von Team6Player
    """
    
    def __init__(self, name: str = "Team6ML", model_path: Optional[str] = None, 
                 training_mode: bool = False):
        super().__init__(PlayerType.AI, name=name)
        
        # Training vs. Inference Mode
        self.training_mode = training_mode
        
        # Feature Extractor (nutzt Team6Player-Logik)
        self.feature_extractor = CatanFeatureExtractor()
        
        # DQN Agent
        self.dqn_agent = CatanDQNAgent(
            state_size=self.feature_extractor.TOTAL_FEATURES,
            action_feature_size=self.feature_extractor.ACTION_FEATURES,
            epsilon=0.1 if not training_mode else 1.0  # Wenig Exploration im Inference Mode
        )
        
        # Fallback zu Team6Player für komplexe Situationen
        self.fallback_player = Team6Player()
        
        # Load model if provided
        if model_path and os.path.exists(model_path):
            self.dqn_agent.load(model_path)
            print(f"Loaded model from {model_path}")
        
        # Training tracking
        self.last_state_features = None
        self.last_action_features = None
        self.last_action_index = None
        self.game_reward = 0.0
        self.turn_count = 0
    
    def handle_request(self, message_type: MessageType, possible_actions: List[Action]) -> Action:
        """
        Hauptfunktion: Wählt beste Action basierend auf DQN + Fallback-Logik
        """
        assert self.game_state is not None
        
        # Setup fallback player
        self.fallback_player.game_state = self.game_state
        self.fallback_player.player_no = self.player_no
        
        # Spezielle Behandlung für Setup-Phase und komplexe Situationen
        if self._should_use_fallback(possible_actions):
            action = self.fallback_player.handle_request(message_type, possible_actions)
            
            # Im Training-Mode trotzdem Erfahrung sammeln
            if self.training_mode:
                self._store_fallback_experience(possible_actions, action)
            
            return action
        
        # ML-basierte Entscheidung
        return self._choose_ml_action(possible_actions)
    
    def _should_use_fallback(self, possible_actions: List[Action]) -> bool:
        """
        Entscheidet, ob Team6Player-Fallback verwendet werden soll
        """
        # Setup-Phase: Nutze Team6Player
        if self.game_state.phase == GamePhase.SETUP:
            return True
        
        # Discard-Situationen: Team6Player
        from ai_games.learn_settlers.game.objects.actions import DiscardAction
        if len(possible_actions) > 0 and isinstance(possible_actions[0], DiscardAction):
            return True
        
        # Robber-Placement: Nutze Team6Player-Evaluationen
        from ai_games.learn_settlers.game.objects.game_state import RobberState
        if self.game_state.robber_state != RobberState.NO_STATE:
            return True
        
        # Spezielle Karten-Situationen
        if (self.game_state.monopoly or self.game_state.year_of_plenty > 0 or 
            self.game_state.road_building > 0):
            return True
        
        # Sehr frühe Züge (erste 5 Runden)
        if self.game_state.turn < 5:
            return True
        
        return False
    
    def _choose_ml_action(self, possible_actions: List[Action]) -> Action:
        """
        Wählt Action basierend auf DQN
        """
        # Extrahiere State Features
        state_features = self.feature_extractor.extract_state_features(
            self.game_state, self.player_no
        )
        
        # Extrahiere Action Features für alle möglichen Actions
        action_features_list = []
        for action in possible_actions:
            action_features = self.feature_extractor.extract_action_features(
                self.game_state, self.player_no, action
            )
            action_features_list.append(action_features)
        
        # DQN Entscheidung
        action_index = self.dqn_agent.act(
            state_features, action_features_list, training=self.training_mode
        )
        
        chosen_action = possible_actions[action_index]
        
        # Store für Training
        if self.training_mode:
            self.last_state_features = state_features
            self.last_action_features = action_features_list[action_index]
            self.last_action_index = action_index
        
        return chosen_action
    
    def _store_fallback_experience(self, possible_actions: List[Action], chosen_action: Action):
        """
        Speichert Erfahrung auch wenn Fallback-Player verwendet wurde
        """
        if not self.training_mode:
            return
            
        # Extrahiere Features
        state_features = self.feature_extractor.extract_state_features(
            self.game_state, self.player_no
        )
        
        action_features_list = []
        chosen_index = 0
        for i, action in enumerate(possible_actions):
            action_features = self.feature_extractor.extract_action_features(
                self.game_state, self.player_no, action
            )
            action_features_list.append(action_features)
            
            if action == chosen_action:
                chosen_index = i
        
        # Store für späteren Reward
        self.last_state_features = state_features
        self.last_action_features = action_features_list[chosen_index]
        self.last_action_index = chosen_index
    
    def update_game_state(self, message_type: MessageType, action: Action | GameState):
        """
        Update Game State + Training Logic
        """
        # Update fallback player
        self.fallback_player.update_game_state(message_type, action)
        
        # Standard update
        super().update_game_state(message_type, action)
        
        # Training Logic
        if self.training_mode and self.last_state_features is not None:
            self._update_training(message_type, action)
    
    def _update_training(self, message_type: MessageType, action: Action | GameState):
        """
        Updates für DQN Training
        """
        # Berechne Reward basierend auf Action-Outcomes
        reward = self._calculate_reward(message_type, action)
        self.game_reward += reward
        
        # Check if game ended
        done = False
        if isinstance(action, PhaseAction) and action.game_phase == GamePhase.ENDED:
            done = True
            # Game-End Reward basierend auf Platzierung
            final_reward = self._calculate_final_reward(action)
            reward += final_reward
        
        # Store experience in replay buffer
        if self.last_state_features is not None:
            # Nächster State (falls nicht Game-End)
            next_state_features = None
            next_action_features_list = None
            
            if not done and self.game_state is not None:
                try:
                    next_state_features = self.feature_extractor.extract_state_features(
                        self.game_state, self.player_no
                    )
                    # Für echte next_actions bräuchten wir die nächsten possible_actions
                    # Hier verwenden wir vereinfachte Dummy-Actions
                    next_action_features_list = [np.zeros(self.feature_extractor.ACTION_FEATURES)]
                except:
                    # Fallback wenn State-Extraktion fehlschlägt
                    pass
            
            # Store in replay buffer
            self.dqn_agent.remember(
                state_features=self.last_state_features,
                action_features=self.last_action_features,
                reward=reward,
                next_state_features=next_state_features,
                next_action_features_list=next_action_features_list,
                done=done
            )
            
            # Train network (wenn genug Erfahrungen vorhanden)
            if len(self.dqn_agent.memory) > self.dqn_agent.batch_size:
                loss = self.dqn_agent.replay()
                if loss is not None and self.turn_count % 10 == 0:
                    print(f"Turn {self.turn_count}, Loss: {loss:.4f}, Epsilon: {self.dqn_agent.epsilon:.4f}")
        
        self.turn_count += 1
    
    def _calculate_reward(self, message_type: MessageType, action: Action | GameState) -> float:
        """
        Berechnet Reward basierend auf Action-Outcomes
        """
        if not self.game_state:
            return 0.0
        
        my_player = self.game_state.players[self.player_no]
        reward = 0.0
        
        # Basis-Rewards für positive Entwicklungen
        from ai_games.learn_settlers.game.objects.actions import BuildCornerAction, BuildEdgeAction
        
        if isinstance(action, BuildCornerAction):
            # Settlement/City gebaut
            if action.building_type in [BuildingType.SETTLEMENT, BuildingType.HARBOR_SETTLEMENT]:
                reward += 2.0  # Settlement = +1 VP
            elif action.building_type in [BuildingType.CITY, BuildingType.HARBOR_CITY]:
                reward += 3.0  # City = +1 VP + bessere Ressourcen
        
        elif isinstance(action, BuildEdgeAction):
            # Road gebaut
            reward += 0.5
            # Bonus wenn longest road erreicht
            if my_player.longest_road:
                reward += 2.0
        
        # Victory Point Reward
        if hasattr(action, 'player_no') and action.player_no == self.player_no:
            current_vp = my_player.victory_points
            reward += current_vp * 0.1  # Kontinuierlicher VP-Bonus
        
        # Negative Rewards
        from ai_games.learn_settlers.game.objects.actions import RobberAction
        if isinstance(action, RobberAction) and action.target_player == self.player_no:
            reward -= 0.5  # Bestohlen worden
        
        # Resource efficiency reward
        total_resources = my_player.resources[-1]
        if total_resources > 7:
            reward -= 0.1 * (total_resources - 7)  # Penalty für zu viele Ressourcen
        
        return reward
    
    def _calculate_final_reward(self, phase_action: PhaseAction) -> float:
        """
        Berechnet finalen Reward basierend auf Spielergebnis
        """
        if not phase_action.vp_update:
            return 0.0
        
        final_scores = phase_action.vp_update
        my_score = final_scores[self.player_no]
        max_score = max(final_scores)
        
        # Win/Loss Reward
        if my_score == max_score:
            # Gewonnen!
            winners = [i for i, score in enumerate(final_scores) if score == max_score]
            if len(winners) == 1:
                return 10.0  # Klarer Sieg
            else:
                return 5.0   # Unentschieden
        else:
            # Verloren - aber Belohnung basierend auf Platzierung
            better_players = sum(1 for score in final_scores if score > my_score)
            placement_reward = 2.0 - (better_players * 0.5)  # 2nd place = 1.5, 3rd = 1.0, 4th = 0.5
            return max(placement_reward, -2.0)  # Mindestens -2.0
    
    def prepare_game(self, action: PhaseAction):
        """
        Bereitet neues Spiel vor
        """
        super().prepare_game(action)
        self.fallback_player.prepare_game(action)
        
        # Reset training variables
        self.last_state_features = None
        self.last_action_features = None
        self.last_action_index = None
        self.game_reward = 0.0
        self.turn_count = 0
    
    def save_model(self, filepath: str):
        """
        Speichert das trainierte Modell
        """
        self.dqn_agent.save(filepath)
    
    def set_training_mode(self, training: bool):
        """
        Schaltet zwischen Training- und Inference-Mode um
        """
        self.training_mode = training
        if not training:
            self.dqn_agent.epsilon = 0.01  # Minimale Exploration im Inference
    
    def get_training_stats(self) -> dict:
        """
        Gibt Training-Statistiken zurück
        """
        return {
            'epsilon': self.dqn_agent.epsilon,
            'training_steps': self.dqn_agent.training_step,
            'memory_size': len(self.dqn_agent.memory),
            'avg_loss': np.mean(self.dqn_agent.loss_history[-100:]) if self.dqn_agent.loss_history else 0.0,
            'game_reward': self.game_reward,
            'turn_count': self.turn_count
        }