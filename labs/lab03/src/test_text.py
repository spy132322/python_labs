import lib.text as form
# Test for normilize
print('\nTesting normilize func\n')
print(r'ПрИвЕт\nМИр\t  Out: ', form.normalize('ПрИвЕт\nМИр\t'))
print(r'ёжик, Ёлка  Out: ', form.normalize('ёжик, Ёлка', yo2e=True))
print(r'Hello\r\nWorld  Out: ', form.normalize('Hello\r\nWorld'))
print(r' двойные пробелы   Out: ', form.normalize(' двойные пробелы '))

# Tests for tokenize
print('\nTesting tokenize func\n')
print(r'привет мир Out:', form.tokenize('привет мир'))
print(r'hello,world!!! Out:', form.tokenize('hello,world!!!'))
print(r'по-настоящему круто Out:', form.tokenize('по-настоящему круто'))
print(r'2025 год Out:', form.tokenize('2025 год'))
print(r'emoji 😀 не слово Out:', form.tokenize('emoji 😀 не слово'))

# Tests for count and top
print('\nTesting count_freq & top_n\n')
print(f'["a","b","a","c","b","a"] Out counter: {form.count_freq(["a","b","a","c","b","a"])} Out top_n {form.top_n(form.count_freq(["a","b","a","c","b","a"]))}')
print(f'["bb","aa","bb","aa","cc"] Out counter: {form.count_freq(["bb","aa","bb","aa","cc"])} Out top_n {form.top_n(form.count_freq(["bb","aa","bb","aa","cc"]), 2)}')

