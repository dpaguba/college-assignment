import random
import numpy as np
from typing import List, Dict, Tuple, Set, Optional

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
from ai_games.learn_settlers.ai.team6.strategy_manager import StrategyManager




class Team6Player(Player):
    def __init__(self, name: str = "Team6AI") -> None:
        super().__init__(PlayerType.AI, name=name)
        self.initialize_strategy()

    def initialize_strategy(self) -> None:
        # Probabilities are relative to each other and maybe should be adjusted based on the performance
        # Building priorities
        self.building_priorities = {
            "settlement": 2,  # High priority for settlements (1 VP)
            "city": 3,         # Medium-high priority for cities (1 VP and free up settlement)
            "road": 1,         # Medium priority for roads (needed for settlements and the longest road)
            "card": 4,         # Lower priority for cards (uncertain benefit)
        }

        divider_resource = self.building_priorities["settlement"]+self.building_priorities["road"]*2+self.building_priorities["card"]+self.building_priorities["settlement"]+2* self.building_priorities["city"]+self.building_priorities["card"]+3* self.building_priorities["city"]+self.building_priorities["card"]
        """Initialize the strategy parameters for the AI"""
        # Resource value weights - how important each resource is
        self.resource_values = {
            0: (self.building_priorities["settlement"]+self.building_priorities["road"])/divider_resource,  # Wood - needed for roads and settlements
            1: (self.building_priorities["settlement"]+self.building_priorities["road"])/divider_resource,  # Brick - needed for roads and settlements
            2: (self.building_priorities["card"])/divider_resource,  # Sheep - needed only for dev cards
            3: (self.building_priorities["settlement"]+2* self.building_priorities["city"]+self.building_priorities["card"])/divider_resource, # Wheat/Grain - needed for settlements, cities, and dev cards
            4: (3* self.building_priorities["city"]+self.building_priorities["card"])/divider_resource,  # Ore - needed for cities and dev cards
        }

        # Development card play priorities
        self.dev_card_priorities = {
            DevelopmentCard.KNIGHT: 8,          # High for robber control and the largest army
            DevelopmentCard.ROAD_BUILDING: 7,   # Free roads are valuable
            DevelopmentCard.YEAR_OF_PLENTY: 6,  # Good for getting the necessary resources
            DevelopmentCard.MONOPOLY: 5,        # Situational, but can be powerful
        }
        
        # Dice probability per number (used for settlement placement)
        self.dice_probabilities = {
            2: 1,
            3: 2,
            4: 3,
            5: 4,
            6: 5,
            8: 5,
            9: 4,
            10: 3,
            11: 2,
            12: 1,
        }

    # Track initial settlement placement for diversity scoring
        self.settlement_count = 0
        self.first_settlement_resources = set()
        self.first_settlement_dice_numbers = set()

    def handle_request(self, message_type: MessageType, possible_actions: list[Action]) -> Action:
        """Main function to handle action requests from the game"""
        assert self.game_state is not None
        my_no = self.player_no
        
        # Handle discard actions first
        if len(possible_actions) > 0 and isinstance(possible_actions[0], DiscardAction):
            return self.handle_discard(possible_actions[0])
        
        # Handle game phases
        if self.game_state.phase == GamePhase.SETUP:
            return self.handle_setup(possible_actions)
        
        # Handle dice roll
        if len(possible_actions) == 1 and isinstance(possible_actions[0], DiceAction):
            return possible_actions[0]
        
        # Handle robber placement
        if self.game_state.robber_state == RobberState.PLACE_ROBBER:
            return self.handle_robber_placement(possible_actions)
        
        # Handle robber stealing
        if self.game_state.robber_state == RobberState.STEAL_RESOURCE:
            return self.handle_robber_steal(possible_actions)
        
        # Handle monopoly card
        if self.game_state.monopoly:
            return self.handle_monopoly(possible_actions)
        
        # Handle year of plenty card
        if self.game_state.year_of_plenty > 0:
            return self.handle_year_of_plenty(possible_actions)
        
        # Handle road building card
        if self.game_state.road_building > 0:
            return self.handle_road_building(possible_actions)
        
        # Handle regular turn
        return self.handle_turn(possible_actions)


# TODO: Uberschuss beruecksichtigen
    def handle_discard(self, discard_action: DiscardAction) -> Action:
        """Handle resource discarding - strategically discard the least useful resources"""
        discard_logic = DiscardHelper(self.game_state, discard_action)
        
        # Get all possible discards
        possible_discards = discard_logic.propose_discard()
        
        # We need to discard multiple resources
        while discard_logic.to_discard > 0:
            # Create a list of discards with their values
            valued_discards = []
            for discard in possible_discards:
                # Find which resource is being discarded
                res_idx = np.argmax(discard.out_resources[0:5])
                value = self.resource_values[res_idx]
                valued_discards.append((discard, value))
            
            # Sort by value (the least valuable first)
            valued_discards.sort(key=lambda x: x[1])
            
            # Take the least valuable resource
            chosen_discard = valued_discards[0][0]
            
            # Apply the discard and get new options
            more_to_discard = discard_logic.apply_discard(chosen_discard)
            
            if more_to_discard:
                possible_discards = discard_logic.propose_discard()
        
        return discard_logic.get_action()

    def handle_setup(self, possible_actions: list[Action]) -> Action:
        """Handle initial settlement and road placement in the setup phase"""
        action_types = [type(action) for action in possible_actions]
        
        # Initial settlement placement
        if BuildCornerAction in action_types:
            return self.choose_initial_settlement(possible_actions)
        
        # Initial road placement
        elif BuildEdgeAction in action_types:
            return self.choose_initial_road(possible_actions)
        
        # Fallback to random choice in case of an unknown action
        return random.choice(possible_actions)

    def choose_initial_settlement(self, possible_actions: list[Action]) -> BuildCornerAction:
        """Choose the best location for initial settlement based on resource production potential"""
        corner_actions = [action for action in possible_actions if isinstance(action, BuildCornerAction)]

        # Evaluate each corner based on resource quality and probability
        scored_corners = []
        for action in corner_actions:
            corner = action.corner
            score = self.evaluate_settlement_location(corner)
            scored_corners.append((action, score))

        # Sort by score (highest first)
        scored_corners.sort(key=lambda x: x[1], reverse=True)

        # Return the highest scored corner
        best_action = scored_corners[0][0]

        # Store data about the first settlement placement
        self.settlement_count += 1
        if self.settlement_count == 1:
            for tile_id in best_action.corner.tiles:
                tile = self.game_state.board.get_tile_by_id(tile_id)
                if tile is None or tile.terrain in [Terrain.Water, Terrain.Desert]:
                    continue
                self.first_settlement_resources.add(tile.terrain.value)
                self.first_settlement_dice_numbers.add(tile.dice)

        return best_action


    def evaluate_settlement_location(self, corner: Corner) -> float:
        """Evaluate a potential settlement location based on resource production and other factors"""
        score = 0.0
        source_types = set() #for diversity of ressource types
        dice_numbers = set() #for diversity of dice values
        
        # Look at adjacent tiles and their resource types and probabilities
        for tile_id in corner.tiles:
            tile = self.game_state.board.get_tile_by_id(tile_id)
            if tile is None or tile.terrain == Terrain.Water or tile.terrain == Terrain.Desert:
                continue

            #gather ressource types for diversity
            source_types.add(tile.terrain.value)
            #gather dice numbers to the set
            dice_numbers.add(tile.dice)

            
            # Add a score based on the resource type
            resource_value = self.resource_values[tile.terrain.value]
            
            # Add score based on dice probability
            if tile.dice in self.dice_probabilities:
                dice_value = self.dice_probabilities[tile.dice]
                score += resource_value * dice_value
        
        # Bonus for harbors
        if corner.building.building_id == BuildingType.HARBOR and corner.building.resources is not None:
            # Check if it's a resource-specific harbor (2:1) or generic harbor (3:1)
            min_trade_cost = min(corner.building.resources)
            if min_trade_cost == 2:  # Resource-specific harbor
                resources = np.where(corner.building.resources == 2)[0]
                # If it's a resource we value highly, it's even better
                for res in resources:
                    if res < 5:  # Make sure it's a valid resource index
                        score += self.resource_values[res] * 2
            else:  # Generic harbor (3:1)
                score += 2  # Still valuable but less than resource-specific

        # Ressource diversity bonus
        if len(source_types) == 3:
            score += 1.5
        elif len(source_types) == 2:
            score += 0.5

        #dice diversity bonus
        if len(dice_numbers) == 3:
            score += 1.5
        elif len(dice_numbers) == 2:
            score += 0.5

        # Only consider variety bonus for the second settlement
        if self.settlement_count == 2:
            new_resources = source_types - self.first_settlement_resources
            if len(new_resources) == 3:
                score += 1.5
            elif len(new_resources) == 2:
                score += 1.0
            elif len(new_resources) == 1:
                score += 0.5

            new_dice_numbers = dice_numbers - self.first_settlement_dice_numbers
            if len(new_dice_numbers) == 3:
                score += 1.5
            elif len(new_dice_numbers) == 2:
                score += 1.0
            elif len(new_dice_numbers) == 1:
                score += 0.5


        
        return score

    def choose_initial_road(self, possible_actions: list[Action]) -> BuildEdgeAction:
        """Choose the best edge for initial road placement"""
        edge_actions = [action for action in possible_actions if isinstance(action, BuildEdgeAction)]
        
        # For initial roads, we want to place them in a direction that allows for future expansion
        # Calculate a simple score based on how many valid empty corners are adjacent
        scored_edges = []
        for action in edge_actions:
            edge = action.edge
            score = self.evaluate_road_location(edge)
            scored_edges.append((action, score))
        
        # Sort by score (highest first)
        scored_edges.sort(key=lambda x: x[1], reverse=True)
        
        # Return the highest scored edge
        return scored_edges[0][0]

    def evaluate_road_location(self, edge: Edge) -> float:
        """Evaluate a potential road location based on future expansion potential"""
        score = 0.0
        
        # Check both ends of the road for potential settlement locations
        adjacent_corners = self.game_state.board.get_neighbors_of_edge(edge.id)
        for corner in adjacent_corners:
            # Skip corners that already have buildings
            if corner.building.building_id not in [BuildingType.EMPTY, BuildingType.HARBOR]:
                continue
                
            # Evaluate the corner as a potential settlement location
            corner_score = self.evaluate_settlement_location(corner)
            score += corner_score
            
            # Bonus if this corner is in the possible settlements set
            if corner in self.game_state.board.possible_settlements:
                score += 5
        
        return score

    def handle_robber_placement(self, possible_actions: list[Action]) -> Action:
        """Choose where to place the robber to hinder opponents the most"""
        robber_actions = [action for action in possible_actions if isinstance(action, RobberAction)]
        
        # Score each potential robber location
        scored_locations = []
        for action in robber_actions:
            tile = action.tile
            score = self.evaluate_robber_location(tile)
            scored_locations.append((action, score))
        
        # Sort by score (highest first)
        scored_locations.sort(key=lambda x: x[1], reverse=True)
        
        # Return the highest scored location
        return scored_locations[0][0]

    def evaluate_robber_location(self, tile: Tile) -> float:
        """Evaluate a location for placing the robber"""
        score = 0.0
        my_no = self.player_no
        
        # Get all corners adjacent to this tile
        corner_ids = self.game_state.board.cornermap.get(tile.pos, [])
        corners = [self.game_state.board.corners[corner_id] for corner_id in corner_ids]
        
        # Check which players have buildings on these corners
        for corner in corners:
            if corner.building.player_no >= 0 and corner.building.player_no != my_no:
                # Opponent has a building here
                opponent_no = corner.building.player_no
                opponent = self.game_state.players[opponent_no]
                
                # Higher score for focusing on players with more points
                score += opponent.victory_points * 2
                
                # Higher score if they have many resources
                score += opponent.resources[-1]
                
                # Higher score for targeting building type (city > settlement)
                if corner.building.building_id in [BuildingType.CITY, BuildingType.HARBOR_CITY]:
                    score += 3
                else:
                    score += 1
                
                # Higher score if the tile produces a valuable resource
                if tile.terrain.value < 5:  # Not desert or water
                    resource_value = self.resource_values[tile.terrain.value]
                    dice_prob = self.dice_probabilities.get(tile.dice, 0)
                    score += resource_value * dice_prob
        
        return score

    def handle_robber_steal(self, possible_actions: list[Action]) -> Action:
        """Choose which player to steal from"""
        # If we can only decline, do so
        if len(possible_actions) == 1 and possible_actions[0].action_type == ActionType.DECLINE:
            return possible_actions[0]
            
        # Get all robber steal actions
        steal_actions = [action for action in possible_actions if isinstance(action, RobberAction) and action.robber_type == RobberActionType.STEAL]
        
        # Score each potential target
        scored_targets = []
        for action in steal_actions:
            target_no = action.target_player
            score = self.evaluate_steal_target(target_no)
            scored_targets.append((action, score))
        
        # Sort by score (highest first)
        scored_targets.sort(key=lambda x: x[1], reverse=True)
        
        # Return the highest-scored target
        return scored_targets[0][0]

    def evaluate_steal_target(self, target_no: int) -> float:
        """Evaluate a player as a potential robbery target"""
        target = self.game_state.players[target_no]
        score = 0.0
        
        # Higher score for players with more victory points (leader targeting)
        score += target.victory_points * 2
        
        # Higher score for players with more resources
        score += target.resources[-1] * 1.5
        
        # Higher score for players with the longest road or the largest army
        if target.longest_road:
            score += 3
        if target.largest_army:
            score += 3
        
        return score

    def handle_monopoly(self, possible_actions: list[Action]) -> Action:
        """Choose which resource to monopolize"""
        # If we can only decline, do so
        if len(possible_actions) == 1 and possible_actions[0].action_type == ActionType.DECLINE:
            return possible_actions[0]
            
        # Get all trade actions (monopoly uses trade actions with target_player=-2)
        monopoly_actions = [action for action in possible_actions if isinstance(action, TradeAction)]
        
        # Score each potential resource to monopolize
        scored_resources = []
        for action in monopoly_actions:
            resource_idx = np.argmax(action.in_resources[0:5])
            score = self.evaluate_monopoly_resource(resource_idx)
            scored_resources.append((action, score))
        
        # Sort by score (highest first)
        scored_resources.sort(key=lambda x: x[1], reverse=True)
        
        # Return the highest scored resource
        return scored_resources[0][0]

    def evaluate_monopoly_resource(self, resource_idx: int) -> float:
        """Evaluate a resource for the monopoly card"""
        score = 0.0
        my_no = self.player_no
        
        # Base score is the value of the resource
        score += self.resource_values[resource_idx] * 2
        
        # Check how many of this resource other players have
        total_in_play = 0
        for player_idx, player in enumerate(self.game_state.players):
            if player_idx != my_no:
                total_in_play += player.resources[resource_idx]
        
        # More of the resource in play = better monopoly target
        score += total_in_play * 3
        
        # Bonus if we need this resource for our current goals
        my_resources = self.game_state.players[my_no].resources
        
        # If we're close to having enough for a settlement
        if (resource_idx in [0, 1, 2, 3] and  # Wood, Brick, Sheep, Wheat
            my_resources[0] > 0 and my_resources[1] > 0 and  # Some Wood and Brick
            my_resources[2] > 0 and my_resources[3] > 0):    # Some Sheep and Wheat
            score += 2
            
        # If we're close to having enough for a city
        if (resource_idx in [3, 4] and  # Wheat, Ore
            my_resources[3] > 0 and my_resources[4] > 0):  # Some Wheat and Ore
            score += 3
        
        return score

    def handle_year_of_plenty(self, possible_actions: list[Action]) -> Action:
        """Choose which resources to gain with Year of Plenty"""
        # If we can only decline, do so
        if len(possible_actions) == 1 and possible_actions[0].action_type == ActionType.DECLINE:
            return possible_actions[0]
            
        # Get all trade actions (Year of Plenty uses trade actions with target_player=-1)
        yop_actions = [action for action in possible_actions if isinstance(action, TradeAction)]
        
        # Score each potential resource to take
        scored_resources = []
        for action in yop_actions:
            resource_idx = np.argmax(action.in_resources[0:5])
            score = self.evaluate_yop_resource(resource_idx)
            scored_resources.append((action, score))
        
        # Sort by score (highest first)
        scored_resources.sort(key=lambda x: x[1], reverse=True)
        
        # If this is our first pick, and we have more than one option
        if self.game_state.year_of_plenty == 2 and len(scored_resources) > 1:
            return scored_resources[0][0]
        # For the second pick, we may want a different resource
        elif self.game_state.year_of_plenty == 1 and len(scored_resources) > 1:
            # Try to get a complementary resource
            my_resources = self.game_state.players[self.player_no].resources
            
            # Check what we need most
            if my_resources[0] == 0 and my_resources[1] >= 1:  # Need Wood for Road/Settlement
                for action, _ in scored_resources:
                    if action.in_resources[0] > 0:  # Wood
                        return action
            elif my_resources[1] == 0 and my_resources[0] >= 1:  # Need Brick for Road/Settlement
                for action, _ in scored_resources:
                    if action.in_resources[1] > 0:  # Brick
                        return action
            elif my_resources[3] == 1 and my_resources[4] >= 2:  # Need 1 more Wheat for City
                for action, _ in scored_resources:
                    if action.in_resources[3] > 0:  # Wheat
                        return action
            elif my_resources[4] == 2 and my_resources[3] >= 1:  # Need 1 more Ore for City
                for action, _ in scored_resources:
                    if action.in_resources[4] > 0:  # Ore
                        return action
            
            # If no special case, just take the highest scored one
            return scored_resources[0][0]
        else:
            return scored_resources[0][0]

    def evaluate_yop_resource(self, resource_idx: int) -> float:
        """Evaluate a resource for the Year of Plenty card"""
        score = 0.0
        my_no = self.player_no
        my_resources = self.game_state.players[my_no].resources
        
        # Base score is the value of the resource
        score += self.resource_values[resource_idx] * 2
        
        # Bonus if the resource is rare in the bank
        bank_amount = self.game_state.resources[resource_idx]
        if bank_amount < 5:
            score += (5 - bank_amount)
        
        # Bonus if we need this resource for our current goals
        
        # If we need this resource for a road
        if resource_idx in [0, 1] and my_resources[resource_idx] == 0:  # Wood or Brick
            score += 3
            
        # If we need this resource for a settlement
        if resource_idx in [0, 1, 2, 3] and my_resources[resource_idx] == 0:  # Any settlement resource
            score += 4
            
        # If we need this resource for a city
        if resource_idx in [3, 4]:  # Wheat or Ore
            # More points if we're close to building a city
            if my_resources[3] >= 1 and my_resources[4] >= 2:  # Have enough already
                score += 0
            elif my_resources[3] == 1 and my_resources[4] == 2 and resource_idx == 3:  # Need 1 more Wheat
                score += 5
            elif my_resources[3] == 2 and my_resources[4] == 1 and resource_idx == 4:  # Need 1 more Ore
                score += 5
            elif my_resources[3] == 1 and my_resources[4] == 1 and resource_idx == 4:  # Need 2 more Ore
                score += 4
            elif my_resources[3] == 0 and my_resources[4] == 2 and resource_idx == 3:  # Need 2 more Wheat
                score += 4
            else:
                score += 2
        
        return score

    def handle_road_building(self, possible_actions: list[Action]) -> Action:
        """Choose where to build roads with the Road Building card"""
        # If we can only decline, do so
        if len(possible_actions) == 1 and possible_actions[0].action_type == ActionType.DECLINE:
            return possible_actions[0]
            
        # Get all build edge actions
        road_actions = [action for action in possible_actions if isinstance(action, BuildEdgeAction)]
        
        # Score each potential road location
        scored_roads = []
        for action in road_actions:
            edge = action.edge
            score = self.evaluate_road_location(edge)
            scored_roads.append((action, score))
        
        # Sort by score (highest first)
        scored_roads.sort(key=lambda x: x[1], reverse=True)
        
        # Return the highest scored road
        return scored_roads[0][0]

    def handle_turn(self, possible_actions: list[Action]) -> Action:
        """Handle regular turn actions, choosing the most strategic option"""
        # Group actions by type for easier processing
        action_groups = self.group_actions_by_type(possible_actions)
        
        # If we can do nothing else but pass, then pass
        if len(possible_actions) == 1 and possible_actions[0].action_type == ActionType.PASS:
            return possible_actions[0]
        
        # Check if we should build a settlement
        settlement_actions = action_groups.get("settlement", [])
        if settlement_actions:
            best_settlement = self.choose_best_settlement(settlement_actions)
            if best_settlement:
                return best_settlement
        
        # Check if we should build a city
        city_actions = action_groups.get("city", [])
        if city_actions:
            best_city = self.choose_best_city(city_actions)
            if best_city:
                return best_city
        
        # Check if we should build a road
        road_actions = action_groups.get("road", [])
        if road_actions:
            best_road = self.choose_best_road(road_actions)
            if best_road:
                return best_road
        
        # Check if we should buy a development card
        card_actions = action_groups.get("card", [])
        if card_actions and card_actions[0].draw:
            should_buy = self.should_buy_development_card()
            if should_buy:
                return card_actions[0]
        
        # Check if we should play a development card
        if card_actions:
            for action in card_actions:
                if not action.draw and action.card_type is not None:
                    if self.should_play_development_card(action.card_type):
                        return action
        
        # Check if we should trade with the bank
        trade_actions = action_groups.get("trade", [])
        if trade_actions:
            best_trade = self.choose_best_trade(trade_actions)
            if best_trade:
                return best_trade
        
        # If no good action found, pass
        for action in possible_actions:
            if action.action_type == ActionType.PASS:
                return action
        
        # Fallback to random choice
        return random.choice(possible_actions)

    def group_actions_by_type(self, possible_actions: list[Action]) -> Dict[str, list[Action]]:
        """Group actions by their type for easier processing"""
        groups = {}
        
        for action in possible_actions:
            if action.action_type == ActionType.BUILD:
                if isinstance(action, BuildCornerAction):
                    if action.building_type in [BuildingType.SETTLEMENT, BuildingType.HARBOR_SETTLEMENT]:
                        groups.setdefault("settlement", []).append(action)
                    elif action.building_type in [BuildingType.CITY, BuildingType.HARBOR_CITY]:
                        groups.setdefault("city", []).append(action)
                elif isinstance(action, BuildEdgeAction):
                    groups.setdefault("road", []).append(action)
            elif action.action_type == ActionType.CARD:
                groups.setdefault("card", []).append(action)
            elif action.action_type == ActionType.TRADE:
                groups.setdefault("trade", []).append(action)
            elif action.action_type == ActionType.PASS:
                groups.setdefault("pass", []).append(action)
        
        return groups

    def choose_best_settlement(self, settlement_actions: list[BuildCornerAction]) -> Optional[BuildCornerAction]:
        """Choose the best settlement location to build"""
        my_no = self.player_no
        my_resources = self.game_state.players[my_no].resources
        
        # Check if we have resources for a settlement
        if (my_resources[0] >= 1 and my_resources[1] >= 1 and
            my_resources[2] >= 1 and my_resources[3] >= 1):
            
            # Score each potential settlement location
            scored_settlements = []
            for action in settlement_actions:
                corner = action.corner
                score = self.evaluate_settlement_location(corner)
                scored_settlements.append((action, score))
            
            # Sort by score (highest first)
            scored_settlements.sort(key=lambda x: x[1], reverse=True)
            
            # Only build if the best settlement is good enough
            if scored_settlements and scored_settlements[0][1] > 2.0:
                return scored_settlements[0][0]
        
        return None

    def choose_best_city(self, city_actions: list[BuildCornerAction]) -> Optional[BuildCornerAction]:
        """Choose the best city location to build"""
        my_no = self.player_no
        my_resources = self.game_state.players[my_no].resources
        
        # Check if we have resources for a city
        if my_resources[3] >= 2 and my_resources[4] >= 3:
            
            # Score each potential city location
            scored_cities = []
            for action in city_actions:
                corner = action.corner
                score = self.evaluate_city_location(corner)
                scored_cities.append((action, score))
            
            # Sort by score (highest first)
            scored_cities.sort(key=lambda x: x[1], reverse=True)
            
            # Only build if the best city is good enough
            if scored_cities and scored_cities[0][1] > 3.0:
                return scored_cities[0][0]
        
        return None

    def evaluate_city_location(self, corner: Corner) -> float:
        """Evaluate a potential city location"""
        score = 0.0
        
        # Look at adjacent tiles and their resource types and probabilities
        for tile_id in corner.tiles:
            tile = self.game_state.board.get_tile_by_id(tile_id)
            if tile is None or tile.terrain == Terrain.Water or tile.terrain == Terrain.Desert:
                continue
            
            # Add score based on resource type (value x2 for cities)
            resource_value = self.resource_values[tile.terrain.value] * 2
            
            # Add score based on dice probability
            if tile.dice in self.dice_probabilities:
                dice_value = self.dice_probabilities[tile.dice]
                score += resource_value * dice_value
        
        # Extra points for harbors
        if corner.building.building_id == BuildingType.HARBOR_SETTLEMENT and corner.building.resources is not None:
            # Resource-specific harbor
            min_trade_cost = min(corner.building.resources)
            if min_trade_cost == 2:
                resources = np.where(corner.building.resources == 2)[0]
                for res in resources:
                    if res < 5:
                        score += self.resource_values[res] * 3
            else:  # Generic harbor
                score += 3
        
        return score

    def choose_best_road(self, road_actions: list[BuildEdgeAction]) -> Optional[BuildEdgeAction]:
        """Choose the best road location to build"""
        my_no = self.player_no
        my_resources = self.game_state.players[my_no].resources
        
        # Check if we have resources for a road
        if my_resources[0] >= 1 and my_resources[1] >= 1:
            
            # Score each potential road location
            scored_roads = []
            for action in road_actions:
                edge = action.edge
                score = self.evaluate_road_location(edge)
                scored_roads.append((action, score))
            
            # Sort by score (highest first)
            scored_roads.sort(key=lambda x: x[1], reverse=True)
            
            # Only build if the best road is good enough
            if scored_roads and scored_roads[0][1] > 1.0:
                return scored_roads[0][0]
        
        return None

    def should_buy_development_card(self) -> bool:
        """Decide if we should buy a development card"""
        my_no = self.player_no
        my_resources = self.game_state.players[my_no].resources
        
        # Check if we have resources for a development card
        if my_resources[2] >= 1 and my_resources[3] >= 1 and my_resources[4] >= 1:
            # Factors that make buying a card more attractive:
            
            # 1. If we already have 2 knight cards played (almost largest army)
            if self.game_state.players[my_no].knights >= 2:
                return True
                
            # 2. If we're close to 10 victory points, a victory point card might win the game
            if self.game_state.players[my_no].victory_points >= 8:
                return True
                
            # 3. If we have excess sheep, wheat, and ore
            if (my_resources[2] > 2 and my_resources[3] > 2 and my_resources[4] > 2):
                return True
                
            # 4. If we're in the middle game and need more ways to get points
            if (len(self.game_state.players[my_no].buildings) >= 3 and 
                self.game_state.players[my_no].victory_points >= 4):
                return True
            
            # 5. If we have a lot of one resource and could use monopoly
            max_resource = max(my_resources[0:5])
            if max_resource >= 4:
                return True
                
            # Otherwise, prioritize other buildings
            return False
        
        return False

    def should_play_development_card(self, card_type: DevelopmentCard) -> bool:
        """Decide if we should play a development card"""
        my_no = self.player_no
        
        if card_type == DevelopmentCard.KNIGHT:
            # Play knight if:
            # 1. We are close to the largest army
            if self.game_state.players[my_no].knights >= 2:
                return True
                
            # 2. Someone else is about to get the largest army
            for player in self.game_state.players:
                if player.knights >= 2 and not player.largest_army and player != self.game_state.players[my_no]:
                    return True
                    
            # 3. There are valuable resources to block
            for tile in [tile for row in self.game_state.board.tiles for tile in row if tile is not None]:
                if tile.pos != self.game_state.robber_tile and tile.dice in [6, 8]:
                    # Check if opponents have settlements/cities on this tile
                    corner_ids = self.game_state.board.cornermap.get(tile.pos, [])
                    for corner_id in corner_ids:
                        corner = self.game_state.board.corners[corner_id]
                        if corner.building.player_no >= 0 and corner.building.player_no != my_no:
                            return True
            
            # 4. A player is getting too far ahead
            leader_points = max([p.victory_points for p in self.game_state.players])
            if leader_points >= 8 and leader_points > self.game_state.players[my_no].victory_points:
                return True
                
            # Otherwise, save it
            return False
            
        elif card_type == DevelopmentCard.ROAD_BUILDING:
            # Always play road building if available - free roads are always good
            return True
            
        elif card_type == DevelopmentCard.YEAR_OF_PLENTY:
            # Play year of plenty if:
            # 1. We need specific resources to build something important
            my_resources = self.game_state.players[my_no].resources
            
            # Need resources for a settlement
            if (my_resources[0] == 0 or my_resources[1] == 0 or 
                my_resources[2] == 0 or my_resources[3] == 0):
                # If we have most of the resources for a settlement
                count = sum([1 for i in range(4) if my_resources[i] >= 1])
                if count >= 2:
                    return True
            
            # Need resources for a city
            if (my_resources[3] < 2 or my_resources[4] < 3) and (my_resources[3] >= 1 and my_resources[4] >= 1):
                return True
                
            # 2. A resource is rare in the bank
            for i in range(5):
                if self.game_state.resources[i] <= 2 and self.resource_values[i] >= 1.0:
                    return True
                    
            # Otherwise, save it
            return False
            
        elif card_type == DevelopmentCard.MONOPOLY:
            # Play monopoly if:
            # 1. Several players have a resource we need
            my_resources = self.game_state.players[my_no].resources
            for resource_idx in range(5):
                # Count how many of this resource other players have
                other_players_resources = sum([p.resources[resource_idx] for p in self.game_state.players if p != self.game_state.players[my_no]])
                
                # If there are a lot of these resources in play
                if other_players_resources >= 4:
                    # And it's valuable to us
                    if self.resource_values[resource_idx] >= 1.0:
                        return True
            
            # 2. We're close to building something important and need a specific resource
            # For settlement
            if (my_resources[0] == 0 and my_resources[1] >= 1 and 
                my_resources[2] >= 1 and my_resources[3] >= 1):
                # Check if wood is in other players' hands
                wood_in_play = sum([p.resources[0] for p in self.game_state.players if p != self.game_state.players[my_no]])
                if wood_in_play >= 3:
                    return True
            
            # For city
            if my_resources[3] == 1 and my_resources[4] >= 2:
                # Check if wheat is in other players' hands
                wheat_in_play = sum([p.resources[3] for p in self.game_state.players if p != self.game_state.players[my_no]])
                if wheat_in_play >= 3:
                    return True
            
            # Otherwise, save it
            return False
        
        return False

# TODO: verbessern
    def choose_best_trade(self, trade_actions: list[TradeAction]) -> Optional[TradeAction]:
        """Choose the best trade to make with the bank"""
        my_no = self.player_no
        my_resources = self.game_state.players[my_no].resources
        
        # Evaluate what we need most
        needed_resources = []
        
        # If we're close to building a settlement
        settlement_needs = []
        for i in range(4):  # Wood, Brick, Sheep, Wheat
            if my_resources[i] == 0:
                settlement_needs.append(i)
        
        # If we're close to building a city
        city_needs = []
        if my_resources[3] < 2:  # Need more Wheat
            city_needs.append(3)
        if my_resources[4] < 3:  # Need more Ore
            city_needs.append(4)
        
        # If we're close to building a road
        road_needs = []
        if my_resources[0] == 0:  # Need Wood
            road_needs.append(0)
        if my_resources[1] == 0:  # Need Brick
            road_needs.append(1)
        
        # Determine what we need most based on current building options
        if len(settlement_needs) == 1 and sum([my_resources[i] for i in range(4) if i != settlement_needs[0]]) >= 3:
            needed_resources.extend(settlement_needs)
        if len(city_needs) == 1 and (my_resources[3] >= 1 and my_resources[4] >= 1):
            needed_resources.extend(city_needs)
        if len(road_needs) == 1 and ((road_needs[0] == 0 and my_resources[1] >= 1) or (road_needs[0] == 1 and my_resources[0] >= 1)):
            needed_resources.extend(road_needs)
        
        # If we don't have specific needs, prioritize based on resource values
        if not needed_resources:
            for i in range(5):
                if my_resources[i] == 0:
                    needed_resources.append(i)
        
        # Score each potential trade
        scored_trades = []
        for action in trade_actions:
            if action.target_player == -1:  # Bank trade
                # What resource are we getting?
                in_resource = np.argmax(action.in_resources[0:5])
                
                # What resource are we giving?
                out_resource = np.argmax(action.out_resources[0:5])
                out_amount = action.out_resources[out_resource]
                
                # Calculate trade value
                value_gain = self.resource_values[in_resource]
                value_loss = self.resource_values[out_resource] * out_amount
                net_value = value_gain - value_loss
                
                # Bonus if we need this resource
                if in_resource in needed_resources:
                    net_value += 2
                
                # Bonus if we have excess of the resource we're giving
                if my_resources[out_resource] >= 4:
                    net_value += 1
                
                # Only trade if it's a net benefit
                if net_value > 0:
                    scored_trades.append((action, net_value))
        
        # Sort by value (highest first)
        scored_trades.sort(key=lambda x: x[1], reverse=True)
        
        # Return the best trade if it exists
        if scored_trades:
            return scored_trades[0][0]
        
        return None
    