from twilio.rest import Client

class TwilioTool:
    def __init__(self, service_sid: str):
        self.client = Client(api_key, api_secret, account_sid)
        self.service = self.client.conversations.v1.services(serivce_sid)


    def send_whatsapp_message(self, to_whatsapp: str, body: str) -> str:
        from_whatsapp = "whatsapp:+493041736523"
        if not to_whatsapp.startswith("whatsapp:"):
            to_whatsapp = "whatsapp:" + to_whatsapp
        message = self.client.messages.create(
            from_=from_whatsapp,
            body=body,
            to=to_whatsapp
        )
        return message.sid

    def create_conversation(self):
        conversation = self.service.conversations.create()
        return conversation

    def get_my_conversation(self):
        for conversation in self.service.conversations.list():
            for participant in conversation.participants.list():
                if participant.messaging_binding["address"] == PERSONAL_NUM:
                    return conversation

        return None

    def create_participant(self, conversation):
        participant = (
            self.client.conversations.v1.services(SVC_ID)
            .conversations(conversation.sid)
            .participants.create(
                messaging_binding_address=PERSONAL_NUM,
                messaging_binding_proxy_address=MASTERSHOOL_NUM
            )
        )
        return participant

    def create_message(self, conversation, message: str):
        self.client.conversations.v1.services(SVC_ID) \
            .conversations(conversation.sid) \
            .messages.create(
            author=MASTERSHOOL_NUM,
            body=message
        )