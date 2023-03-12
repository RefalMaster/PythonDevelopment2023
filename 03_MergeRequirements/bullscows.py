import random
import argparse
from urllib import request
from collections import Counter

def bullscows(guess: str, secret: str):
    if len(guess) != len(secret):
        print("Error: different sizes of guess and secret")
        return (-1, -1)
    bulls = [g == s for g, s in zip(guess, secret)]
    cows = Counter(guess) & Counter(secret)
    return sum(bulls), sum(cows.values())

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

parser = argparse.ArgumentParser()
parser.add_argument("dictionary", type=str)
parser.add_argument("length", nargs='?', default=5, type=int)

args = parser.parse_args()

if ":" not in args.dictionary:
    with open(args.dictionary) as file:
        words = file.read().split()
        words = [i for i in words if len(i) == args.length]
else:
    words = request.urlopen(args.dictionary).read()
    words = words.decode().split()
    words = [i for i in words if len(i) == args.length]

gameplay(ask, inform, words)