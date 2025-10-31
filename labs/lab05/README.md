## 5я лаба
### Код функций
```python
# src/lab05/json_csv.py
from pathlib import Path
import json
import csv
from typing import List, Dict, Any


def _ensure_relative(path: Path) -> None:
    if path.is_absolute():
        raise ValueError("Путь должен быть относительным")


def json_to_csv(json_path: str | Path, csv_path: str | Path) -> None:
    """
    Преобразует JSON-файл в CSV.

    Поддерживается только JSON, содержащий список словарей: [{...}, {...}, ...].
    Порядок колонок: берётся порядок ключей из первого объекта списка (т.е. порядок
    сохранённый в первом dict). Если у последующих объектов отсутствует поле,
    в CSV подставляется пустая строка.

    Кодировка: UTF-8.

    Ошибки:
        - неверный тип файла (расширение) -> ValueError
        - путь абсолютный -> ValueError
        - отсутствующий файл -> FileNotFoundError (при открытии)
        - пустой JSON или неподдерживаемая структура -> ValueError
        - список содержит элементы не-словари -> ValueError
    """
    jp = Path(json_path)
    cp = Path(csv_path)

    _ensure_relative(jp)
    _ensure_relative(cp)

    if jp.suffix.lower() != ".json":
        raise ValueError("Неверный тип входного файла: ожидался .json")
    if cp.suffix.lower() != ".csv":
        raise ValueError("Неверный тип выходного файла: ожидался .csv")

    with jp.open("r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Невалидный JSON: {e}")

    if not isinstance(data, list) or len(data) == 0:
        raise ValueError("Пустой JSON или неподдерживаемая структура")

    if not all(isinstance(item, dict) for item in data):
        raise ValueError("Список должен содержать только словари")

    first = data[0]
    if not isinstance(first, dict) or len(first) == 0:
        headers: List[str] = list(first.keys())
    else:
        headers = list(first.keys())

    all_keys = set()
    for d in data:
        all_keys.update(d.keys())

    remaining = [k for k in sorted(all_keys) if k not in headers]
    headers.extend(remaining)

    if cp.parent and not cp.parent.exists():
        cp.parent.mkdir(parents=True, exist_ok=True)

    with cp.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers, extrasaction='ignore')
        writer.writeheader()
        for row in data:
            out_row = {k: ("" if row.get(k) is None else str(row.get(k))) for k in headers}
            writer.writerow(out_row)


def csv_to_json(csv_path: str | Path, json_path: str | Path) -> None:
    """
    Преобразует CSV в JSON (список словарей).

    Первая строка CSV обязана быть заголовком. Все значения сохраняются как строки.
    Результат записывается с json.dump(..., ensure_ascii=False, indent=2).

    Кодировка: UTF-8.

    Ошибки:
        - неверный тип файла (расширение) -> ValueError
        - путь абсолютный -> ValueError
        - отсутствующий файл -> FileNotFoundError (при открытии)
        - CSV без заголовка или пустой -> ValueError
    """
    cp = Path(csv_path)
    jp = Path(json_path)

    _ensure_relative(cp)
    _ensure_relative(jp)

    if cp.suffix.lower() != ".csv":
        raise ValueError("Неверный тип входного файла: ожидался .csv")
    if jp.suffix.lower() != ".json":
        raise ValueError("Неверный тип выходного файла: ожидался .json")

    with cp.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("CSV без заголовка или пустой")
        rows: List[Dict[str, str]] = []
        for raw in reader:
            row = {k: ("" if v is None else str(v)) for k, v in raw.items()}
            rows.append(row)

    if len(rows) == 0:
        raise ValueError("CSV без заголовка или пустой")

    if jp.parent and not jp.parent.exists():
        jp.parent.mkdir(parents=True, exist_ok=True)

    with jp.open("w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

from pathlib import Path
import csv
from typing import List

def csv_to_xlsx(csv_path: str | Path, xlsx_path: str | Path) -> None:
    """
    Конвертирует CSV в XLSX.

    Требования:
        - Использует openpyxl (если не установлен, бросает ImportError с подсказкой).
        - Первая строка CSV — заголовок.
        - Лист называется "Sheet1".
        - Колонки получают автоширину по длине текста (минимум 8).
        - Кодировка CSV: UTF-8.

    Ошибки:
        - неверный тип файла (расширение) -> ValueError
        - путь абсолютный -> ValueError
        - отсутствующий файл -> FileNotFoundError (при открытии)
        - CSV без заголовка или пустой -> ValueError
    """
    cp = Path(csv_path)
    xp = Path(xlsx_path)

    _ensure_relative(cp)
    _ensure_relative(xp)

    if cp.suffix.lower() != ".csv":
        raise ValueError("Неверный тип входного файла: ожидался .csv")
    if xp.suffix.lower() not in (".xlsx",):
        raise ValueError("Неверный тип выходного файла: ожидался .xlsx")
    try:
        from openpyxl import Workbook
        from openpyxl.utils import get_column_letter
    except ImportError as e:
        raise ImportError(
            "Для конвертации CSV в XLSX требуется пакет 'openpyxl'. "
            "Установите его: pip install openpyxl"
        ) from e

    with cp.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        try:
            rows = list(reader)
        except csv.Error as e:
            raise ValueError(f"Ошибка при чтении CSV: {e}")

    if not rows:
        raise ValueError("CSV без заголовка или пустой")

    header = rows[0]
    if not header or all(h == "" for h in header):
        raise ValueError("CSV без заголовка или пустой")

    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"

    for r in rows:
        ws.append([("" if c is None else str(c)) for c in r])

    num_cols = max(len(r) for r in rows)
    col_max_lengths: List[int] = [0] * num_cols
    for r in rows:
        for i in range(num_cols):
            val = ""
            if i < len(r) and r[i] is not None:
                val = str(r[i])
            l = len(val)
            if l > col_max_lengths[i]:
                col_max_lengths[i] = l

    MIN_WIDTH = 8
    for i, maxlen in enumerate(col_max_lengths, start=1):
        width = max(MIN_WIDTH, maxlen)
        width = float(width) + 1.5
        col_letter = get_column_letter(i)
        ws.column_dimensions[col_letter].width = width

    if xp.parent and not xp.parent.exists():
        xp.parent.mkdir(parents=True, exist_ok=True)

    wb.save(str(xp))

```

### Тест 1 json -> csv

#### Тест по файлика из лабы

Вход:
[in](/labs/lab05/test_files/ready/people.json)
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
[out](/labs/lab05/output/ready/people_out.csv)
```csv
name,age,city
Alice,22,SPB
Bob,25,Moscow
Carlos,30,Kazan
Dana,21,SPB
Andrey,27,Novosibirsk
```

#### Тест по моим 100 % оригинальным файликам
Vhod
[in](/labs/lab05/test_files/my/100%_original.json)
```json
[
  {
    "name": "Elena",
    "age": 23,
    "city": "Moscow"
  },
  {
    "name": "Igor",
    "age": 29,
    "city": "SPB"
  },
  {
    "name": "Maria",
    "age": 26,
    "city": "Kazan"
  },
  {
    "name": "Sergey",
    "age": 24,
    "city": "Yekaterinburg"
  },
  {
    "name": "Olga",
    "age": 31,
    "city": "Novosibirsk"
  }
]
```
Выход:
[out](/labs/lab05/output/my/people_out.csv)
```csv
name,age,city
Elena,23,Moscow
Igor,29,SPB
Maria,26,Kazan
Sergey,24,Yekaterinburg
Olga,31,Novosibirsk
```

### Тест 2 csv -> json

#### Тест по файликам из лабы

Вход:
[in](/labs/lab05/test_files/ready/people.csv)
```csv
name,age,city
Alice,22,SPB
Bob,25,Moscow
Carlos,30,Kazan
Dana,21,SPB
Andrey,27,Novosibirsk
```
Выход:
[out](/labs/lab05/output/ready/people_out.json)
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

#### Тест по моим файлам
Вход:
[in](/labs/lab05/test_files/my/100%25_original.csv)
```csv
city,country,population
Nizhny Novgorod,Russia,1259015
Samara,Russia,1134730
Rostov-on-Don,Russia,1115093
Ufa,Russia,1091204
Perm,Russia,1048000
```
Выход:
[out](/labs/lab05/output/my/people_out.json)
```json
[
  {
    "city": "Nizhny Novgorod",
    "country": "Russia",
    "population": "1259015"
  },
  {
    "city": "Samara",
    "country": "Russia",
    "population": "1134730"
  },
  {
    "city": "Rostov-on-Don",
    "country": "Russia",
    "population": "1115093"
  },
  {
    "city": "Ufa",
    "country": "Russia",
    "population": "1091204"
  },
  {
    "city": "Perm",
    "country": "Russia",
    "population": "1048000"
  }
]
```

### Тест 3й функции csv -> xlsx

#### Тестим на файликах лабы
Вход:
[in](/labs/lab05/test_files/ready/cities.csv)
```csv
city,country,population
SPB,Russia,5384342
Moscow,Russia,13010112
Kazan,Russia,1306953
Novosibirsk,Russia,1620162
Yekaterinburg,Russia,1493749
```
Выход:
[out](/labs/lab05/output/ready/cities_out.xlsx)

#### Тестим на моих щедевро файлах

Вход:
[in](/labs/lab05/test_files/my/100%_original.csv)
```csv
city,country,population
Nizhny Novgorod,Russia,1259015
Samara,Russia,1134730
Rostov-on-Don,Russia,1115093
Ufa,Russia,1091204
Perm,Russia,1048000
```
[out](/labs/lab05/output/my/city_out.xlsx)