def format_record(rec: tuple[str, str, float]) -> str | type[ValueError] | type[TypeError]:
    """
    Форматирует запись о студенте в строку вида:
    "Фамилия И.О., гр. GROUP, GPA X.XX".

    Аргументы:
        rec (tuple[str, str, float]):
            - rec[0]: строка с ФИО (2 или 3 слова).
            - rec[1]: название группы (строка, не пустая).
            - rec[2]: средний балл (float или int).

    Возвращает:
        str: Отформатированная строка с фамилией, инициалами, группой и GPA.
        ValueError: Если не указана группа или неверно задано ФИО.
        TypeError: Если средний балл не является числом (float или int).

    Примеры:
        >>> format_record(("иванов иван иванович", "пи-101", 4.25))
        'Иванов И.И., гр. ПИ-101, GPA 4.25'

        >>> format_record(("сидоров петр", "пи-102", 3))
        'Сидоров П.П., гр. ПИ-102, GPA 3.00'
    """
    if len(rec[1]) == 0: return ValueError('Гиде группа??')
    if not isinstance(rec[2], float) and not isinstance(rec[2], int): return TypeError('что ты сюда вписал?')
    try:
        n1,n2,n3 = rec[0].strip().split()
        return f"{n1[0].upper() + n1[1:]} {n2[0].upper()}.{n3[0].upper() if n3 else n2[0].upper()}., гр. {rec[1].upper()}, GPA {rec[2]:.2f}"
    except:
        pass
    try:
        n1,n2 = rec[0].strip().split()
        return f"{n1[0].upper() + n1[1:]} {n2[0].upper()}.{n2[0].upper()}., гр. {rec[1].upper()}, GPA {rec[2]:.2f}"
    except Exception as e: print(e); return ValueError('Неверное ФИО')
