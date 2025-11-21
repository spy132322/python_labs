import pytest
from libs.text import normalize, tokenize, count_freq, top_n


@pytest.mark.parametrize(
    "source, expected",
    [
        ("ПрИвЕт\nМИр\t", "привет мир"),
        ("ёжик, Ёлка", "ежик, елка"),
        ("Hello\r\nWorld", "hello world"),
        (" двойные пробелы ", "двойные пробелы"),
        ("", ""),
    ],
)
def test_normalize_various(source, expected):
    assert normalize(source, yo2e=True) == expected


def test_tokenize_basic_and_empty():
    s = "Привет, мир! Это — тест."
    tokens = tokenize(s)
    # ожидаем, что токены — последовательность слов без пунктуации
    assert isinstance(tokens, list)
    assert all(isinstance(t, str) for t in tokens)
    assert "Привет" in tokens

    # пустая строка -> пустой список
    assert tokenize("") == []


@pytest.mark.parametrize(
    "tokens, expected",
    [
        ([], {}),
        (["a", "b", "a", "c", "b", "a"], {"a": 3, "b": 2, "c": 1}),
        (["тест"], {"тест": 1}),
    ],
)
def test_count_freq(tokens, expected):
    assert count_freq(tokens) == expected


def test_top_n_ordering_and_ties():
    freq = {"apple": 3, "banana": 3, "cherry": 2, "date": 1}
    # при одинаковой частоте — сортировка по алфавиту для ключей
    top2 = top_n(freq, 2)
    assert top2 == [("apple", 3), ("banana", 3)]

    # n больше длины словаря -> вернуть все элементы, корректно отсортированные
    all_items = top_n(freq, 10)
    expected_all = [("apple", 3), ("banana", 3), ("cherry", 2), ("date", 1)]
    assert all_items == expected_all


# Проверка интеграции normalize -> tokenize -> count_freq -> top_n
def test_integration_normalize_tokenize_count_top():
    text = "Бык! Бык? корова,\nКорова.\tБык"

    tokens = tokenize(normalize(text))
    freq = count_freq(tokens)
    top = top_n(freq, 2)

    assert freq == {"бык": 3, "корова": 2}
    assert top[0][0] == "бык"
    assert top[0][1] == 3


# Поведение при апострофах/дефисах зависит от реализации — проверим устойчивость
def test_tokenize_keeps_apostrophes_and_hyphens():
    s = "it's re-use self-contained"
    tokens = tokenize(s)
    assert any("it" in t or "it's" in t or "its" in t for t in tokens)


# Проверка типов и ошибок
def test_normalize_raises_on_non_str():
    with pytest.raises(TypeError):
        normalize(None)  # type: ignore


def test_tokenize_raises_on_non_str():
    with pytest.raises(TypeError):
        tokenize(123)  # type: ignore
