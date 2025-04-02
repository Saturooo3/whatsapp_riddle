import os
from dotenv import load_dotenv
from twilio_tool import TwilioTool
from openai_tool import OpenAITool
from whatsapp_riddle_executers import (Riddle, UserGuessAnalysis)
from rich import console

twilio_client = TwilioTool()
openai_client = OpenAITool()

console = console.Console()

def display_greeting():
    text = (
    """
    Welcome to the game!
    The rules are simple:
    1. Choose the type of the riddle.
    2. Answer the riddle or ask for "hint".
    3. If the answer is wrong you get a hint.
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
        else:
            respond_wrong_answer = (
                f"Wrong answer, but here you get a hint: "
                f"{user_guess_analysis.hint}")

            twilio_client.create_message(conversation, respond_wrong_answer)

            messages.append(
                {"role": "assistant", "content": user_guess_analysis.hint})

def load_or_create_conversation(my_name):
    conversation = twilio_client.get_conversation()
    if not conversation:
        console.print("No conversation found, creating new one",
                      style="bold blue")
        conversation = twilio_client.create_conversation(my_name)
        twilio_client.create_participant(conversation)
        console.print("Created new conversation and participant",
                      style="bold blue")

    return conversation


def main():

    console.print("Starting game!", style="bold green")
    my_name = "Yusuf"

    console.print(f"Getting conversation for {twilio_client.my_number}", style="bold blue")
    conversation = load_or_create_conversation(my_name)
    console.print("Got conversation from twilio", style="bold blue")

    greeting = display_greeting()
    twilio_client.create_message(conversation=conversation, message=greeting)
    console.print("Displayed greeting", style="bold blue")

    continue_game = True
    console.print("Entering main loop", style="bold blue")
    while continue_game:
        riddle_type = get_riddle_type(conversation)

        messages = [
            {"role": "system",
             "content": "You are my assistant to give me riddles to solve, and give me hints, when I'm stuck."},
            {"role": "user",
             "content": f"Create a riddle for me to solve with the type {riddle_type}"}
        ]

        riddle_response: Riddle = openai_client.structured_answer(messages=messages, model=Riddle)
        twilio_client.create_message(conversation,riddle_response.content)

        messages.append(
            {"role": "assistant", "content": riddle_response.content})

        check_answer_and_give_feedback(conversation, messages)



if __name__ == "__main__":
    main()
