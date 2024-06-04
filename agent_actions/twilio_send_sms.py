import os
import logging
from typing import Type
from pydantic import BaseModel, Field
from vocode.streaming.action.base_action import BaseAction
from vocode.streaming.models.actions import (
    ActionConfig,
    ActionInput,
    ActionOutput,
)
from .custom_models import MyActionType


class TwilioSendSmsActionConfig(ActionConfig, type=MyActionType.TWILIO_SEND_SMS):
    pass


class TwilioSendSmsParameters(BaseModel):
    to: str = Field(..., description="The mobile number of the recipient.")
    body: str = Field(..., description="The body of the sms.")


class TwilioSendSmsResponse(BaseModel):
    success: bool
    message: str


class TwilioSendSms(
    BaseAction[
        TwilioSendSmsActionConfig, TwilioSendSmsParameters, TwilioSendSmsResponse
    ]
):
    description: str = "Sends an sms."
    parameters_type: Type[TwilioSendSmsParameters] = TwilioSendSmsParameters
    response_type: Type[TwilioSendSmsResponse] = TwilioSendSmsResponse

    async def run(
        self, action_input: ActionInput[TwilioSendSmsParameters]
    ) -> ActionOutput[TwilioSendSmsResponse]:
        from twilio.rest import Client

        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')  
        from_number = os.getenv("TWILIO_FROM_NUMBER")

        try:
            # Initialize the Nylas client      
            client = Client(account_sid, auth_token)
            logging.info(f"Sending SMS to: {action_input.params.to}, Body: {action_input.params.body}")

            # Send the sms
            message = client.messages.create(from_=from_number,body=action_input.params.body, to="+91{}".format(action_input.params.to))
            logging.info(f"SMS sent successfully. SID: {message.sid}")

            return ActionOutput(action_type=self.action_config.type, response=TwilioSendSmsResponse(success=True, message="Successfully sent SMS."))
        
# TODO: replace bare exception with specific exception
        except RuntimeError as e:
            logging.error(f"Failed to send SMS: {e}")
            return ActionOutput(action_type=self.action_config.type, response=TwilioSendSmsResponse(success=False, message="Failed to send SMS"))
