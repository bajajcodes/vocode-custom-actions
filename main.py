import logging
import os
import sys
import uvicorn
import typing

# Third-party imports
from fastapi import FastAPI
from vocode.streaming.telephony.config_manager.redis_config_manager import (
    RedisConfigManager,
)
from vocode.streaming.telephony.server.base import (
    TelephonyServer
)
from dotenv import load_dotenv

from vocode.streaming.models.events import Event, EventType
from vocode.streaming.models.transcript import (TranscriptCompleteEvent)
from vocode.streaming.utils import events_manager
from agent_actions.custom_agent_factory import MyAgentFactory

# if running from python, this will load the local .env
# docker-compose will load the .env file by itself
load_dotenv()

app = FastAPI(docs_url=None)

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

config_manager = RedisConfigManager(
    logger=logger,
)

BASE_URL = os.getenv("BASE_URL")

port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 3000

# Open a ngrok tunnel to the dev server
logger.info('ngrok tunnel "{}" -> "http://127.0.0.1:{}"'.format(BASE_URL, port))


if not BASE_URL:
    raise ValueError("BASE_URL must be set in environment")

telephony_server = TelephonyServer(
    base_url=BASE_URL,
    config_manager=config_manager,
    logger=logger,
    agent_factory=MyAgentFactory()
)

app.include_router(telephony_server.get_router())

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=port)