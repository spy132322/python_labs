#!/usr/bin/env python3
"""count_text.py — утилита подсчёта частот слов в текстовых файлах (.txt).

Особенности:
- Принимает один или несколько входных файлов с расширением ``.txt``.
- Поддерживает указание кодировки (по умолчанию utf-8).
- Может сохранять отчёт по каждому файлу (--per-file) и/или сводный отчёт (--total) в CSV-файлы.
- Выполняет базовые проверки ввода (существование файлов и расширения).
- Докстринги и аннотации типов присутствуют для удобства сопровождения и тестирования.

Примеры запуска:
    python count_text.py --in data/input.txt
    python count_text.py --in a.txt b.txt --per-file report_per_file.csv --total report_total.csv
    python count_text.py --in data/input_cp1251.txt --encoding cp1251 --total report.csv
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

from libs.text import normalize, tokenize, count_freq  # ожидается из ЛР3


def _is_txt_file(path: str | Path) -> bool:
    """Возвращает True, если путь имеет расширение .txt (регистр игнорируется)."""
    return Path(path).suffix.lower() == ".txt"


def validate_input_files(paths: Iterable[str]) -> List[Path]:
    """Проверяет существование и расширение входных файлов.

    Args:
        paths: Итерация по путям к файлам (строки).

    Returns:
        Список объектов Path для существующих файлов.

    Raises:
        FileNotFoundError: если какой-то файл не найден.
        ValueError: если файл не имеет расширения .txt.
    """
    validated: List[Path] = []
    for p in paths:
        path_obj = Path(p)
        if not _is_txt_file(path_obj):
            raise ValueError(f"Неподдерживаемое расширение файла: '{p}'. Поддерживается только .txt")
        if not path_obj.exists():
            raise FileNotFoundError(f"Файл не найден: '{p}'")
        if not path_obj.is_file():
            raise FileNotFoundError(f"Ожидался файл, но найден не файл: '{p}'")
        validated.append(path_obj)
    return validated


def ensure_parent_dir(path: str | Path) -> None:
    """Создаёт родительские директории для пути, если их нет.

    Полезно перед записью файлов отчёта.
    """
    p = Path(path)
    parent = p.parent
    if parent and not parent.exists():
        parent.mkdir(parents=True, exist_ok=True)


def write_csv_word_counts(path: str | Path, freqs: Dict[str, int]) -> None:
    """Записывает словарь частот в CSV формата: word,count

    Строки сортируются по убыванию частоты (count ↓) и затем по слову (word ↑).
    Кодировка выходного CSV — utf-8.

    Args:
        path: Путь к CSV-файлу, будет перезаписан.
        freqs: Словарь {word: count}.
    """
    ensure_parent_dir(path)
    rows = sorted(freqs.items(), key=lambda kv: (-kv[1], kv[0]))
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["word", "count"])
        for word, count in rows:
            writer.writerow([word, count])


def write_csv_rows(path: str | Path, header: Sequence[str] | None, rows: Iterable[Sequence]) -> None:
    """Записывает последовательность строк в CSV файл.

    Проверяет, что каждая строка имеет одинаковую длину. Если header передан, он записывается первым.
    Кодировка — utf-8.

    Args:
        path: Путь к CSV-файлу.
        header: Заголовок (tuple/лист строк) или None.
        rows: Итерация по строкам (tuple/list) одинаковой длины.

    Raises:
        ValueError: если строки разной длины.
    """
    rows_list = list(rows)
    if not rows_list and header is None:
        # Пустой файл — создаём пустой файл
        ensure_parent_dir(path)
        Path(path).write_text("", encoding="utf-8", newline="")
        return

    # Если есть header — ожидаем одинаковую длину
    expected_len = None
    if header is not None:
        expected_len = len(header)
    else:
        if rows_list:
            expected_len = len(rows_list[0])

    for r in rows_list:
        if len(r) != expected_len:
            raise ValueError("Все строки для записи в CSV должны иметь одинаковую длину")


    ensure_parent_dir(path)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if header is not None:
            writer.writerow(header)
        for r in rows_list:
            writer.writerow(r)


def process_file(path: Path, encoding: str = "utf-8") -> Dict[str, int]:
    """Читает текстовый файл, нормализует, токенизирует и считает частоты токенов.

    Args:
        path: Путь к .txt файлу (Path).
        encoding: Кодировка для чтения (по умолчанию 'utf-8').

    Returns:
        Словарь частот {word: count}.

    Raises:
        FileNotFoundError: если файл не найден.
        UnicodeDecodeError: если указана неверная кодировка — ошибка будет проброшена.
    """
    # Пропускаем доп. проверку расширения здесь — считаем, что caller уже валидировал
    with path.open("r", encoding=encoding) as f:
        text = f.read()
    tokens = tokenize(normalize(text))
    return count_freq(tokens)


def report_console(freqs: Dict[str, int], top_n: int = 5) -> None:
    """Печатает короткое резюме статистики в консоль.

    Формат:
        Всего слов: <N>
        Уникальных слов: <K>
        Топ-5:
        слово:count
        ...
    """
    total_words = sum(freqs.values())
    unique_words = len(freqs)
    print(f"Всего слов: {total_words}")
    print(f"Уникальных слов: {unique_words}")
    print(f"Топ-{top_n}:")


    top = sorted(freqs.items(), key=lambda kv: (-kv[1], kv[0]))[:top_n]
    for word, count in top:
        print(f"{word}:{count}")


def main(argv: List[str] | None = None) -> None:
    """Парсит аргументы командной строки, выполняет проверки и формирует CSV-отчёты.

    Поведение по ошибкам:
    - Неподдерживаемые расширения входных файлов — программа завершится с кодом 2 и печатью ошибки.
    - Отсутствующие файлы — код 2 и сообщение.
    - Ошибки декодирования (UnicodeDecodeError) — будут проброшены (и обработаны здесь для дружелюбного вывода).
    """
    parser = argparse.ArgumentParser(description="Генерация отчёта по текстам (.txt → .csv)")
    parser.add_argument("--in", dest="inputs", nargs="+", required=True, help="Входные .txt файлы")
    parser.add_argument("--encoding", default="utf-8", help="Кодировка входных файлов (по умолчанию utf-8)")
    parser.add_argument("--per-file", help="Путь к CSV отчёту по каждому файлу (file,word,count)")
    parser.add_argument("--total", help="Путь к сводному CSV отчёту (word,count)")
    args = parser.parse_args(argv)

    try:
        input_paths = validate_input_files(args.inputs)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Ошибка входных данных: {exc}", file=sys.stderr)
        sys.exit(2)

    # Проверим расширения выходных файлов, если они заданы — ожидаем .csv
    for out_arg, out_val in (("--per-file", args.per_file), ("--total", args.total)):
        if out_val is not None and Path(out_val).suffix.lower() != ".csv":
            print(f"Неправильное расширение для {out_arg}: ожидается .csv", file=sys.stderr)
            sys.exit(2)

    try:
        # Пер-файловый отчёт
        if args.per_file:
            per_file_rows: List[Tuple[str, str, int]] = []
            for path in input_paths:
                freqs = process_file(path, args.encoding)
                filename = path.name
                # собираем в виде (file, word, count)
                for word, count in freqs.items():
                    per_file_rows.append((filename, word, count))

                print(f"\n--- {filename} ---")
                report_console(freqs)

            # Сортируем: file ↑, count ↓, word ↑
            per_file_rows_sorted = sorted(per_file_rows, key=lambda r: (r[0], -int(r[2]), r[1]))
            write_header = ("file", "word", "count")
            write_csv_rows(args.per_file, write_header, per_file_rows_sorted)

        # Сводный отчёт
        if args.total:
            total_freqs: Dict[str, int] = {}
            for path in input_paths:
                freqs = process_file(path, args.encoding)
                for word, count in freqs.items():
                    total_freqs[word] = total_freqs.get(word, 0) + count

            write_csv_word_counts(args.total, total_freqs)

            print("\n=== ИТОГОВЫЙ ОТЧЁТ ===")
            report_console(total_freqs)

    except UnicodeDecodeError as exc:
        print(f"Ошибка чтения файла (возможно неверная кодировка): {exc}", file=sys.stderr)
        sys.exit(3)
    except Exception as exc:  # общий fallback — печатаем и выходим с кодом 1
        print(f"Произошла непредвиденная ошибка: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
