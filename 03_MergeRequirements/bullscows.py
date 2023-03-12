import random

def bullscows(guess: str, secret: str):
    if len(guess) != len(secret):
        print("Error: different sizes of guess and secret")
        return (-1, -1)
    bulls, cows = 0, 0
    for i, c in enumerate(guess):
        if c == secret[i]:
            bulls += 1
        elif c in secret:
            cows += 1
    return bulls, cows

def gameplay(ask: callable, inform: callable, words: list[str]):
    word = random.choice(words)
    ask_cnt = 0
    guess = ""
    while guess != word:
        guess = ask("Введите слово: ", words)
        ask_cnt += 1
        bulls, cows = bullscows(guess, word)
        inform("Быки: {}, Коровы: {}", bulls, cows)
    print('Слово угадано, число попыток: {}'.format(ask_cnt))
    return word

def ask(prompt: str, valid: list[str] = None):
    print(prompt)
    guess = input()
    if valid is not None:
        if guess not in valid:
            print('Такого слова нет в списке валидных')
    return guess

def inform(format_string: str, bulls: int, cows: int):
    print(format_string.format(bulls, cows))

print(bullscows("ропот", "полип"))
print(gameplay(ask, inform, ["ропот", "полип"]))