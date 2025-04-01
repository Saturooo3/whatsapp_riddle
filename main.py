import os
from dotenv import load_dotenv
from twilio_tool import TwilioTool
from openai_tool import (OpenAITool, RiddleResponse)

# Laden der Umgebungsvariablen
load_dotenv()

# Twilio-Konfiguration
ACC_SID = os.getenv("ACCOUNT_SID")
API_KEY = os.getenv("API_KEY_SID")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
SVC_ID = os.getenv("SERVICE_SID")
MASTERSHOOL_NUM = dotenv.load_dotenv("MASTERSHOOL_NUMBER")
PERSONAL_NUM = dotenv.load_dotenv("PERSONAL_NUMBER")

twilio_client = TwilioTool(SVC_ID)
openai_client = OpenAITool()

api_key = API_KEY
api_secret = API_KEY_SECRET
account_sid = ACC_SID
# twilio_client = Client(api_key, api_secret, account_sid)                          #unnecessary?
# service = twilio_client.conversations.v1.services(SVC_ID)                          #unnecessary?


# Initialisierung des Twilio-Clients
# twilio_client = Client(API_KEY, API_KEY_SECRET, ACC_SID)                          #unnecessary?



def display_greeting():
    text = (
    """
    Welcome to the game!
    The rules are simple:
    1. Choose the type and the difficulty of the riddle.
    2. Answer the riddle or ask for "hint".
    3. If the answer is wrong you get a hint.
    4. Enjoy the game and don't forget to invite your friends to compete with them.
    """
    )
    print(text)


def get_number_and_name():
    number = input("Enter your number: ")
    name = input("Enter your name: ")
    return number, name

def get_riddle_format():
    riddle_type = input("Choose riddle type (e.g., logic, math, word): ")
    riddle_difficulty = input("Choose difficulty (easy, medium, hard): ")
    return riddle_type, riddle_difficulty

def check_answer_and_give_feedback(answer, riddle_data, conversation):
    if answer == riddle_data["answer"].strip().lower():
        TwilioTool.send_message(conversation, "Correct!")
    else:
        TwilioTool.send_message(conversation,
                                f"Wrong! Here's a hint: {riddle_data["hint"]}")
        answer = input("Try again! ").strip().lower()
        if answer == riddle_data["answer"].strip().lower():
            TwilioTool.send_message(conversation, "Correct!")
        else:
            TwilioTool.send_message(conversation,
                                    f"Wrong! The correct answer was: {riddle_data["answer"]}")


def main():
    display_greeting()
    my_number, my_name = get_number_and_name()
    my_number = PERSONAL_NUM                                                            #delete after tests

    conversation = twilio_client.get_conversation(my_number)
    if not conversation:
        conversation = twilio_client.create_conversation(my_name)
        twilio_client.create_participant(conversation)

    continue_game = True
    while continue_game:
        riddle_type, riddle_difficulty = get_riddle_format()
        riddle_data = OpenAITool.get_structured_answer(riddle_type=riddle_type, riddle_difficulty=riddle_difficulty, format=RiddleResponse, messages=)

        TwilioTool.send_message(conversation, riddle_data["riddle"])

        user_answer = input("Your answer: ").strip().lower()
        check_answer_and_give_feedback(user_answer, riddle_data, conversation)

        ask_to_continue = input("Do you want another riddle? (yes/no): ").strip().lower()
        if ask_to_continue != "yes":
            continue_game = False
            TwilioTool.send_message(conversation, "See you next time!")


if __name__ == "__main__":
    main()
