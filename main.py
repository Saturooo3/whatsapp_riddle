import os
from dotenv import load_dotenv
from twilio_tool import TwilioTool
from openai_tool import OpenAITool

# Laden der Umgebungsvariablen
load_dotenv()

# Twilio-Konfiguration
API_KEY : str = os.getenv("API_KEY_SID")
API_KEY_SECRET: str  = os.getenv("API_KEY_SECRET")
ACC_SID: str  = os.getenv("ACC_SID")
SVC_ID: str  = os.getenv("SVC_ID")
PERSONAL_NUM: str  = os.getenv("PERSONAL_NUM")
MASTERSHOOL_NUM: str  = os.getenv("MASTERSHOOL_NUM")

twilio_client = TwilioTool()
openai_client = OpenAITool()


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

def get_riddle_format(conversation):
    ask_riddle_type = "Choose riddle type (e.g., logic, math, word): "
    TwilioTool.create_message(conversation, message=ask_riddle_type)
    riddle_type = TwilioTool.get_messages(conversation).strip().lower()                  #muss den letzten Eintrag vom participant raussuchen

    ask_riddle_difficulty = "Choose difficulty (easy, medium, hard): "
    TwilioTool.create_message(conversation, message=ask_riddle_difficulty)
    riddle_difficulty = TwilioTool.get_messages(conversation).strip().lower()            #muss den letzten Eintrag vom participant raussuchen

    return riddle_type, riddle_difficulty

def check_answer_and_give_feedback(answer, riddle_data, conversation):
    if answer == riddle_data["answer"].strip().lower():
        TwilioTool.create_message(conversation, "Correct!")
    else:
        response_for_first_wrong_answer =(f"Wrong! Here's a hint: "
                                          f"{riddle_data["hint"]}\nTry again!")

        TwilioTool.create_message(conversation=conversation, message=response_for_first_wrong_answer)
        answer = TwilioTool.get_messages(conversation).strip().lower()                  #muss den letzten Eintrag vom participant raussuchen

        if answer == riddle_data["answer"].strip().lower():
            TwilioTool.create_message(conversation, "Correct!")
        else:
            TwilioTool.create_message(conversation,
                                    f"Wrong! The correct answer was: {riddle_data["answer"]}")


def main():
    display_greeting()
    my_number, my_name = get_number_and_name()

    conversation = twilio_client.get_conversation(my_number)
    if not conversation:
        conversation = twilio_client.create_conversation(my_name)
        twilio_client.create_participant(conversation, my_number)

    continue_game = True
    while continue_game:
        riddle_type, riddle_difficulty = get_riddle_format()
        riddle_data = OpenAITool.structured_answer()
        riddle_text = riddle_data["riddle"],"Your answer: "
        TwilioTool.create_message(conversation, riddle_text)
        user_answer = TwilioTool.get_messages(conversation).strip().lower()         #muss den letzten Eintrag vom participant raussuchen
        check_answer_and_give_feedback(user_answer, riddle_data, conversation)

        ask_to_continue_str ="Do you want another riddle? (yes/no): "
        TwilioTool.create_message(conversation, ask_to_continue_str)

        ask_to_continue = TwilioTool.get_messages(conversation).strip().lower()     #muss den letzten Eintrag vom participant raussuchen

        if ask_to_continue != "yes":
            continue_game = False
            TwilioTool.create_message(conversation, "See you next time!")


if __name__ == "__main__":
    main()
