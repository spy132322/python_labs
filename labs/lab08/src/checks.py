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