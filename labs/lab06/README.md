## Лаба 6

### Таски
#### cli_text.py
[читалка со статой](/labs/lab06/src/cli_text.py)
```python
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
```
#### Скриншотики

[хелпа](/labs/lab06/images/01_1.png)

[тест_ф](/labs/lab06/images/01_02.png)

[тест_ф2](/labs/lab06/images/01_03.png)

#### Конвертер
[супер удобная тулза](/labs/lab06/src/cli_converter.py)
```python
"""
CLI для конвертеров: json2csv, csv2json, csv2xlsx.

Команды:
  json2csv --in <input.json> --out <output.csv>
  csv2json --in <input.csv> --out <output.json>
  csv2xlsx --in <input.csv> --out <output.xlsx>

Ошибки печатаются в stderr, при ошибке код возврата != 0.
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
from typing import List
from libs.conver import json_to_csv, csv_to_json, csv_to_xlsx


def _run_action(func, src: str, dst: str) -> int:
    try:
        func(Path(src), Path(dst))
    except FileNotFoundError as e:
        print(f"Ошибка: файл не найден: {e}", file=sys.stderr)
        return 2
    except ValueError as e:
        print(f"Неверные данные: {e}", file=sys.stderr)
        return 3
    except ImportError as e:
        print(f"Зависимость отсутствует: {e}", file=sys.stderr)
        return 4
    except PermissionError as e:
        print(f"Ошибка доступа: {e}", file=sys.stderr)
        return 5
    except Exception as e:
        print(f"Неожиданная ошибка: {e}", file=sys.stderr)
        return 6
    return 0


def build_parser() -> argparse.ArgumentParser:
    """
    Построить парсер аргументов для CLI конвертеров.
    """
    parser = argparse.ArgumentParser(description="Конвертеры данных (json/csv/xlsx)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    j2c = sub.add_parser("json2csv", help="JSON -> CSV")
    j2c.add_argument("--in", dest="input", required=True, help="Входной JSON (относительный путь)")
    j2c.add_argument("--out", dest="output", required=True, help="Выходной CSV (относительный путь)")

    c2j = sub.add_parser("csv2json", help="CSV -> JSON")
    c2j.add_argument("--in", dest="input", required=True, help="Входной CSV (относительный путь)")
    c2j.add_argument("--out", dest="output", required=True, help="Выходной JSON (относительный путь)")

    c2x = sub.add_parser("csv2xlsx", help="CSV -> XLSX")
    c2x.add_argument("--in", dest="input", required=True, help="Входной CSV (относительный путь)")
    c2x.add_argument("--out", dest="output", required=True, help="Выходной XLSX (относительный путь)")

    return parser


def main(argv: List[str] | None = None) -> int:
    """
    Точка входа для CLI конвертеров. Возвращает код завершения.
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.cmd == "json2csv":
        return _run_action(json_to_csv, args.input, args.output)
    if args.cmd == "csv2json":
        return _run_action(csv_to_json, args.input, args.output)
    if args.cmd == "csv2xlsx":
        return _run_action(csv_to_xlsx, args.input, args.output)
    print("Неизвестная команда", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

```
#### Хелпулина

[хелп](/labs/lab06/images/02_01.png)

### Тестики функций для 2й файлика

Вход:
[in](/labs/lab06/data/people.json)
```json
[
  {
    "name": "Alice",
    "age": 22,
    "city": "SPB"
  },
  {
    "name": "Bob",
    "age": 25,
    "city": "Moscow"
  },
  {
    "name": "Carlos",
    "age": 30,
    "city": "Kazan"
  },
  {
    "name": "Dana",
    "age": 21,
    "city": "SPB"
  },
  {
    "name": "Andrey",
    "age": 27,
    "city": "Novosibirsk"
  }
]
```
Выхлоп:
[out](/labs/lab06/data/output/people_out.csv)
```csv
name,age,city
Alice,22,SPB
Bob,25,Moscow
Carlos,30,Kazan
Dana,21,SPB
Andrey,27,Novosibirsk
```


### Тест 2 csv -> json

Вход:
[in](/labs/lab06/data/people.csv)
```csv
name,age,city
Alice,22,SPB
Bob,25,Moscow
Carlos,30,Kazan
Dana,21,SPB
Andrey,27,Novosibirsk
```
Выход:
[out](/labs/lab06/data/output/people_out.json)
```json
[
  {
    "name": "Alice",
    "age": "22",
    "city": "SPB"
  },
  {
    "name": "Bob",
    "age": "25",
    "city": "Moscow"
  },
  {
    "name": "Carlos",
    "age": "30",
    "city": "Kazan"
  },
  {
    "name": "Dana",
    "age": "21",
    "city": "SPB"
  },
  {
    "name": "Andrey",
    "age": "27",
    "city": "Novosibirsk"
  }
]
```


### Тест 3й функции csv -> xlsx

Вход:
[in](/labs/lab06/data/cities.csv)
```csv
city,country,population
SPB,Russia,5384342
Moscow,Russia,13010112
Kazan,Russia,1306953
Novosibirsk,Russia,1620162
Yekaterinburg,Russia,1493749
```
Выход:
[out](/labs/lab06/data/output/ready/cities_out.xlsx)
