from enum import Enum


class MyActionType(str, Enum):
    TWILIO_SEND_SMS = "twilio_send_sms"
    SENDGRID_SEND_EMAIL = "sendgrid_send_email"
    RESEND_SEND_EMAIL = "resend_send_email"


class MyAgentType(str, Enum):
    CHAT_GPT = "agent_chat_gpt"
    MY_CHAT_GPT = "my_agent_chat_gpt"
