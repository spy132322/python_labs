from serilize import *
from models import Student
print("Тестим функцию погребания в json с list[Student]")
students = [
    Student(fio="Как Его Зовут1", birthdate="2025-11-15", gpa=2, group="Придумайте ченить для группы1"),
    Student(fio="Как Его Зовут2", birthdate="2025-11-16", gpa=3, group="Придумайте ченить для группы2"),
    Student(fio="Как Его Зовут3", birthdate="2025-11-17", gpa=4, group="Придумайте ченить для группы3"),
]
students_to_json(students=students, path="data/std_output.json")

print("Тестим функцию выгрубания с json в list[Student]")
print(students_from_json(path="data/std_unput.json"))

print("Тест ошбок")
Student(-1, "Отс", "2025-12-11", "aaaa")
