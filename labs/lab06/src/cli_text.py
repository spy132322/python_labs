"""
CLI для текстовых утилит: cat и stats.

Команды:
  cat --input <path> [-n]
  stats --input <path> [--top N]

Поведение:
  - Все пути должны быть относительными (будет проверено).
  - При ошибках выводится понятное сообщение и код возврата != 0.
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
import re
from typing import Iterable, List


def _ensure_relative(path: Path) -> None:
    if path.is_absolute():
        raise ValueError("Путь должен быть относительным")


def _read_lines(path: Path) -> List[str]:
    _ensure_relative(path)
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")
    return path.read_text(encoding="utf-8").splitlines()


def cmd_cat(path_str: str, number: bool) -> int:
    """
    Вывести содержимое файла построчно.
    Возвращает код выхода (0 при успехе).
    """
    p = Path(path_str)
    try:
        lines = _read_lines(p)
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        return 2
    if number:
        for i, line in enumerate(lines, start=1):
            print(f"{i:6}\t{line}")
    else:
        for line in lines:
            print(line)
    return 0


_WORD_RE = re.compile(r"\b[а-яА-ЯёЁa-zA-Z0-9']+\b", flags=re.UNICODE)


from libs.text import *
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

def cmd_stats(path_str: str, top: int) -> int:
    """
    Посчитать частоты слов в текстовом файле и вывести топ-N.
    Возвращает код выхода.
    """
    p = Path(path_str)
    try:
        text = p.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"Ошибка: файл не найден: {p}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}", file=sys.stderr)
        return 2
    if not text:
        print("Файл пустой.", file=sys.stderr)
        return 3
    counter = count_freq(tokenize(text))
    if not counter:
        print("Слов не найдено.", file=sys.stderr)
        return 3
    print(format(top_n(counter, 5)))
    return 0


def build_parser() -> argparse.ArgumentParser:
    """
    Построить парсер аргументов для CLI.
    """
    parser = argparse.ArgumentParser(description="Текстовые CLI-утилиты (cat, stats)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_cat = sub.add_parser("cat", help="Вывести содержимое файла")
    p_cat.add_argument("--input", "-i", required=True, help="Путь к файлу (относительный)")
    p_cat.add_argument("-n", action="store_true", help="Нумеровать строки")

    p_stats = sub.add_parser("stats", help="Частоты слов в тексте")
    p_stats.add_argument("--input", "-i", required=True, help="Путь к текстовому файлу (относительный)")
    p_stats.add_argument("--top", "-t", type=int, default=5, help="Сколько топ-слов вывести")

    return parser


def main(argv: List[str] | None = None) -> int:
    """
    Точка входа для запуска CLI из командной строки.
    Возвращает код завершения (для sys.exit).
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.cmd == "cat":
        return cmd_cat(args.input, bool(args.n))
    if args.cmd == "stats":
        top = args.top if args.top and args.top > 0 else 5
        return cmd_stats(args.input, top)
    print("Неизвестная команда", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
