
import numpy as np
from typing import List, Dict, Tuple
from ai_games.learn_settlers.game.objects.actions import *
from ai_games.learn_settlers.game.objects.terrain import Terrain
from ai_games.learn_settlers.com.message_type import MessageType
from ai_games.learn_settlers.game.objects.building import BuildingType
from ai_games.learn_settlers.game.player.player import Player, PlayerType
from ai_games.learn_settlers.game.logic.discard_helper import DiscardHelper
from ai_games.learn_settlers.game.objects.actions.phase_action import GamePhase
from ai_games.learn_settlers.game.objects.board_objects import Corner, Edge, Tile
from ai_games.learn_settlers.game.objects.game_state import GameState, RobberState
from ai_games.learn_settlers.game.objects.actions.card_action import DevelopmentCard
from ai_games.learn_settlers.ai.team6.team6_player import Team6Player

class CatanFeatureExtractor:
    """
    Robuste Feature-Extraktion mit festen, getesteten Dimensionen
    """
    
    def __init__(self):
        self.evaluator = Team6Player()
        
        # Feste Dimensionen - diese werden exakt eingehalten
        self.PLAYER_BASIC_FEATURES = 20    # Eigene Basis-Features
        self.OPPONENT_FEATURES = 28        # 4 Gegner * 7 Features
        self.GAME_STATE_FEATURES = 8       # Allgemeine Spiel-Features
        self.ACTION_FEATURES = 6           # Action-spezifische Features
        
        self.TOTAL_FEATURES = (self.PLAYER_BASIC_FEATURES + self.OPPONENT_FEATURES + 
                              self.GAME_STATE_FEATURES)  # = 56
        
        # Dice probabilities für Evaluationen
        self.dice_probabilities = {
            2: 1/36, 3: 2/36, 4: 3/36, 5: 4/36, 6: 5/36,
            8: 5/36, 9: 4/36, 10: 3/36, 11: 2/36, 12: 1/36
        }
    
    def extract_state_features(self, game_state: GameState, player_no: int) -> np.ndarray:
        """
        Extrahiert exakt 56 State-Features
        """
        features = []
        my_player = game_state.players[player_no]
        
        # PLAYER BASIC FEATURES (20)
        features.extend(self._extract_player_features(my_player))
        
        # OPPONENT FEATURES (28)
        features.extend(self._extract_opponent_features(game_state, player_no))
        
        # GAME STATE FEATURES (8)
        features.extend(self._extract_game_features(game_state, player_no))
        
        # Sicherheitscheck
        if len(features) != self.TOTAL_FEATURES:
            # Padding oder Trimming falls nötig
            if len(features) < self.TOTAL_FEATURES:
                features.extend([0.0] * (self.TOTAL_FEATURES - len(features)))
            else:
                features = features[:self.TOTAL_FEATURES]
        
        return np.array(features, dtype=np.float32)
    
    def _extract_player_features(self, player) -> List[float]:
        """Extrahiert exakt 20 Player-Features"""
        features = []
        
        # Ressourcen (6)
        features.extend(player.resources.astype(float))
        
        # Entwicklungskarten (6)
        features.extend(player.development_cards.astype(float))
        
        # Basis-Statistiken (8)
        features.extend([
            float(player.victory_points),
            float(len(player.buildings)),
            float(len(player.roads)),
            float(player.knights),
            float(player.longest_road),
            float(player.largest_army),
            float(player.resources[-1]),  # Total resources
            float(min(10, player.victory_points))  # Normalized VP (max 10)
        ])
        
        return features[:20]  # Garantiert 20 Features
    
    def _extract_opponent_features(self, game_state: GameState, my_player_no: int) -> List[float]:
        """Extrahiert exakt 28 Opponent-Features (4 Slots * 7 Features)"""
        features = []
        opponents = [p for i, p in enumerate(game_state.players) if i != my_player_no]
        
        # Sortiere Gegner nach Victory Points (stärkste zuerst)
        opponents.sort(key=lambda p: p.victory_points, reverse=True)
        
        # Extrahiere Features für bis zu 4 Gegner
        for i in range(4):  # Maximal 4 Gegner-Slots
            if i < len(opponents):
                opp = opponents[i]
                features.extend([
                    float(opp.victory_points),
                    float(opp.resources[-1]),  # Total resources
                    float(len(opp.buildings)),
                    float(len(opp.roads)),
                    float(opp.knights),
                    float(opp.longest_road),
                    float(opp.largest_army)
                ])
            else:
                # Padding für nicht vorhandene Gegner
                features.extend([0.0] * 7)
        
        return features[:28]  # Garantiert 28 Features
    
    def _extract_game_features(self, game_state: GameState, player_no: int) -> List[float]:
        """Extrahiert exakt 8 Game-State-Features"""
        features = []
        
        # Basis-Spiel-Info (4)
        features.extend([
            float(game_state.turn),
            float(game_state.last_roll),
            float(game_state.phase.value),
            float(game_state.current_player == player_no)
        ])
        
        # Robber-Info (2)
        robber_affects_me = 0.0
        if game_state.robber_tile:
            # Prüfe ob Robber meine Gebäude blockiert
            corner_ids = game_state.board.cornermap.get(game_state.robber_tile, [])
            for corner_id in corner_ids:
                corner = game_state.board.corners[corner_id]
                if corner.building.player_no == player_no:
                    robber_affects_me = 1.0
                    break
        
        features.extend([
            robber_affects_me,
            float(game_state.robber_state.value)
        ])
        
        # Leader-Info (2)
        max_vp = max(p.victory_points for p in game_state.players)
        my_vp = game_state.players[player_no].victory_points
        features.extend([
            float(max_vp),
            float(max_vp - my_vp)  # VP gap to leader
        ])
        
        return features[:8]  # Garantiert 8 Features
    
    def extract_action_features(self, game_state: GameState, player_no: int, 
                               action: Action) -> np.ndarray:
        """
        Extrahiert exakt 6 Action-Features
        """
        self.evaluator.game_state = game_state
        self.evaluator.player_no = player_no
        
        features = []
        
        # Action-Typ (4 Features - One-Hot)
        action_type_features = [0.0, 0.0, 0.0, 0.0]
        if action.action_type == ActionType.BUILD:
            action_type_features[0] = 1.0
        elif action.action_type == ActionType.TRADE:
            action_type_features[1] = 1.0
        elif action.action_type == ActionType.CARD:
            action_type_features[2] = 1.0
        else:  # PASS, DECLINE, etc.
            action_type_features[3] = 1.0
        
        features.extend(action_type_features)
        
        # Action-Evaluation (2 Features)
        evaluation_score = self._evaluate_action(action)
        features.extend([
            evaluation_score,
            1.0 if evaluation_score > 0.3 else 0.0  # Binary: good action
        ])
        
        return np.array(features[:6], dtype=np.float32)
    
    def _evaluate_action(self, action: Action) -> float:
        """Evaluiert Action mit Team6Player-Logik"""
        try:
            if isinstance(action, BuildCornerAction):
                score = self.evaluator.evaluate_settlement_location(action.corner)
                return min(1.0, score / 10.0)  # Normalisiert auf [0,1]
            elif isinstance(action, BuildEdgeAction):
                score = self.evaluator.evaluate_road_location(action.edge)
                return min(1.0, score / 5.0)   # Normalisiert auf [0,1]
            elif action.action_type == ActionType.TRADE:
                return 0.5  # Neutral für Trades
            elif action.action_type == ActionType.CARD:
                return 0.4  # Leicht positiv für Karten
            elif action.action_type == ActionType.PASS:
                return 0.1  # Niedrig für Pass
            else:
                return 0.0
        except:
            return 0.0  # Fallback