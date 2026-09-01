"""
Forest Hangman
==============
A colourful, nature-themed hangman game for the terminal.

Guess nature vocabulary words (animals, plants, geography terms) one
letter at a time before you run out of attempts. Each word comes with
a short definition -- revealed as a hint, or at the end of the round --
so you build vocabulary while you play.

Run:
    python hangman.py

Optional (for coloured output):
    pip install colorama
"""

import random
import sys

# ---------------------------------------------------------------------------
# Optional colour support -- falls back gracefully if colorama isn't installed
# ---------------------------------------------------------------------------
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLOR_ENABLED = True
except ImportError:
    COLOR_ENABLED = False

    class _NoColor:
        def __getattr__(self, _name):
            return ""

    Fore = _NoColor()
    Style = _NoColor()


# ---------------------------------------------------------------------------
# Word bank -- category name -> {word: definition}
# ---------------------------------------------------------------------------
WORD_BANK = {
    "Forest Animals": {
        "wolverine": "A fierce, solitary mammal known for its strength relative to its size.",
        "salamander": "An amphibian that can regenerate lost limbs.",
        "peregrine": "A falcon considered the fastest animal on Earth in a hunting dive.",
        "porcupine": "A rodent covered in sharp, defensive quills.",
        "chameleon": "A reptile famous for changing colour to match its surroundings.",
    },
    "Plants & Trees": {
        "mangrove": "A tree that grows in coastal, salty or brackish water.",
        "eucalyptus": "A fast-growing, aromatic tree favoured by koalas.",
        "sequoia": "A giant coniferous tree, among the tallest living things on Earth.",
        "orchid": "A flower prized for its delicate, intricate petals.",
        "bamboo": "A fast-growing woody grass used for building and food.",
    },
    "Geography & Nature": {
        "glacier": "A slow-moving mass of ice formed from compacted snow.",
        "canyon": "A deep gorge, usually carved by a river over time.",
        "tundra": "A vast, treeless Arctic region with permanently frozen subsoil.",
        "savanna": "A grassy plain scattered with trees, typical of the tropics.",
        "estuary": "The area where a river meets the sea and fresh water mixes with salt.",
    },
}

MAX_WRONG = 6

STAGES = [
    """
     ------
     |    |
     |
     |
     |
     |
    -------""",
    """
     ------
     |    |
     |    O
     |
     |
     |
    -------""",
    """
     ------
     |    |
     |    O
     |    |
     |
     |
    -------""",
    """
     ------
     |    |
     |    O
     |   /|
     |
     |
    -------""",
    """
     ------
     |    |
     |    O
     |   /|\\
     |
     |
    -------""",
    """
     ------
     |    |
     |    O
     |   /|\\
     |   /
     |
    -------""",
    """
     ------
     |    |
     |    O
     |   /|\\
     |   / \\
     |
    -------""",
]


def stage_color(wrong_count: int) -> str:
    """Green when safe, yellow when risky, red when almost hanged."""
    if wrong_count <= 1:
        return Fore.GREEN
    if wrong_count <= 3:
        return Fore.YELLOW
    return Fore.RED


def print_banner() -> None:
    print(Fore.GREEN + Style.BRIGHT + "=" * 48)
    print(Fore.GREEN + Style.BRIGHT + "   FOREST HANGMAN -- Grow Your Vocabulary")
    print(Fore.GREEN + Style.BRIGHT + "=" * 48 + "\n")


def choose_category() -> str:
    categories = list(WORD_BANK.keys())
    print(Fore.CYAN + "Choose a word category:")
    for i, cat in enumerate(categories, start=1):
        print(f"  {i}. {cat}")
    print(f"  {len(categories) + 1}. Surprise me (random mix)")

    while True:
        choice = input(Fore.CYAN + "\nEnter a number: " + Style.RESET_ALL).strip()
        if choice.isdigit():
            choice_num = int(choice)
            if 1 <= choice_num <= len(categories):
                return categories[choice_num - 1]
            if choice_num == len(categories) + 1:
                return random.choice(categories)
        print(Fore.RED + "Please enter a valid option.")


def pick_word(category: str) -> tuple[str, str]:
    word, hint = random.choice(list(WORD_BANK[category].items()))
    return word.lower(), hint


def render_word(word: str, guessed_letters: set[str]) -> str:
    return " ".join(
        (Fore.GREEN + letter + Style.RESET_ALL) if letter in guessed_letters else "_"
        for letter in word
    )


def get_guess(guessed_letters: set[str], hint_used: bool) -> str:
    while True:
        raw = input(
            Fore.CYAN + "\nGuess a letter (or type 'hint'): " + Style.RESET_ALL
        ).strip().lower()

        if raw == "hint":
            if hint_used:
                print(Fore.YELLOW + "You've already used your hint for this word.")
                continue
            return "hint"

        if len(raw) != 1 or not raw.isalpha():
            print(Fore.RED + "Please enter a single letter.")
            continue

        if raw in guessed_letters:
            print(Fore.YELLOW + f"You already guessed '{raw}'. Try another letter.")
            continue

        return raw


def play_round(category: str) -> bool:
    word, hint = pick_word(category)
    guessed_letters: set[str] = set()
    wrong_count = 0
    hint_used = False

    while wrong_count < MAX_WRONG and set(word) - guessed_letters:
        print(stage_color(wrong_count) + STAGES[wrong_count])
        print(f"\nCategory: {category}")
        print("Word: " + render_word(word, guessed_letters))
        print(f"Wrong guesses: {wrong_count}/{MAX_WRONG}")
        if guessed_letters:
            wrong_letters = sorted(guessed_letters - set(word))
            if wrong_letters:
                print(Fore.RED + "Wrong letters: " + ", ".join(wrong_letters))

        guess = get_guess(guessed_letters, hint_used)

        if guess == "hint":
            print(Fore.MAGENTA + f"Hint: {hint}")
            hint_used = True
            continue

        guessed_letters.add(guess)

        if guess in word:
            print(Fore.GREEN + f"Nice! '{guess}' is in the word.")
        else:
            wrong_count += 1
            print(Fore.RED + f"'{guess}' is not in the word.")

    won = not (set(word) - guessed_letters)

    print(stage_color(wrong_count) + STAGES[wrong_count])
    if won:
        print(Fore.GREEN + Style.BRIGHT + f"\nYou got it! The word was '{word}'.")
    else:
        print(Fore.RED + Style.BRIGHT + f"\nOut of attempts! The word was '{word}'.")
    print(Fore.MAGENTA + f"Definition: {hint}")

    return won


def main() -> None:
    print_banner()
    if not COLOR_ENABLED:
        print("(Tip: run 'pip install colorama' for a colourful terminal experience.)\n")

    wins = 0
    losses = 0

    while True:
        category = choose_category()
        won = play_round(category)
        if won:
            wins += 1
        else:
            losses += 1

        print(Fore.CYAN + f"\nScore -- Wins: {wins}  Losses: {losses}")

        again = input(Fore.CYAN + "\nPlay again? (y/n): " + Style.RESET_ALL).strip().lower()
        if again != "y":
            print(Fore.GREEN + "\nThanks for playing Forest Hangman. See you next time!")
            sys.exit(0)


if __name__ == "__main__":
    main()