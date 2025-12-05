import csv
from pathlib import Path
from typing import List, Dict, Any
from models import Student


CSV_HEADER = ["fio", "birthdate", "group", "gpa"]


class Group:
    """
    Класс Group — простое CSV-хранилище студентов.

    Методы:
        - list() -> List[Student]
        - add(student: Student) -> None
        - find(substr: str) -> List[Student]
        - remove(fio: str) -> int  # возвращает число удалённых записей
        - update(fio: str, **fields) -> int  # возвращает число обновлённых записей
        - stats() -> dict  # аналитика по группе
    """

    def __init__(self, storage_path: str):
        self.path = Path(storage_path)
        self._ensure_storage_exists()

    def _ensure_storage_exists(self) -> None:
        """
        Создаёт файл и заголовок, если файла нет или он пустой / заголовка нет.
        """
        if not self.path.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(CSV_HEADER)
            return

        with self.path.open("r", encoding="utf-8", newline="") as f:
            try:
                reader = csv.reader(f)
                header = next(reader, None)
            except Exception:
                header = None

        if header is None or [h.strip() for h in header] != CSV_HEADER:
            with self.path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(CSV_HEADER)

    def _read_all_rows(self) -> List[Dict[str, str]]:
        """
        Возвращает все строки CSV в виде списка словарей (ключи - строки заголовка).
        Если файл пуст или нет данных, возвращает пустой список.
        """
        rows: List[Dict[str, str]] = []
        with self.path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                return []
            for r in reader:
                normalized = {k.strip(): (v.strip() if v is not None else "") for k, v in r.items()}
                rows.append(normalized)
        return rows

    def _write_all_rows(self, rows: List[Dict[str, Any]]) -> None:
        """
        Перезаписывает CSV из списка словарей. Значения будут приведены к строкам.
        """
        with self.path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_HEADER)
            writer.writeheader()
            for r in rows:
                out = {k: ("" if r.get(k) is None else str(r.get(k))) for k in CSV_HEADER}
                writer.writerow(out)

    def list(self) -> List[Student]:
        """
        Возвращает список всех студентов (объекты Student).
        """
        rows = self._read_all_rows()
        students: List[Student] = []
        for r in rows:
            try:
                r_conv = {
                    "fio": r.get("fio", ""),
                    "birthdate": r.get("birthdate", ""),
                    "group": r.get("group", ""),
                    "gpa": float(r.get("gpa", 0)) if r.get("gpa", "") != "" else 0.0,
                }
                students.append(Student.from_dict(r_conv))
            except Exception as e:
                continue
        return students

    def add(self, student: Student) -> None:
        """
        Добавляет нового студента в CSV (в конец). Не проверяет уникальность fio.
        """
        row = {
            "fio": student.fio,
            "birthdate": student.birthdate,
            "group": student.group,
            "gpa": float(student.gpa),
        }
        rows = self._read_all_rows()
        rows.append(row)
        self._write_all_rows(rows)

    def find(self, substr: str) -> List[Student]:
        """
        Поиск по подстроке в fio (регистронезависимо).
        Возвращает список объектов Student.
        """
        substr_lower = substr.lower()
        result: List[Student] = []
        for st in self.list():
            if substr_lower in st.fio.lower():
                result.append(st)
        return result

    def remove(self, fio: str) -> int:
        """
        Удаляет записи с точным соответствием fio.
        Возвращает число удалённых записей.
        """
        rows = self._read_all_rows()
        original_len = len(rows)
        rows = [r for r in rows if r.get("fio", "") != fio]
        removed = original_len - len(rows)
        if removed > 0:
            self._write_all_rows(rows)
        return removed

    def update(self, fio: str, **fields) -> int:
        """
        Обновляет поля у записей с точным fio.
        Поддерживаемые поля: fio, birthdate, group, gpa.
        Возвращает число обновлённых записей.
        """
        allowed = set(CSV_HEADER)
        update_keys = {k for k in fields.keys() if k in allowed}
        if not update_keys:
            return 0

        rows = self._read_all_rows()
        updated = 0
        for r in rows:
            
            if r.get("fio", "") == fio:
                for k in update_keys:
                    val = fields[k]
                    if k == "gpa":
                        try:
                            val = float(val)
                        except Exception:
                            continue
                    r[k] = str(val)
                updated += 1

        if updated > 0:
            self._write_all_rows(rows)
        return updated

    def stats(self) -> Dict[str, Any]:
        """
        Собирает простую аналитику по группе.
        Возвращает словарь:
            {
                "count": int,
                "min_gpa": float | None,
                "max_gpa": float | None,
                "avg_gpa": float | None,
                "groups": { "Группа": count, ... },
                "top_5_students": [ {"fio": ..., "gpa": ...}, ... ]
            }
        """
        students = self.list()
        count = len(students)
        if count == 0:
            return {
                "count": 0,
                "min_gpa": None,
                "max_gpa": None,
                "avg_gpa": None,
                "groups": {},
                "top_5_students": [],
            }

        gpas = [st.gpa for st in students]
        min_gpa = min(gpas)
        max_gpa = max(gpas)
        avg_gpa = sum(gpas) / len(gpas)

        groups_count: Dict[str, int] = {}
        for st in students:
            groups_count[st.group] = groups_count.get(st.group, 0) + 1

        top = sorted(students, key=lambda s: s.gpa, reverse=True)[:5]
        top_5 = [{"fio": s.fio, "gpa": s.gpa} for s in top]

        return {
            "count": count,
            "min_gpa": min_gpa,
            "max_gpa": max_gpa,
            "avg_gpa": avg_gpa,
            "groups": groups_count,
            "top_5_students": top_5,
        }
