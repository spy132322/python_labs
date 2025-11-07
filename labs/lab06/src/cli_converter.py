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
