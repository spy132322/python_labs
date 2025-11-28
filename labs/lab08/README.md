## Лаба 08

### Код А
```python
from dataclasses import dataclass
from checks import verify_date, verify_gpa, verify_type
from datetime import datetime

@dataclass
class Student:
    gpa: float
    fio: str
    birthdate: str
    group: str
    
    # Проверка в postinit
    def __post_init__(self):
        verify_gpa(self.gpa)
        verify_date(self.birthdate)

    # Экспорт данных оьекта в dict
    def to_dict(self) -> dict:
        """
        Вывод данных в dict
        out: {"gpa": int, "fio": str, "group": str, "birthdate": str}
        """
        return {
            "gpa": self.gpa,
            "fio": self.fio,
            "group": self.group,
            "birthdate": self.birthdate
        }

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            fio=d["fio"],
            birthdate=d["birthdate"],
            group=d["group"],
            gpa=d["gpa"],
        )
    # Возраст относительно даты или относительно тек времени
    def age(self, from_date = None)->int:
        """
        Возраст студент относительно даты или тек времени
        Out: years [int]
        """
        if from_date is None:
            from_date = datetime.now()
        try:
            return from_date.replace(year=from_date.year - datetime.strptime(self.birthdate, "Y%-%m-%d").year).year
        except ValueError:
            assert from_date.month == 2 and from_date.day == 29
            return from_date.replace(month=2, day=28,
                                     year=from_date.year-datetime.strptime(self.birthdate, "Y%-%m-%d").year).year

    def __str__(self):
        return f"Студынт: {self.fio}\nGPA: {self.gpa}\nДата самоуничтожения: {self.birthdate}\nГруппа: {self.group}"
```

Код В
```python
import json
from models import Student
from checks import verify_type

def students_to_json(students, path):
    data = [s.to_dict() for s in students]
    with open(path, "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def students_from_json(path):
    with open(path, "r", encoding='utf-8') as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise TypeError

    student_list = []
    for d in data:
        verify_type(d, dict)
        verify_type(d.get('fio'), str)
        verify_type(d.get('birthdate'), str)
        verify_type(d.get('gpa'), float)
        verify_type(d.get('group'), str)
        try:
            student = Student.from_dict(d)
        except Exception as e:
            raise ValueError

        student_list.append(student)

    return student_list
```

Код Проверщика
```python
def verify_date(data: str) -> None:
    """
    Verify date format func and validate
    input:
        YYYY-MM-DD
    output:
        None
    """
    import datetime
    try:
        datetime.date.fromisoformat(data)
        return None
    except ValueError:
        raise ValueError('Неверный формат даты')

def verify_gpa(data: float) -> None:
    """
    Проверка gpa ∈ [0; 5]
    """
    if (data < 0) or (data > 5):
        raise ValueError('Выход за границы gpa')
    return None

def verify_type(data, val_type: type):
    if not isinstance(data, val_type):
        raise TypeError('Неверный тип данных на входе')
```


### Тесты 

![picture](/labs/lab08/images/01.png)

#### Данные ввода для теста импорта из json

![picture2](/labs/lab08/images/02.png)

### Выход

#### Файл с данными для теста экспорта в json

![file_inp](/labs/lab08/images/03.png)