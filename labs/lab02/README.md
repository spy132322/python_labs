## Лаба 02

### Таска 1
```python
def min_max(nums: list[float | int]) -> tuple[float | int, float | int] | type[ValueError]:
    return (min(nums), max(nums)) if (len(nums) != 0) else ValueError

def unique_sorted(nums: list[float | int]) -> list[float | int]:    
    return sorted(list(set(nums)))

def flatten(mat: list[list | tuple]) -> list | type[TypeError]:
    output = []
    for obj in mat:
        if not isinstance(obj, tuple) and not isinstance(obj, list):
            return TypeError
        for val in obj:
            output.append(val)
    return output
```
![Task1](/lab02/images/01.jpg)

### Таска B
```python
def transpose(mat: list[list[float | int]]) -> list[list[float | int]] | type[ValueError]:
    if not mat:
        return []
    row_length = len(mat[0])    
    for item in mat:
        if len(item) != row_length: return ValueError
    return [[row[i] for row in mat] for i in range(row_length)]
def col_sum(mat: list[list[float | int]]) -> list[float] | type[ValueError]:
    if not mat: return []
    row_length = len(mat[0])
    for item in mat:
        if len(item) != row_length: return ValueError
    nmat = transpose(mat)
    return [sum(arr) for arr in nmat] # type: ignore

def row_sum(mat: list[list[float | int]]) -> list[float] | type[ValueError]:
    if not mat: return []
    row_length = len(mat[0])
    for item in mat:
        if len(item) != row_length: return ValueError
    return [sum(arr) for arr in mat]
```
![Task1](/lab02/images/02.jpg)

### Таска C
```python
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
        return f"{n1[0].upper() + n1[1:]} {n2[0]}.{n3[0] if n3 else n2[0]}., гр. {rec[1].upper()}, GPA {rec[2]:.2f}"
    except:
        pass
    try:
        n1,n2 = rec[0].strip().split()
        return f"{n1[0].upper() + n1[1:]} {n2[0]}.{n2[0]}., гр. {rec[1].upper()}, GPA {rec[2]:.2f}"
    except Exception as e: print(e); return ValueError('Неверное ФИО')
```

![Task1](/lab02/images/03.jpg)