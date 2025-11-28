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