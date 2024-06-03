import os
from dotenv import load_dotenv

load_dotenv()

from vocode.streaming.telephony.conversation.outbound_call import OutboundCall
from vocode.streaming.telephony.config_manager.redis_config_manager import RedisConfigManager
from langchain.memory import ConversationBufferMemory
from vocode.streaming.models.agent import ChatGPTAgentConfig
from vocode.streaming.models.synthesizer import AzureSynthesizerConfig
from vocode.streaming.models.telephony import TwilioConfig
from vocode.streaming.models.transcriber import DeepgramTranscriberConfig
from vocode.streaming.models.message import BaseMessage
from vocode.streaming.models.agent import FillerAudioConfig
from prompt import SENDS_AN_SMS_PROMPT
from vocode.streaming.action.nylas_send_email import NylasSendEmailActionConfig
from agent_actions.custom_agent import MyChatGPTAgentConfig
from agent_actions.twilio_send_sms import TwilioSendSmsActionConfig


BASE_URL = os.environ["BASE_URL"]
TWILIO_FROM_NUMBER=os.environ["TWILIO_FROM_NUMBER"]
TWILIO_TO_NUMBER=os.environ["TWILIO_TO_NUMBER"]
TWILIO_ACCOUNT_SID=os.environ["TWILIO_ACCOUNT_SID"] 
TWILIO_AUTH_TOKEN=os.environ["TWILIO_AUTH_TOKEN"] 


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
            min_interrupt_confidence=1,
        ),
        agent_config=MyChatGPTAgentConfig(
            send_filler_audio=FillerAudioConfig(use_typing_noise=True),
            initial_message=BaseMessage(text="Hello?"),
            prompt_preamble=SENDS_AN_SMS_PROMPT,
            model_name="gpt-4-turbo",
            temperature=0.1,
            generate_responses=True,
            allow_agent_to_be_cut_off=True,
            track_bot_sentiment=True,
            actions=[TwilioSendSmsActionConfig()],
            allowed_idle_time_seconds=5,
            memory=memory,
        )
    )

    input("Press enter to start call...")
    await outbound_call.start()
    print(outbound_call.conversation_id)
    print(outbound_call.telephony_id)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())