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
        out: {"gpa": float, "fio": str, "group": str, "birthdate": str}
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