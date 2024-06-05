import os
import logging
from typing import Type
from pydantic import BaseModel, Field
from vocode.streaming.action.base_action import BaseAction
from vocode.streaming.models.actions import (
  ActionConfig,
  ActionInput,
  ActionOutput
)
from .custom_models import MyActionType

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class SendGridSendEmailActionConfig(ActionConfig, type=MyActionType.SENDGRID_SEND_EMAIL):
  pass

class SendGridSendEmailParameters(BaseModel):
    recipient_email: str = Field(..., description="The email address of the recipient.")  
    subject: str = Field(..., description="The subject of the email")
    body: str = Field(..., description="The body of the email")

class SendGridSendEmailResponse(BaseModel):
    success: bool
    message: str

class SendGridSendEmail(
   BaseAction[
      SendGridSendEmailActionConfig, SendGridSendEmailParameters, SendGridSendEmailResponse
      ]):
  description: str = "Sends an email"
  parameters_type: Type[SendGridSendEmailParameters] = SendGridSendEmailParameters
  response_type: Type[SendGridSendEmailResponse] = SendGridSendEmailResponse

  async def run(self, action_input: ActionInput[SendGridSendEmailParameters]) -> ActionOutput[SendGridSendEmailResponse]:
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail

    sendgrid_api_key = os.environ.get("SENDGRID_API_KEY")
    from_email = os.environ.get("SENDGRID_FROM_EMAIL")

    try:
      message = Mail(from_email=from_email, to_emails=action_input.params.recipient_email, subject=action_input.params.subject, html_content=action_input.params.body)
    
      sg = SendGridAPIClient(sendgrid_api_key)
      response = sg.send(message)
      logging.DEBUG(f"Email sent successfully. StatusCode: {response.status_code}")
      return ActionOutput(action_type=self.action_config.type, response=SendGridSendEmailResponse(success=True, message="Successfully sent Email."))

# TODO: replace bare exception with specific exception
    except RuntimeError as e:
      logging.ERROR(f"Failed to send Email: {e}")
      print(f"Failed to send Email: {e}")
      return ActionOutput(action_type=self.action_config.type, response=SendGridSendEmailResponse(success=False, message="Failed to send Email"))
    
    # TODO: make the say message work
  # def _user_message_param_info(self):
  #       return {
  #           "type": "string",
  #           "description": """
  #           Let me send the email using sendgrid for you 
  #           """,
  #       }
  