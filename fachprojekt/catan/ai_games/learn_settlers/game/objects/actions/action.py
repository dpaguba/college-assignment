from ai_games.learn_settlers.game.objects.actions.action_type import ActionType


class Action:
    
    def __init__(self, player_no:int, action_type:ActionType = ActionType.PASS) -> None:
        self.player_no = player_no
        self.action_type = action_type


    def __eq__(self, value: object) -> bool:
        assert isinstance(value, Action)
        return self.action_type == value.action_type and self.player_no == value.player_no
    
    def __str__(self) -> str:
        return f"P:{self.player_no} {self.action_type.name}"