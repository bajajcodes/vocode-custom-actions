from typing import Optional, Type
from pydantic import BaseModel, Field
import os
from vocode.streaming.action.base_action import BaseAction
from vocode.streaming.models.actions import (
    ActionConfig,
    ActionInput,
    ActionOutput,
    ActionType,
)


class NylasSendEmailActionConfig(ActionConfig, type=ActionType.NYLAS_SEND_EMAIL):
    pass


class NylasSendEmailParameters(BaseModel):
    to: str = Field(..., description="The mobile number of the recipient.")
    body: str = Field(..., description="The body of the sms.")


class NylasSendEmailResponse(BaseModel):
    success: bool


class NylasSendEmail(
    BaseAction[
        NylasSendEmailActionConfig, NylasSendEmailParameters, NylasSendEmailResponse
    ]
):
    description: str = "Sends an sms."
    parameters_type: Type[NylasSendEmailParameters] = NylasSendEmailParameters
    response_type: Type[NylasSendEmailResponse] = NylasSendEmailResponse

    async def run(
        self, action_input: ActionInput[NylasSendEmailParameters]
    ) -> ActionOutput[NylasSendEmailResponse]:
        from twilio.rest import Client

        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')  
        from_number = os.getenv("TWILIO_FROM_NUMBER")
        
#         # Initialize the Nylas client      
        client = Client(account_sid, auth_token)
        print("twilio recepient_to_number:{} sms_body:{}".format(action_input.params.to, action_input.params.body))

#         # Send the sms
        message = client.messages.create(from_=from_number,body=action_input.params.body, to="+91{}".format(action_input.params.to))
        print("sms_sid: {} date_created{} date_sent{}".format(message.sid, message.date_created, message.date_sent))

        return ActionOutput(
            action_type=self.action_config.type,
            response=NylasSendEmailResponse(success=True),
        )
