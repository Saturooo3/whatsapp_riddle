import os
from dotenv import load_dotenv
from twilio_tool import TwilioTool
from openai_tool import OpenAITool
from whatsapp_riddle_executers import (Riddle, UserGuessAnalysis)
from rich import console
import json

twilio_client = TwilioTool()
openai_client = OpenAITool()

console = console.Console()

def display_greeting():
    text = (
    """
    Welcome to the game!\n
    The rules are simple:\n
    1. Choose the type of the riddle.
    2. Answer the riddle, ask for "hint".
    3. If the answer is wrong, I will give you a hint.
    4. If you want a new riddle or you want to give up, just tell me...
    4. Enjoy the game and don't forget to invite your friends to compete with them.
    """
    )
    return text


def get_number_and_name():
    number = "whatsapp:",input("Enter your number(+49....): ")
    name = input("Enter your name: ")
    return number, name


def get_riddle_type(conversation):
    ask_riddle_type = "Choose riddle type (e.g., logic, math, word): "
    twilio_client.create_message(conversation, message=ask_riddle_type)
    riddle_type = twilio_client.get_last_message_from_user(conversation)
    return riddle_type


def check_answer_and_give_feedback(conversation, messages):
    while True:
        new_message = twilio_client.get_last_message_from_user(conversation)
        messages.append({"role": "user", "content": new_message})
        user_guess_analysis: UserGuessAnalysis = openai_client.structured_answer(
            messages, UserGuessAnalysis)

        if user_guess_analysis.is_correct:
            twilio_client.create_message(conversation, "You did it!")
            break
        elif user_guess_analysis.is_giving_up:
            twilio_client.create_message(conversation, f"Shame on you. You gave up!\nThe answer was: {user_guess_analysis.answer}")
            break
        elif user_guess_analysis.is_asking_for_hint:
            twilio_client.create_message(conversation, user_guess_analysis.hint)
        else:
            respond_wrong_answer = (
                f"Wrong answer, but here you get a hint:\n"
                f"{user_guess_analysis.hint}")

            twilio_client.create_message(conversation, respond_wrong_answer)

            messages.append(
                {"role": "assistant", "content": user_guess_analysis.hint})

def load_or_create_conversation():
    conversation = twilio_client.get_conversation()
    if not conversation:
        console.print("No conversation found, creating new one",
                      style="bold blue")
        conversation = twilio_client.create_conversation()
        twilio_client.create_participant(conversation)
        console.print("Created new conversation and participant",
                      style="bold blue")

    return conversation

def initialize_messages(riddle_type, asked_riddles):
    initialization_message = (f"Create a new riddle for me, that is not in the list "
                              f"{asked_riddles}. It should be riddle from type {riddle_type}")
    messages = [
            {"role": "system",
             "content": "You are my assistant to give me riddles to solve, and give me hints, when I'm stuck."},
            {"role": "user",
             "content": initialization_message }
        ]

    return messages

def read_asked_riddles_from_json():
    try:
        with open("asked_riddles.json", "r") as f:
            data = json.loads(f.read())
        return data
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def write_asked_riddles_to_json(asked_riddles):
    with open("asked_riddles.json", "w") as f:
        f.write(json.dumps(asked_riddles))


def main():
    console.print("Starting game!", style="bold green")

    console.print(f"Getting conversation for {twilio_client.my_number}", style="bold blue")
    conversation = load_or_create_conversation()
    console.print("Got conversation from twilio", style="bold blue")

    greeting = display_greeting()
    twilio_client.create_message(conversation=conversation, message=greeting)
    console.print("Displayed greeting", style="bold blue")

    continue_game = True
    console.print("Entering main loop", style="bold blue")
    while continue_game:
        riddle_type = get_riddle_type(conversation)

        asked_riddles : list = read_asked_riddles_from_json()
        messages = initialize_messages(riddle_type, asked_riddles)

        riddle_response: Riddle = openai_client.structured_answer(messages=messages, model=Riddle)
        twilio_client.create_message(conversation, riddle_response.content)
        console.print(f"Riddle send to player", style="bold blue")
        asked_riddles.append(riddle_response.content)
        write_asked_riddles_to_json(asked_riddles)

        messages.append({"role": "assistant", "content": riddle_response.content})

        check_answer_and_give_feedback(conversation, messages)
        console.print(f"Answer checked", style="bold blue")

if __name__ == "__main__":
    main()
