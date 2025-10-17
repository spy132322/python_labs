import argparse
import csv
import os
from libs.text import normalize, tokenize, count_freq

def write_csv(path: str, data: dict):
    """Сохраняет словарь частот в CSV: word,count"""
    with open(path, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["word", "count"])
        writer.writerows(data.items())

def process_file(path: str, encoding: str) -> dict:
    """Читает файл, нормализует, токенизирует и возвращает словарь частот"""
    with open(path, "r", encoding=encoding) as f:
        text = f.read()
    tokens = tokenize(normalize(text))
    return count_freq(tokens)

def report_console(freqs: dict):
    """Печатает статистику в консоль"""
    total_words = sum(freqs.values())
    unique_words = len(freqs)
    print(f"Всего слов: {total_words}")
    print(f"Уникальных слов: {unique_words}")
    print("Топ-5:")
    top5 = sorted(freqs.items(), key=lambda x: x[1], reverse=True)[:5]
    for word, count in top5:
        print(f"{word}:{count}")

def main():
    parser = argparse.ArgumentParser(description="Генерация отчёта по текстам")
    parser.add_argument("--in", dest="inputs", nargs="+", required=True, help="Входные файлы")
    parser.add_argument("--encoding", default="utf-8", help="Кодировка входных файлов (по умолчанию utf-8)")
    parser.add_argument("--per-file", help="Путь к CSV отчёту по каждому файлу")
    parser.add_argument("--total", help="Путь к сводному CSV отчёту")
    args = parser.parse_args()
    if args.per_file:
        per_file_rows = []
        for path in args.inputs:
            freqs = process_file(path, args.encoding)
            filename = os.path.basename(path)
            for word, count in freqs.items():
                per_file_rows.append((filename, word, count))
            print(f"\n--- {filename} ---")
            report_console(freqs)
        with open(args.per_file, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["file", "word", "count"])
            writer.writerows(per_file_rows)
    if args.total:
        total_freqs = {}
        for path in args.inputs:
            freqs = process_file(path, args.encoding)
            for word, count in freqs.items():
                total_freqs[word] = total_freqs.get(word, 0) + count
        write_csv(args.total, total_freqs)

        print("\n=== ИТОГОВЫЙ ОТЧЁТ ===")
        report_console(total_freqs)

if __name__ == "__main__":
    main()
