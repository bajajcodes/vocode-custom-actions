import os

from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from vocode.streaming.models.agent import CutOffResponse
from vocode.streaming.models.message import BaseMessage
from vocode.streaming.models.synthesizer import AzureSynthesizerConfig
from vocode.streaming.models.telephony import TwilioConfig
from vocode.streaming.models.transcriber import (DeepgramTranscriberConfig,
                                                 TimeEndpointingConfig)
from vocode.streaming.models.vector_db import PineconeConfig
from vocode.streaming.telephony.config_manager.redis_config_manager import \
    RedisConfigManager
from vocode.streaming.telephony.conversation.outbound_call import OutboundCall

from agent_actions.custom_agent import MyChatGPTAgentConfig
from agent_actions.sendgrid_send_email import SendGridSendEmailActionConfig
from agent_actions.twilio_send_sms import TwilioSendSmsActionConfig
from prompt import (SALES_CALL_PROMPT, SENDS_AN_EMAIL_PROMPT,
                    SENDS_AN_SMS_PROMPT, VOICE_AI_ACTIONS_PROMPT)

load_dotenv()

BASE_URL = os.environ["BASE_URL"]
TWILIO_FROM_NUMBER=os.environ["TWILIO_FROM_NUMBER"]
TWILIO_TO_NUMBER=os.environ["TWILIO_TO_NUMBER"]
TWILIO_ACCOUNT_SID=os.environ["TWILIO_ACCOUNT_SID"] 
TWILIO_AUTH_TOKEN=os.environ["TWILIO_AUTH_TOKEN"] 

# Ensure that the environment variable 'PINECONE_INDEX_NAME' is not None
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")
if pinecone_index_name is None:
    raise ValueError("Environment variable 'PINECONE_INDEX_NAME' is not set.")

vector_db_config = PineconeConfig(index=pinecone_index_name,embeddings_model="text-embedding-3-small")


async def main():
    config_manager = RedisConfigManager()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    outbound_call = OutboundCall(
        base_url=BASE_URL,
        to_phone=TWILIO_TO_NUMBER,
        from_phone=TWILIO_FROM_NUMBER,
        config_manager=config_manager,
        mobile_only=False,
        twilio_config=TwilioConfig(account_sid=TWILIO_ACCOUNT_SID,
            auth_token=TWILIO_AUTH_TOKEN, record=True),
        synthesizer_config=AzureSynthesizerConfig(
            voice_name="en-US-AriaNeural",
            language_code="en-US",
            rate=15,
            pitch=0,
            sampling_rate=8000,
            audio_encoding="mulaw",
        ),
        transcriber_config=DeepgramTranscriberConfig(
            language="en",
            sampling_rate=8000,
            chunk_size=20 * 160,
            audio_encoding="mulaw",
            model="nova-2-conversationalai",
            min_interrupt_confidence=0.9,
            endpointing_config=TimeEndpointingConfig(time_cutoff_seconds=0.6)
        ),
        agent_config=MyChatGPTAgentConfig(
            # send_filler_audio=FillerAudioConfig(use_typing_noise=True),
            initial_message=BaseMessage(text="Hello, I am Nisha."),
            prompt_preamble=SALES_CALL_PROMPT,
            model_name="gpt-4-turbo",
            temperature=0.1,
            generate_responses=True,
            allow_agent_to_be_cut_off=True,
            cut_off_response=CutOffResponse(),
            track_bot_sentiment=True,
            actions=[TwilioSendSmsActionConfig(),SendGridSendEmailActionConfig()],
            allowed_idle_time_seconds=10,
            memory=memory,
            vector_db_config=vector_db_config
        )
    )

    input("Press enter to start call...")
    await outbound_call.start()
    print(outbound_call.conversation_id)
    print(outbound_call.telephony_id)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())