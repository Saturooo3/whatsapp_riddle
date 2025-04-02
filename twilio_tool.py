from twilio.rest import Client
from dotenv import load_dotenv
import os
from time import sleep

load_dotenv()

API_KEY : str = os.getenv("API_KEY")
API_KEY_SECRET: str  = os.getenv("API_KEY_SECRET")
ACC_SID: str  = os.getenv("ACC_SID")
SVC_ID: str  = os.getenv("SVC_ID")
PERSONAL_NUM: str  = os.getenv("PERSONAL_NUM")
MASTERSHOOL_NUM: str  = os.getenv("MASTERSHOOL_NUM")

load_dotenv()


class TwilioTool:
    def __init__(self):
        self.client = Client(API_KEY, API_KEY_SECRET, ACC_SID)
        self.service = self.client.conversations.v1.services(SVC_ID)


    def create_conversation(self, name):
        """
        gets name for conversation and creates a new conversation
        """
        name_str = f"Chat with {name}"
        conversation = self.service.conversations.create(friendly_name=name_str)
        return conversation


    def create_participant(self, conversation, my_number):
        """
        gets a conversation and adds participant to the conversation
        """
        participant = (
            self.service.conversations(conversation.sid)
                .participants.create(
                messaging_binding_address=my_number,
                messaging_binding_proxy_address=MASTERSHOOL_NUM
            )
        )
        return participant


    def get_participant(self, conversation, my_number):
        """
        gets a number and returns participant if already exists,
        returns None if not
        """
        participants = (self.service.conversations(conversation.sid)
                        .participants.list())
        for participant in participants:
            if participant.messaging_binding.get("address") == my_number:
                return participant
        return None


    def get_conversation(self, my_number):
        """
        gets number and returns conversation if exists, if not returns None
        """
        for conversation in self.service.conversations.list():
            participants = self.service.conversations(
                conversation.sid).participants.list()
            for participant in participants:
                if participant.messaging_binding.get("address") == my_number:
                    return conversation
        return None


    def create_message(self, conversation, message: str):
        """
        gets conversation and message as string and sends message to conversation
        """
        message=self.service.conversations(conversation.sid).messages.create(
            author=MASTERSHOOL_NUM,
            body=message
        )
        return message.sid

    def send_whatsapp_message(self, to_whatsapp: str, body: str) -> str:
        from_whatsapp = MASTERSHOOL_NUM
        if not to_whatsapp.startswith("whatsapp:"):
            to_whatsapp = "whatsapp:" + to_whatsapp
        message = self.client.messages.create(
            from_=from_whatsapp,
            body=body,
            to=to_whatsapp
        )

        return message.sid

    def get_messages(self, conversation):

        messages = (
        self.service.conversations(conversation.sid).messages.list()
        )
        return messages


    def get_last_message_from_user(self, conversation, my_number):
        while True:
            messages = self.get_messages(conversation)
            if not messages:
                sleep(1)
                continue
            last_message = messages[-1]
            if last_message.author != my_number:
                sleep(1)
                continue
            else:
                return last_message.body
