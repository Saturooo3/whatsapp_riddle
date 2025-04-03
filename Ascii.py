# def print_ascii_greeting():
#     ascii_art = (
#         "\033╔════════════════════════════════════════════════╗\033\n"
#         "\033║     🎮 \033[mWELCOME TO THE RIDDLE GAME!\033🎮        ║\033\n"
#         "\033╚════════════════════════════════════════════════╝\033\n"
#         "\n  📜 \033[The rules are simple:\033\n"
#         "  \033╔════════════════════════════════════════════╗\033\n"
#         "  \033║\033\t1. 🧩 Choose your riddle type             \033║\033\n"
#         "  \033║\033\t2. 🗝️ Answer or cry hint!                 \033║\033\n"
#         "  \033║\033\t3. ❌ Fail? The oracle helps!             \033║\033\n"
#         "  \033║\033\t4. 🔄 Seek a new challenge? Speak!        \033║\033\n"
#         "  \033║\033\t5. 🏆 Glory awaits the persistent!        \033║\033\n"
#         "  \033╚════════════════════════════════════════════╝\033\n"
#     )
#     return ascii_art
# def print_ascii_greeting():
#     ascii_art = (
#         "\033[96m"  # Setze Farbe z. B. Cyan
#         "╔════════════════════════════════════════════════╗\n"
#         "║     🎮  WELCOME TO THE RIDDLE GAME! 🎮        ║\n"
#         "╚════════════════════════════════════════════════╝\n"
#         "\n"
#         "📜  The rules are simple:\n"
#         "╔════════════════════════════════════════════╗\n"
#         "║  1. 🧩 Choose your riddle type             ║\n"
#         "║  2. 🗝️  Answer or cry 'hint!'              ║\n"
#         "║  3. ❌ Fail? The oracle helps!             ║\n"
#         "║  4. 🔄 Seek a new challenge? Speak!        ║\n"
#         "║  5. 🏆 Glory awaits the persistent!        ║\n"
#         "╚════════════════════════════════════════════╝\n"
#         "\033[0m"  # Reset Farbe
#     )
#     print(ascii_art)

def print_ascii_greeting():
    return (
        "🎮 *WELCOME TO THE RIDDLE GAME!* 🎮\n\n"
        "📜 _The rules are simple:_\n"
        "1️⃣ 🧩 Choose your riddle type\n"
        "2️⃣ 🗝️ Answer or cry 'hint!'\n"
        "3️⃣ ❌ Fail? The oracle helps!\n"
        "4️⃣ 🔄 Want a new challenge? Just say so!\n"
        "5️⃣ 🏆 Glory awaits the persistent!"
    )

def print_choose_riddle():
    return (
        "🤔 Choose your riddle type:\n📚 (e.g., math, word)"
    )

def print_win():
    return (
        "🌟═════════════════════🌟\n🎉🎉  YOU DID IT!  🎉🎉\n🌟═════════════════════🌟"
    )

def print_give_up(user_guess_analysis):
    return (
        f"😔 Shame on you. You gave up!\n🧠 The answer was: {user_guess_analysis.answer}"
    )

def print_hint(user_guess_analysis):
    return (
        f"The oracle frowns upon your answer... 🧙‍♂️\n💡But whispers a clue:\n🔍 {user_guess_analysis.hint}"
    )