import os
from lib.text import *
def format(top: list[tuple[str, int]]):
    '''
    Форматирование строки в таблицу
    слово        | частота
    ----------------------
    привет       | 10
    мир          | 7
    ...
    Вход:
    list[tuple(key, val)]
    '''
    length_of_words = max(len(word) for word, _ in top)
    print(f"{'слово':<{length_of_words}} | {'частота'}")
    print('-' * (length_of_words + 12))
    for word, freq in top:
        print(f"{word:<{length_of_words}} | {freq}")

def no_format(top: list[tuple[str, int]]):
    '''
    Вывод списка в формате:
    key: val
    '''
    for val in top:
        print(f"{val[0]}: {val[1]}")

def main():
    isFormated: bool = True if os.getenv('FORMAT') == "TRUE" else False
    tokenized_input: list = tokenize(input())
    print(f"Всего слов: {len(tokenized_input)}")
    freq: dict = count_freq(tokenized_input)
    print(f"Всего уникальных слов: {len([k for k, v in freq.items() if v == 1])}")
    print("Топ-5:")
    format(top_n(freq, 5)) if isFormated else no_format(top_n(freq, 5))
if __name__ == "__main__":
    main()