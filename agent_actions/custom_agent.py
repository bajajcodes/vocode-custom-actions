import logging
from typing import  Optional
from .custom_action_factory import MyActionFactory
from .custom_models import MyAgentType
from vocode.streaming.models.agent import ChatGPTAgentConfig, AgentType
from vocode.streaming.agent.chat_gpt_agent import ChatGPTAgent


class MyChatGPTAgentConfig(ChatGPTAgentConfig, type=MyAgentType.MY_CHAT_GPT.value):
  pass

class MyChatGPTAgent(ChatGPTAgent):
  def __init__(self, agent_config: MyChatGPTAgentConfig,  action_factory: MyActionFactory = MyActionFactory(), logger: Optional[logging.Logger] = None,):
    super().__init__(agent_config, action_factory=action_factory, logger=logger)

