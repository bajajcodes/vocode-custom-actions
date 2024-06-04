import os
from typing import Type
from pydantic import BaseModel, Field
from vocode.streaming.action.base_action import BaseAction
from vocode.streaming.models.actions import (
  ActionConfig,
  ActionInput,
  ActionOutput
)
from .custom_models import MyActionType

class SendGridSendEmailActionConfig(ActionConfig, type=MyActionType.SENDGRID_SEND_EMAIL):
  pass

class SendGridSendEmailParameters(BaseModel):
  subject: str = Field(..., description="The subject of the email")
  body: str = Field(..., description="The body of the email")

class SendGridSendEmailResponse(BaseModel):
  success: bool

class SendGridSendEmail(BaseAction(SendGridSendEmailActionConfig, SendGridSendEmailParameters, SendGridSendEmailResponse)):
  description: str = "Sends an email"
  parmeters_type: Type[SendGridSendEmailParameters] = SendGridSendEmailParameters
  response_type: Type[SendGridSendEmailResponse] = SendGridSendEmailResponse

  async def run(self, action_input: ActionInput[SendGridSendEmailParameters], response_type: Type[SendGridSendEmailResponse] = SendGridSendEmailResponse):
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail

    message = Mail(from_email="", to_emails="", subject=action_input.params.subject, html_content=action_input.params.body)
    
    sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
    response = sg.send(message)

    print("SendGrid Send Email status_code:{} body:{} headers:{}".format(response.status_code, response.body, response.headers))

    return ActionOutput(action_type=self.action_config.type, response=SendGridSendEmailResponse(success=True))
    

