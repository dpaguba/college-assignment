import  logging.config
import threading
from asyncio import Queue
from concurrent.futures import ThreadPoolExecutor

from websockets.sync.client import connect
from websockets.sync.client import ClientConnection
from websockets.sync.connection import Connection

from ai_games.learn_settlers.com import *

# Logging
logging.config.fileConfig('ai_games/learn_settlers/utils/logging.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)
class Client:
    def __init__(self, callback, client_id:str) -> None:
        # Game
        self.callback = callback

        # asyncio
        self.executor = ThreadPoolExecutor(max_workers=16)
        self.message_queue = Queue()
        

        # Websocket
        self.id:str = client_id
        self.ws: ClientConnection | None | Connection = None

        # Stats
        self.connected = threading.Event()

    # Internal Messaging
    def get_executor(self):
        return self.executor
    
    def start(self, uri):
        with connect(uri) as websocket:
            self.ws = websocket
            self.connected.set()
            for message in websocket:
                msg:MyMessage = MyMessage()
                msg.ParseFromString(message)
                logger.info(f"Recived Message: {msg}")
                if msg.HasField("welcome"):
                    assert self.id == msg.welcome.client_id
                    logger.info(f"Connected with ID: {self.id}")
                self.get_executor().submit(self.callback,msg)
            logger.debug("Connection Closed")

    def connect(self, uri):
        self.get_executor().submit(self.start, uri)
        msg = MyMessage()
        msg.client_id = self.id
        msg.hello.version = "0.2"
        self.send_message(msg)
        logger.debug("Connection Requested")
    
    def close(self):
        assert self.ws is not None
        logger.debug("Starting shutdown procedure")
        msg = MyMessage()
        msg.close.version = "0.2"
        msg.close.client_id = self.id
        self.send_message(msg)
        self.ws.close()
        
    def send_message(self, message: Message):
        self.connected.wait()
        assert self.ws is not None
        logger.info(f"Sending Message: {message}")
        self.ws.send(message.SerializeToString())
