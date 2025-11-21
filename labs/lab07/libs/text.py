def normalize(text: str, casefold: bool = True, yo2e: bool = False) -> str:
    """
    Нормализует текст:
      - убирает лишние пробелы,
      - при необходимости приводит к нижнему регистру (`casefold=True`),
      - при необходимости заменяет 'ё' → 'е' (`yo2e=True`).

    Args:
        text (str): Исходная строка.
        casefold (bool, optional): Приводить ли текст к нижнему регистру. По умолчанию True.
        yo2e (bool, optional): Заменять ли 'ё' и 'Ё' на 'е' и 'Е'. По умолчанию False.

    Returns:
        str: Нормализованная строка.
    """
    import re

    text = re.sub(r"\s+", " ", text).strip()
    text = text.replace("ё", "е").replace("Ё", "Е") if yo2e else text
    return text.casefold() if casefold else text


def tokenize(text: str) -> list[str]:
    """
    Разбивает текст на токены (слова).

    Использует регулярное выражение, чтобы выделить слова, включая составные с дефисом
    (например, «научно-технический» будет одним токеном).

    Args:
        text (str): Исходный текст.

    Returns:
        list[str]: Список токенов (слов).
    """
    import re

    return re.findall(r"\w+(?:-\w+)*", text)


def count_freq(tokens: list[str]) -> dict[str, int]:
    """
    Подсчитывает частоту встречаемости каждого слова в списке токенов.

    Args:
        tokens (list[str]): Список токенов (слов).

    Returns:
        dict[str, int]: Словарь, где ключ — слово, значение — количество его вхождений.
    """
    return {word: tokens.count(word) for word in set(tokens)}


def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    """
    Возвращает N самых частотных слов.

    Сначала сортирует слова по убыванию частоты, затем — по алфавиту при равной частоте.

    Args:
        freq (dict[str, int]): Словарь частот слов.
        n (int, optional): Сколько слов вернуть. По умолчанию 5.

    Returns:
        list[tuple[str, int]]: Список кортежей (слово, частота), отсортированный по убыванию частоты.
    """
    return sorted(freq.items(), key=lambda item: (-item[1], item[0]))[:n]
