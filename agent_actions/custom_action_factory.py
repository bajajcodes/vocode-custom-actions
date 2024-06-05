from vocode.streaming.models.actions import ActionConfig
from vocode.streaming.action.base_action import BaseAction
from .twilio_send_sms import TwilioSendSmsActionConfig, TwilioSendSms
from .sendgrid_send_email import SendGridSendEmailActionConfig, SendGridSendEmail

class MyActionFactory:
  def create_action(self, action_config: ActionConfig) -> BaseAction:
      print("create_action.action_config {}".format(action_config))
      if isinstance(action_config, TwilioSendSmsActionConfig):
         return TwilioSendSms(action_config=action_config, should_respond=True)
      if (isinstance(action_config, SendGridSendEmailActionConfig)):
         return SendGridSendEmail(action_config=action_config, should_respond=True)
      else:
         raise Exception("Invalid custom action type")
