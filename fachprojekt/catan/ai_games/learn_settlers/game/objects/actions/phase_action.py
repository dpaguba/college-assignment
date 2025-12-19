

from enum import IntEnum
from ai_games.learn_settlers.game.objects.actions.action import Action
from ai_games.learn_settlers.game.objects.actions.action_type import ActionType

class GamePhase(IntEnum):
    WAITING = 0
    SETUP = 1
    PLAY = 2
    ENDED = 3

class PhaseAction(Action):
    def __init__(self, player_no:int, game_phase:GamePhase, vp_update:list[int]|None = None):
        super().__init__(player_no, ActionType.GAMEPHASE)
        self.game_phase = game_phase
        self.vp_update = vp_update

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PhaseAction):
            return False
        return super().__eq__(other) and self.game_phase == other.game_phase and self.vp_update == other.vp_update

    def __str__(self) -> str:
        return f"New phase: {self.game_phase.name} by Player {self.player_no}"