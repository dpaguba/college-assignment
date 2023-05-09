import os

os.makedirs("logs",exist_ok=True)
os.makedirs("gamelog",exist_ok=True)

from google.protobuf.message import Message
from ai_games.learn_settlers.com.message_type import MessageType
from ai_games.learn_settlers.com.com_pb2 import MyMessage, PlayerType, GamePhaseMessage,TerrainMessage, TileList, TileMessage, CornerMessage, EdgeMessage, BuildingMessage, PlayerStatsMessage, GameStateMessage, TileIdMessage, BoardMessage, BuildCornerMessage, BuildEdgeMessage, DiceActionMessage, PhaseActionMessage, TradeActionMessage, RobberActionMessage, CardActionMessage, ActionMessage, ActionListMessage, RoadChangeMessage, DiscardMessage  # type: ignore