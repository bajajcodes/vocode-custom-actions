import logging
from typing import Optional, cast

from vocode.streaming.agent.base_agent import BaseAgent
from vocode.streaming.agent.chat_gpt_agent import ChatGPTAgent
from vocode.streaming.models.agent import AgentConfig, ChatGPTAgentConfig

from .custom_agent import MyChatGPTAgent, MyChatGPTAgentConfig


class MyAgentFactory:
    def create_agent(
        self, agent_config: AgentConfig, logger: Optional[logging.Logger] = None
    ) -> BaseAgent:
        print("agent_config.type: {}".format(agent_config.type))
        if isinstance(agent_config, MyChatGPTAgentConfig):
            return MyChatGPTAgent(agent_config=agent_config, logger=logger)
        elif isinstance(agent_config, ChatGPTAgentConfig):
            return ChatGPTAgent(
                agent_config=cast(ChatGPTAgentConfig, agent_config), logger=logger
            )
        else:
            raise Exception("Invalid custom agent config", agent_config.type)
