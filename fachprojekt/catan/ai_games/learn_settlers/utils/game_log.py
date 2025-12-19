import gzip, time, uuid

from ai_games.learn_settlers.com import *
from ai_games.learn_settlers.com.message_decoder import MessageDecoder
from ai_games.learn_settlers.com.message_encoder import MessageEncoder
from ai_games.learn_settlers.game.objects.actions.action import Action
from ai_games.learn_settlers.game.objects.game_state import GameState

LOG_VERSION = 1
INT_SIZE = 2
# TODO save a seed for the card deck for reprodicibility
class GameLog():

    def __init__(self, id, continous_logging = False, enabled = True) -> None:

        self.create_time = time.strftime("%Y%m%d-%H%M%S")

        self.game_id = id
        self.log_id = uuid.uuid4().hex
        self.continous_logging = continous_logging
        self.enabled = enabled

        self.filename = "gamelog/" + str(self.create_time) +"_"+ str(self.game_id) + "_" + str(self.log_id) +".gamelog"

        self.log : list[MyMessage] = list()

        start_log = MyMessage()
        start_log.create_game.game_id = self.game_id
        start_log.create_game.time = self.create_time

        self.log.append(start_log)
        if self.continous_logging and self.enabled:
            start_str = start_log.SerializeToString()
            open(self.filename, "wb").write(LOG_VERSION.to_bytes(1) + len(start_str).to_bytes(INT_SIZE) +start_str)

    def append(self, type:MessageType, actions:Action|GameState):
        message = MessageEncoder.encode(type, actions)
        self.log.append(message)
        if self.continous_logging and self.enabled:
            ms = message.SerializeToString()
            open(self.filename, "ab").write( len(ms).to_bytes(INT_SIZE) + ms)

    def write(self, compress = True):
        if self.continous_logging or not self.enabled:
            return
        f = gzip.open(self.filename +".gz", "wb") if compress else open(self.filename, "wb")
        f.write(LOG_VERSION.to_bytes(1, "big"))
        f.write(b"".join([len((p:=l.SerializeToString())).to_bytes(INT_SIZE, "big") +  p for l in self.log]))
        f.close()

    # def write_error(self, compress = False):
    #     if compress:
    #         gzip.open(self.filename +".errorlog.gz", "wb").write(b"\n".join([l.SerializeToString() for l in self.log]))
    #     else:
    #         open(self.filename +".errorlog", "wb").write(b"\n".join([l.SerializeToString() for l in self.log]))