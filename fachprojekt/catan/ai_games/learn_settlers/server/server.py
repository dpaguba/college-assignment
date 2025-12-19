import queue, threading
import logging.config, time
from websockets import ConnectionClosed

from websockets.sync.server import serve
from  websockets.sync.server import ServerConnection

from ai_games.learn_settlers.com import *


# Logging
logging.config.fileConfig('ai_games/learn_settlers/utils/logging.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)
class Server:
    def __init__(self, host:str, port:int, callback) -> None:
        # Game
        self.callback = callback
        self.version = "0.2"

        # Internal
        self.clients:dict[str, ServerConnection] = {}
        self.host = host
        self.port = port

        # threading
        self.lock = threading.Lock()

    def start(self):
        with serve(self.handler, self.host, self.port) as server:
            server.serve_forever()

    def _send(self, ws:ServerConnection, message : Message):
        logger.info("Sending Message: " + str(message))
        ws.send(message.SerializeToString())

    def handler(self, websocket:ServerConnection):
        for message in websocket:
            t = time.time()
            msg:MyMessage = MyMessage()
            msg.ParseFromString(message)
            logger.info("Message Recived: " + str(msg))
            if msg.HasField("hello"):
                if msg.hello.version != self.version:
                    error = MyMessage()
                    error.error.error = "Wrong Protocol Version"
                    self._send(websocket,error)
                    continue
                logger.info("New Client")
                id = msg.client_id
                self.lock.acquire()
                self.clients[id] = websocket
                self.lock.release()
                welcome = MyMessage()
                welcome.welcome.client_id = id
                self._send(websocket,welcome)
            elif msg.HasField("close"):
                client_id = msg.close.client_id
                if client_id in self.clients.keys():
                    logger.info(f"Client {client_id} disconnected")
                    ws  = self.clients[client_id]
                    ws.close()
                    try:
                        self.clients.pop(client_id)
                    except KeyError:
                        logger.warning("Client already removed")
            self.callback(msg)
            logger.debug("Message handling time: " + str(time.time()-t))
        logger.debug("Connection Closed")

    def send(self, player_id, message : Message):
        try:
            self._send(self.clients[player_id],message)
        except(KeyError):
            logger.warning("Trying to send message to unkown client: " + str(player_id))
        except(ConnectionClosed):
            logger.warning("Trying to send message to closed connection: " + str(player_id))
            self.clients.pop(player_id)
