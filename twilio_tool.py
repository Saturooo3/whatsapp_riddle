from twilio.rest import Client

class TwilioTool:
    def __init__(self, service_sid: str):
        self.client = Client(api_key, api_secret, account_sid)
        self.service = self.client.conversations.v1.services(service_sid)


    def create_conversation(self, name):
        name_str = f"Chat with {name}"
        conversation = self.service.conversations.create(friendly_name=name_str)
        return conversation


    def create_participant(self, conversation):
        participant = (
            self.service.conversations(conversation.sid)
                .participants.create(
                messaging_binding_address=PERSONAL_NUM,
                messaging_binding_proxy_address=MASTERSHOOL_NUM
            )
        )
        return participant


    def get_participant(self, my_number):
        participants = (self.service.conversations(conversation.sid)
                        .participants.list())
        for participant in participants:
            if participant.messaging_binding.address == my_number:
                return participant
        return None


    def get_my_conversation(self, my_number):
        for conversation in self.service.conversations.list():
            for participant in conversation.participants.list():
                if participant.messaging_binding["address"] == my_number:
                    return conversation

        return None


    def send_message(self, conversation, message: str):
        self.serivce.conversations(conversation.sid).messages.create(
            author=MASTERSHOOL_NUM,
            body=message
        )


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